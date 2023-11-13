from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2client.service_account import ServiceAccountCredentials
from sheets.models import SheetsAccounts
from sheets.services import BaseParameterMixin, ExternalService
from cgitb import reset
import pickle
import json
import os.path
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

class Callback(APIView, BaseParameterMixin):

    def get(self, request):
        
        SCOPES = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/drive.readonly", "https://www.googleapis.com/auth/spreadsheets.readonly"]
        creds = None

        if os.path.exists('token.json'):
            with open('token.json', 'rb') as token:

                creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Create the flow using the client secrets file from the Google API
                # Console.
                os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
                flow = Flow.from_client_secrets_file('sheets/client_jala.json', SCOPES, redirect_uri='https://restapi.dev.jala.ai/public/google_sheet_callback')

                # Tell the user to go to the authorization URL.
                auth_url, _ = flow.authorization_url(prompt='consent', # Enable offline access so that you can refresh an access token without
                # re-prompting the user for permission. Recommended for web server apps.
                access_type='offline',
                # Enable incremental authorization. Recommended as a best practice.
                include_granted_scopes='true')

                print('Please go to this URL: {}'.format(auth_url))
                flow.fetch_token(code=self.get_code())
                creds = flow.credentials
                # inni nyimpen token sama email user ke tabel akun
                emaile = ExternalService().get_user_info(token=creds.token)
                new_akun = SheetsAccounts(
                        email = emaile['email'],
                        token = creds.token,
                    )
                new_akun.save()

            # Save the credentials for the next run
            # with open('token.json', 'w') as token:
            #     token.write(creds.to_json())

        return Response(status=200, data=creds.to_json())