from rest_framework.response import Response
from rest_framework.views import APIView
from sheets.models import ColumnAds, FilterSetup, LogLeads, SheetsAccounts, SheetsAds
from sheets.serializers import SheetsAdsSerializer
from .services import BaseParameterMixin, ExternalService
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import time
from collections import defaultdict
from itertools import groupby
import re
from string import Template
import json

class CekGsheetLeads(APIView, BaseParameterMixin):

    def get_queryset(self):
        account_id = self.get_account_id()
        
        queryset = SheetsAds.objects.filter(accountId=account_id)
        return queryset
    
    serializer_class = SheetsAdsSerializer

    def post_leads(self, d, body_leads, y, skip):
        post_lead = ExternalService().post_lead(channel_code=d.channelCode, data_lead=body_leads)
        if(post_lead.status_code == 200):
            
            new_logs = LogLeads(
                    adsId_id = d.id,
                    adsName = d.name,
                    lead_phone = body_leads['Phone'],
                    lead_name = body_leads['Name'],
                    lead_email = body_leads['Email'],
                    lead_notes = body_leads['Notes'],
                    success = True,
                    row = y+1,
                    skip = skip
                )
            new_logs.save()

        else :
            new_logs = LogLeads(
                    adsId_id = d.id,
                    adsName = d.name,
                    lead_phone = body_leads['Phone'],
                    lead_name = body_leads['Name'],
                    lead_email = body_leads['Email'],
                    lead_notes = body_leads['Notes'],
                    success = False,
                    row = y+1,
                    skip = skip
                )
            new_logs.save()

    def check_filter(self, rawdata, adsid, d, y, body_leads):
        fitlers_data =  FilterSetup.objects.filter(adsId=adsid).values('column', 'filter', 'text').order_by('id')
        sendleads = []

        for s in fitlers_data :
            if s['filter'] == 'Exist' :
                cek = False
                if rawdata[s['column'].lower()] != '' and rawdata[s['column'].lower()] != None:
                    cek = True
                sendleads.append(cek)

            elif s['filter'] == 'Does not exist' :
                cek = False
                if rawdata[s['column'].lower()] == None:
                    if rawdata[s['column'].lower()] == '' :
                        cek = True
                sendleads.append(cek)

            elif s['filter'] == 'Contains' :
                cek = False
                if s['text'].lower() in rawdata[s['column'].lower()] :
                    cek = True
                sendleads.append(cek)
            
            elif s['filter'] == 'Does not contains' :
                cek = False
                if s['text'].lower() not in rawdata[s['column'].lower()] :
                    cek = True
                sendleads.append(cek)
            
            elif s['filter'] == 'Exactly matches' :
                cek = False
                if s['text'].lower() == rawdata[s['column'].lower()] :
                    cek = True
                sendleads.append(cek)
            
            elif s['filter'] == 'Does not exactly matches' :
                cek = False
                if s['text'].lower() != rawdata[s['column'].lower()] :
                    cek = True
                sendleads.append(cek)

            else :
                sendleads.append(False)

        if False not in sendleads :
            self.post_leads(d=d, body_leads=body_leads, y=y, skip=False)

        else :
            new_logs = LogLeads(
                    adsId_id = d.id,
                    lead_phone = None,
                    success = True,
                    row = y+1,
                    skip = True
                )
            new_logs.save()


    def get(self, request):
        tokene = SheetsAccounts.objects.filter(status='connected').values('token', 'refresh_token', 'email')
        lists = []
        status='failed'
        detail='permission revoke'
        count = 0

        for t in tokene:
            try :
                creds = self.credentials_from_dict(tokens=None, ref=t['refresh_token'])
                service_sheets = build('sheets', 'v4', credentials=creds, cache_discovery=False)
            except :
                status='failed'
                detail='permission revoke'
                count = 0
            else :
                daata = SheetsAds.objects.filter(status='running', account_sheet=t['email'])
                for d in daata:
                    time.sleep(0.01)
                    status='success'
                    detail='succcess'
                    isfilter = False

                    try :
                        getrow = service_sheets.spreadsheets().values().get(spreadsheetId=d.spreadsheetId, range= d.worksheet_name+"!A1:Z").execute().get('values', [])
                    except :
                        getrow = None
                    else :
                        lastrow_query = LogLeads.objects.filter(adsId=d.id).exclude(createdAt=None).values_list('row', flat=True).order_by('-createdAt')
                        
                        if d.isFilter == True:
                            isfilter = True

                        if(lastrow_query.count() == 0):
                            lastrow = int(1)
                        else :
                            lastrow = int(lastrow_query[0])

                        if(len(getrow) > lastrow) :
                            names = ColumnAds.objects.filter(adsId_id=d.id).values_list('name', flat=True)
                            text = ColumnAds.objects.filter(adsId_id=d.id).values_list('text',flat=True)
                            custom = dict(zip(names, text))
                            body_leads = []

                            # ambil berapa banyak row yang baru
                            i = len(getrow) - lastrow
                            count=i
                            for y in range(i):
                                # index start dari last row
                                y+=lastrow
                                rowlead = dict(zip([i.lower().replace(" ", "_") for i in getrow[int(d.head)]], getrow[y]))
                                rowleads = dict(zip([i.replace(" ", "_") for i in getrow[int(d.head)]], getrow[y]))
                                body_leads = {}       
                                for k, v in custom.items():
                                    v = re.sub(r'\{.*?\}', lambda x: ''.join(x.group(0).replace(' ','_')), v)
                                    template_object = Template(v)
                                    formatted_string = template_object.safe_substitute(rowleads)
                                    # ini handling kalo value nya kosong, tp masih perlu optimasi
                                    if '$' in formatted_string :
                                        formatted_string = re.sub(r'\${.*?\}', ' ', formatted_string)

                                    # try :
                                    #     formatted_string= template_object.substitute(rowleads)
                                    #     # print(formatted_string)
                                    # except Exception:
                                    #     formatted_string = ''

                                    body_leads.update({k : formatted_string})
                                    if body_leads.get('Email') == None :
                                        body_leads.update({'Email' : None})
                                    if body_leads.get('Notes') == None :
                                        body_leads.update({'Notes' : None})

                                if(isfilter == True):
                                    self.check_filter(rawdata=rowlead, adsid=d.id, d=d, y=y, body_leads=body_leads)
                                
                                else :
                                    post_lead = ExternalService().post_lead(channel_code=d.channelCode, data_lead=body_leads)
                                    if(post_lead.status_code == 200):
                                        new_logs = LogLeads(
                                                adsId_id = d.id,
                                                adsName = d.name,
                                                lead_phone = body_leads['Phone'],
                                                lead_name = body_leads['Name'],
                                                lead_email = body_leads['Email'],
                                                lead_notes = body_leads['Notes'],
                                                success = True,
                                                row = y+1
                                            )
                                        new_logs.save()

                                    else :
                                        reslog = ''
                                        if post_lead.text != None :
                                            reslog = json.loads(post_lead.text)
                                        new_logs = LogLeads(
                                                adsId_id = d.id,
                                                adsName = d.name,
                                                lead_phone = body_leads['Phone'],
                                                lead_name = body_leads['Name'],
                                                lead_email = body_leads['Email'],
                                                lead_notes = body_leads['Notes'],
                                                success = False,
                                                row = y+1,
                                                log=reslog
                                            )
                                        new_logs.save()

        return Response(status=200, data=lists)