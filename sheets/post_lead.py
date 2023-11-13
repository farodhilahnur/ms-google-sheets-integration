from sheets.models import LogLeads, SheetsAds
from sheets.serializers import SheetsAdsSerializer
from .services import BaseParameterMixin, ExternalService
from rest_framework import mixins, generics
from .utils import err_resp, invalid_handler, succ_resp
from django.db import transaction
from django.http.response import HttpResponse
from googleapiclient.errors import HttpError

import rest_framework
import requests
import json
import os
import time

class POSTLeadListCreateView(BaseParameterMixin, mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    
    queryset = SheetsAds.objects.all()
    serializer_class = SheetsAdsSerializer

    def project_id(self, account_id, channel_id):
        project = ExternalService().get_project_channel(account_id=account_id, channel_id=channel_id)
        
        return project['campaign']['project']['id']

    def updatelog(self, adsId, lead_phone, success, row):
        new_logs = LogLeads(
                adsId_id = adsId,
                lead_phone = lead_phone,
                success = success,
                row = row
            )
        new_logs.save()

    def last_row(self):
        ssid = self.get_sheetsId()
        wsh = self.get_wsheets()
        prow = self.get_prow()

        service_sheets = self.service_google_api()
        daata = SheetsAds.objects.filter(status='running')
        lists = []
        try:
            for d in daata:
                getrow = service_sheets.spreadsheets().values().get(spreadsheetId=d.spreadsheetId, range= d.worksheet_name+"!A1:Z").execute().get('values', [])
                
                lastrow_query = LogLeads.objects.filter(adsId=d.id).values_list('row', flat=True).order_by('-createdAt')[0]
                lastrow = int(lastrow_query)

                if(len(getrow) > lastrow) :
                    # ambil berapa banyak row yang baru
                    i = len(getrow) - lastrow

                    for y in range(i):
                        # index start dari last row
                        y+=lastrow
                        data_lead = dict(zip(getrow[0], getrow[y]))
                        post_lead = ExternalService().post_lead(channel_code=d.channelCode, data_lead=data_lead)
                        
                        if(post_lead.status_code == 200):
                            self.updatelog(adsId=d.id, lead_phone=None, success=True, row=y+1)
                        else :
                            self.updatelog(adsId=d.id, lead_phone=None, success=False, row=y+1)
                        
                        lists.append(data_lead)
        except :
            return []

        return lists

    def get(self, request):
        account_id = self.get_account_id()
        user_id = self.get_user_id()
        since = self.get_since()
        until = self.get_until()
        external = ExternalService()
        
        postlead = self.last_row()

        return succ_resp(data=postlead)
  