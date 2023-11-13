import email
import os.path
import json
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from sheets.callback import Callback
from sheets.models import SheetsAccounts
from sheets.services import BaseParameterMixin, ExternalService
from rest_framework import mixins, generics
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GetSheets(APIView, BaseParameterMixin):

    def get(self, request):
        account_id = self.get_account_id()
        email = self.get_email()
        list_sheets = []

        creds= None
        tokene = SheetsAccounts.objects.filter(accountId=account_id, email=email).values('token', 'refresh_token')
        if(list(tokene) != []):
            a = ExternalService().cek_token(token=str(list(tokene)[0]['token']))
            
            creds = self.credentials_from_dict(tokens=list(tokene)[0]['token'], ref=list(tokene)[0]['refresh_token'])

            service = build("drive", "v3", credentials=creds)
            service_sheets = build('sheets', 'v4', credentials=creds)

            # Call the Sheets API
            results = service.files().list(q= "mimeType='application/vnd.google-apps.spreadsheet'").execute()
            items = results.get("files", [])

            if not items:
                print('No files found.')

            for item in items:
                list_sheets.append({"spreadsheets" : item["name"], "id" : item["id"]})
        
        return Response(status=200, data=list_sheets)

    
    def store_lead(self):
        external = ExternalService()
        channel_code='65ecec50-ed9a-45a6-b72e-40d707eae506'
        list_lead = self.get()

        for l in list_lead:
            e = external.post_lead(channel_code=channel_code, data_lead=l)
            print(e)

class GetIdSheets(APIView, BaseParameterMixin):
    
    def get(self, request, pk):
        wsh = self.get_wsheets()
        prow = self.get_prow()
        email= self.get_email()

        res = {}
        try:
            tokene = SheetsAccounts.objects.filter(email=email).values('token', 'refresh_token')
            if(list(tokene) != []):
                a = ExternalService().cek_token(token=str(list(tokene)[0]['token']))
                print(a)

                creds = self.credentials_from_dict(tokens=list(tokene)[0]['token'], ref=list(tokene)[0]['refresh_token'])
                service_sheets = build('sheets', 'v4', credentials=creds)
                # Call the Sheets API
                wsheets = str(wsh)
                rows = service_sheets.spreadsheets().values().get(spreadsheetId=str(pk), range= wsheets+"!A1:Z").execute().get('values', [])
                
                # print(f"{len(rows)} rows retrieved")
                row1 = rows[int(prow)]
                res.update(dict(zip(rows[0], row1)))

        except HttpError as err:
            print(err)

        return Response(status=200, data=res)

class TestTrigger(APIView, BaseParameterMixin):

    def col_to_letter(self, col):
        '''Gets the letter of a column number'''
        r = ''
        while col > 0:
            v = (col - 1) % 26
            r = chr(v + 65) + r
            col = (col - v - 1) // 26
        
        # ini yang difungsi
        # result = service_sheets.spreadsheets().values().get(spreadsheetId=ssid, range=wsheets+"!A1:Z").execute()
        # values = result.get('values', [[]])[int(prow)]
        # print(values)
        # # Generate the headers mapping
        # headers = {}
        # for i, value in enumerate(values, start=1):
        #     if value is not None and value != '':
        #         headers['col#'+ str(self.col_to_letter(i))] = value

        return r

    def get(self, request):
        account_id= self.get_account_id()
        ssid = self.get_sheetsId()
        wsh = self.get_wsheets()
        prow = self.get_prow()
        email= self.get_email()
        
        res = {}
        try:
            tokene = SheetsAccounts.objects.filter(email=email, accountId = account_id).values('token', 'refresh_token')
            if(list(tokene) != []):

                creds = self.credentials_from_dict(tokens=list(tokene)[0]['token'], ref=list(tokene)[0]['refresh_token'])
                service_sheets = build('sheets', 'v4', credentials=creds)
                # Call the Sheets API
                wsheets = str(wsh)
                rows = service_sheets.spreadsheets().values().get(spreadsheetId=ssid, range= wsheets+"!A1:Z").execute().get('values', [])
                
                # print(f"{len(rows)} rows retrieved")
                row1 = rows[int(prow)]
                res.update(dict(zip(rows[0], row1)))

        except HttpError as err:
            print(err)

        return Response(status=200, data=res)


class GetWorkSheets(APIView, BaseParameterMixin):
    
    def get(self, request, pk):
        account_id= self.get_account_id()
        email= self.get_email()

        try:
            # Call the Sheets API
            list_data = []
            tokene = SheetsAccounts.objects.filter(email=email, accountId = account_id).values('token', 'refresh_token')

            if(list(tokene) != []):
                a = ExternalService().cek_token(token=str(list(tokene)[0]['token']))
                print(a)

                creds = self.credentials_from_dict(tokens=list(tokene)[0]['token'], ref=list(tokene)[0]['refresh_token'])
                service_sheets = build('sheets', 'v4', credentials=creds)
                service = service_sheets.spreadsheets().get(spreadsheetId=str(pk), fields="sheets.properties").execute().get('sheets', [])
            
                for r in service:
                    dic = {}
                    dic.update({'worksheetId' : r['properties']['sheetId'], 'worksheetName' : r['properties']['title']})
                    list_data.append(dic)
        
        except HttpError as err:
            print(err)

        return Response(status=200, data=list_data)

class GetWorkSheetsListRow(APIView, BaseParameterMixin):
    
    def get(self, request, pk):
        account_id=self.get_account_id()
        wsh = self.get_wsheets()
        email= self.get_email()

        res = []
        try:
            # Call the Sheets API
            tokene = SheetsAccounts.objects.filter(email=email, accountId = account_id).values('token', 'refresh_token')

            if(list(tokene) != []):
                a = ExternalService().cek_token(token=str(list(tokene)[0]['token']))

                creds = self.credentials_from_dict(tokens=list(tokene)[0]['token'], ref=list(tokene)[0]['refresh_token'])
                service_sheets = build('sheets', 'v4', credentials=creds)
                wsheets = str(wsh)
                rows = service_sheets.spreadsheets().values().get(spreadsheetId=str(pk), range= wsheets+"!A1:Z").execute().get('values', [])
                total = len(rows)
                for i in range(total)[1:]:
                    res.append({"Rows":"SpreadSheet Row " + f"{i}"})
        
        # finally:
        #     flow.close()
        except HttpError as err:
            print(err)

        return Response(status=200, data=res)

class GetChannels(BaseParameterMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    
    # serializer_class = getChannelSerializer

    def get(self, request):
        account_id = self.get_account_id()
        # self.queryset = SheetsAds.objects.filter(accountId=account_id)

        return self.list(request)                   
