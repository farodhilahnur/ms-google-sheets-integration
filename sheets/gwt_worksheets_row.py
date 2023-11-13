import os.path
import json
from pprint import pprint
from traceback import print_tb
from rest_framework.views import APIView
from rest_framework.response import Response
from sheets.services import BaseParameterMixin, ExternalService

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GetWorkSheetsRow(APIView, BaseParameterMixin):
    
    def get(self, request, pk):
        wsh = self.get_wsheets()
        prow = self.get_prow()
        service_sheets = self.service_google_api()

        try:
            
            # Call the Sheets API
            wsheets = str(wsh)
            rows = service_sheets.spreadsheets().values().get(spreadsheetId=str(pk), range= wsheets+"!A1:Z").execute().get('values', [])
            
            print(f"{len(rows)} rows retrieved")
            row1 = rows[int(prow)]
            dataas = dict(zip(rows[0], row1))

        # finally:
        #     flow.close()
        except HttpError as err:
            print(err)

        return Response(status=200, data=dataas)
