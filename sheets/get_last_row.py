import os.path
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from sheets.services import BaseParameterMixin, ExternalService

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GetLastRow(APIView, BaseParameterMixin):
    
    def get(self, request, pk):
        SCOPES = ["https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/drive.readonly", "https://www.googleapis.com/auth/spreadsheets.readonly"]
        creds = None

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'sheets/credentials_4.json', SCOPES)
                creds = flow.run_local_server(port=2222)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service_sheets = build('sheets', 'v4', credentials=creds)
            
            # Call the Sheets API
            res = service_sheets.spreadsheets().get(spreadsheetId=str(pk), fields="sheets.properties").execute()
            rows = service_sheets.spreadsheets().values().get(spreadsheetId=str(pk), range="kesatu!A2:Z").execute().get('values', [])
            last_row = rows[-1] if rows else None
            last_row_id = len(rows)
            print(last_row_id, last_row)

        # finally:
        #     flow.close()
        except HttpError as err:
            print(err)

        return Response(status=200, data=last_row)
