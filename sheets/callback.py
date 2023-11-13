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
from rest_framework.renderers import TemplateHTMLRenderer

class Callback(APIView, BaseParameterMixin):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'response.html'

    def get(self, request):
        account_id = self.get_account_id()
        SCOPES = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/drive.readonly", "https://www.googleapis.com/auth/spreadsheets.readonly"]
        creds = None
        base_url_redirect = os.environ.get('REDIRECT_URI')

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
                flow = Flow.from_client_secrets_file('sheets/client_jala.json', SCOPES, redirect_uri=str(base_url_redirect))

                # Tell the user to go to the authorization URL.
                auth_url, state = flow.authorization_url(prompt='consent', access_type='offline', include_granted_scopes='true')
                if(self.get_code() != None) :
                    flow.fetch_token(code=self.get_code())
                    creds = flow.credentials
                    # inni nyimpen token sama email user ke tabel akun
                    emaile = ExternalService().get_user_info(token=creds.token)
                    new_akun = SheetsAccounts(
                            email = emaile['email'],
                            token = creds.token,
                            refresh_token = creds.refresh_token,
                            # accountId=account_id
                        )
                    new_akun.save()

                else :
                    return Response(template_name='response.html')

        return Response(template_name='response.html')
    
    def create_keyfile_dict(self):
        base_url_redirect = os.environ.get('REDIRECT_URI')
        base_url_client_id = os.environ.get('CLIENT_ID')
        base_url_clientt_secret = os.environ.get('CLIENT_SECRET')
        base_url_project_id = os.environ.get('PROJECT_ID')

        var = {
            "web": {
                "client_id":base_url_client_id,
                "project_id":base_url_project_id,
                "auth_uri":"https://accounts.google.com/o/oauth2/auth",
                "token_uri":"https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
                "client_secret":base_url_clientt_secret,
                "redirect_uris":base_url_redirect
                }
            }

        return var
        
    def auth_url(self):

        SCOPES = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/drive.readonly", "https://www.googleapis.com/auth/spreadsheets.readonly"]
        creds = None
        base_url_redirect = os.environ.get('REDIRECT_URI')

        with open('sheets/client_jala.json', 'w') as convert_file:
            convert_file.write(json.dumps(self.create_keyfile_dict()))

        if os.path.exists('token.json'):
            with open('token.json', 'rb') as token:

                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        url = ''
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Create the flow using the client secrets file from the Google API
                # Console.
                os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
                flow = Flow.from_client_secrets_file('sheets/client_jala.json', SCOPES, redirect_uri=str(base_url_redirect))

                # Tell the user to go to the authorization URL.
                auth_url, state = flow.authorization_url(prompt='consent', access_type='offline', include_granted_scopes='true')
                url = str(auth_url)

        return url