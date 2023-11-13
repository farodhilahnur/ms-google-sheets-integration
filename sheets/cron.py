from rest_framework.response import Response
from rest_framework.views import APIView
from sheets.models import LogLeads, SheetsAccounts, SheetsAds
from sheets.serializers import SheetsAdsSerializer
from .services import BaseParameterMixin, ExternalService
from rest_framework import mixins, generics
from .utils import err_resp, invalid_handler, succ_resp
from django.db import transaction
from django.http.response import HttpResponse
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def last_row(self):
    print('jalan cron')
    daata = SheetsAds.objects.filter(status='running')
    lists = []

    try:
        for d in daata:
            if(d.account_sheet != None and d.channelCode != None):

                tokene = SheetsAccounts.objects.filter(status='connected', email=d.account_sheet).values('token', 'refresh_token')
                creds = BaseParameterMixin().credentials_from_dict(tokens=list(tokene)[0]['token'], ref=list(tokene)[0]['refresh_token'])
                # If there are no (valid) credentials available, let the user log in.
                if not creds or not creds.valid:
                    if creds and creds.expired and creds.refresh_token:
                        creds.refresh(Request())
                    else:
                        creds = creds

                service_sheets = build('sheets', 'v4', credentials=creds)

                getrow = service_sheets.spreadsheets().values().get(spreadsheetId=d.spreadsheetId, range= d.worksheet_name+"!A1:Z").execute().get('values', [])

                lastrow_query = LogLeads.objects.filter(adsId=d.id, success=True).exclude(createdAt=None).values_list('row', flat=True).order_by('-createdAt')
                
                if(lastrow_query.count() == 0):
                    lastrow = int(1)
                else :
                    lastrow = int(lastrow_query[0])

                if(len(getrow) > lastrow) :
                    # ambil berapa banyak row yang baru
                    i = len(getrow) - lastrow

                    for y in range(i):
                        # index start dari last row
                        y+=lastrow
                        
                        data_lead = dict(zip(getrow[0], getrow[y]))

                        post_lead = ExternalService().post_lead(channel_code=d.channelCode, data_lead=data_lead)

                        if(post_lead.status_code == 200):
                            new_logs = LogLeads(
                                    adsId_id = d.id,
                                    lead_phone = None,
                                    success = True,
                                    row = y+1
                                )
                            new_logs.save()

                            # self.updatelog(adsId=d.id, lead_phone=None, success=True, row=y+1)
                        else :
                            new_logs = LogLeads(
                                    adsId_id = d.id,
                                    lead_phone = None,
                                    success = False,
                                    row = y+1
                                )
                            new_logs.save()

                            # self.updatelog(adsId=d.id, lead_phone=None, success=False, row=y+1)
                        
                        lists.append(data_lead)
    except :
        return []

    return lists