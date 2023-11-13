import requests
import json
from django.conf import settings
import os
from django.db import connection
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from rest_framework.response import Response
import logging
from sheets.models import SheetsAccounts

class BaseParameterMixin():
    def get_account_id(self):
        account_id = self.request.GET.get('account_id')
        return account_id
    
    def get_user_id(self):
        user_id = self.request.GET.get('user_id')
        return user_id
    
    def get_invoker_role(self):
        invoker_role = self.request.GET.get('invoker_role')
        return invoker_role
    
    def get_since(self):
        since = self.request.GET.get('since')
        return since
    
    def get_until(self):
        until = self.request.GET.get('until')
        return until
    
    def get_additional(self):
        additional = self.request.GET.get('without_additional_information')
        return additional
    
    def get_sheetsId(self):
        archive = self.request.GET.get('sheet_id')
        return archive
    
    def get_wsheets(self):
        archive = self.request.GET.get('worksheet')
        return archive

    def get_prow(self):
        archive = self.request.GET.get('row')
        return archive

    def get_code(self):
        user_id = self.request.GET.get('code')
        return user_id
    
    def get_email(self):
        user_id = self.request.GET.get('email')
        return user_id
    
    def get_head(self):
        user_id = self.request.GET.get('head')
        return user_id

    def get_adsid(self):
        id = self.request.GET.get('ads_id')
        return id

    def get_project(self):
        search = self.request.GET.get('project_id')
        return search 

    def get_campaign(self):
        search = self.request.GET.get('campaign_id')
        return search
    
    def get_channel(self):
        search = self.request.GET.get('channel_id')
        return search
    
    def get_search(self):
        search = self.request.GET.get('search')
        return search

    def get_size(self):
        until = self.request.GET.get('size')
        return until
    
    def get_skip(self):
        until = self.request.GET.get('skip')
        return until
    
    def filter_date(self):
        since = self.get_since()
        until = self.get_until()

        filterd = {}
        if(since != None and until != None):
            # filterd = {"createdAt__range": [str(since), str(until)]}
            filterd = {"createdAt__date__gte" : str(since), "createdAt__date__lte" : str(until)}

        return filterd
    
    def filter_channel(self):
        channel = self.get_channel()
        if(channel != None):
            channel = [int(x) for x in self.request.GET.get('channel_id', '').split(',')]

        filter_ch = {}
        if(channel != None):
            filter_ch = {"adsId__channelId__in": channel}
        
        return filter_ch
    
    def filter_project(self):
        channel = self.get_project()
        if(channel != None):
            channel = [int(x) for x in self.request.GET.get('project_id', '').split(',')]

        filter_ch = {}
        if(channel != None):
            filter_ch = {"adsId__projectId__in": channel}
        
        return filter_ch
    
    def filter_ads_id(self):
        ads = self.get_adsid()

        if(ads != None):
            ads = [int(x) for x in self.request.GET.get('ads_id', '').split(',')]

        filter_ch = {}
        if(ads != None):
            filter_ch = {"adsId_id__in": ads}
        
        return filter_ch
    
    def page_limit(self, size, skip):
        # MyModel.objects.all()[OFFSET:OFFSET+LIMIT]
        total_limit = int(size) + int(skip)

        return total_limit
    
    def get_credentials_as_dict(tokens, refresh_token) -> dict:
        credentials_as_dict = {

            "token": tokens,

            "refresh_token": refresh_token,

            "token_uri": "https://oauth2.googleapis.com/token",

            "client_id": "92987046251-pakorolv7it32732fi1miqbh9fr4kgov.apps.googleusercontent.com",

            "client_secret": "OCSPX-S8-MBvmOkGU_aMmi8V7tfrKuWjwP",

            "scopes": ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/drive.readonly", "https://www.googleapis.com/auth/spreadsheets.readonly"]

        }

        return credentials_as_dict

    def service_google_api(self):
        email = self.get_email()
        tokene = SheetsAccounts.objects.filter(email=email).values('token', 'refresh_token', flat=True)
        creds = self.get_credentials_as_dict(tokens=list(tokene)[0]['token'], refresh_token=list(tokene)[0]['refresh_token'])
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                creds = creds

        service_sheets = build('sheets', 'v4', credentials=creds)

        return service_sheets

    
    def credentials_from_dict(credentials_dict: dict, tokens, ref) -> Credentials:
        base_url_client_id = os.environ.get('CLIENT_ID')
        base_url_clientt_secret = os.environ.get('CLIENT_SECRET')

        creds= Credentials(

            tokens,

            refresh_token=ref,

            token_uri="https://oauth2.googleapis.com/token",

            client_id=str(base_url_client_id),

            client_secret=str(base_url_clientt_secret),

            scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/drive.readonly", "https://www.googleapis.com/auth/spreadsheets.readonly"]

        )

        return creds

    def access_auth(self, request):
        email = self.get_email()
        list_sheets = []

        creds= None
        tokene = SheetsAccounts.objects.filter(email=email).values('token', 'refresh_token')
        if(list(tokene) != []):
            creds = self.credentials_from_dict(tokens=str(list(tokene)[0]['token']), ref=list(tokene)[0]['refresh_token'])

 
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

class ExternalService():

    def __init__(self):
        return

    base_url_team = os.environ.get('TEAM_API_URL')
    base_url_project = os.environ.get('PROJECT_API_URL')
    base_url_product = os.environ.get('PRODUCT_API')
    base_url_report = os.environ.get('REPORT_API')
    base_url_core = os.environ.get('CORE_API_URL')
    base_url_lead = os.environ.get('LEAD_API_URL')

    def get_user_by_account_id(self, account_id):
        url = self.base_url_core+"users?account_id="+str(account_id)
        response = requests.request("GET", url)
        if(response.status_code == 200):
            team = json.loads(response.text)
            return team
        else:
            return None

    def get_project_by_account_id(self, account_id):
        url = self.base_url_project+"minimal/project?account_id="+str(account_id)
        response = requests.request("GET", url)
        if(response.status_code == 200):
            team = json.loads(response.text)
            return team
        else:
            return None
    
    def get_campaign_by_account_id(self, account_id):
        url = self.base_url_project+"rest/campaigns?account_id="+str(account_id)
        response = requests.request("GET", url)
        if(response.status_code == 200):
            team = json.loads(response.text)
            return team
        else:
            return None

    def get_channel_by_account_id(self, account_id):
        url = self.base_url_project+"rest/channels?account_id="+str(account_id)+"&without_additional_information=true"

        response = requests.request("GET", url)
        if(response.status_code == 200):
            team = json.loads(response.text)
            return team
        else:
            return None
    
    def get_user_info(self, token):
        url = 'https://www.googleapis.com/oauth2/v2/userinfo?alt=json&access_token='+token
        response = requests.request("GET", url)
        if(response.status_code == 200):
            team = json.loads(response.text)
            return team
        else:
            return None
    
    def cek_token(self, token):
        url = 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token='+token
        response = requests.request("GET", url)

        return response.status_code

    
    def get_project_id(self, account_id, projectId):
        url = self.base_url_project+"rest/projects/"+ str(projectId) +"?account_id="+str(account_id)
        response = requests.request("GET", url)
        if(response.status_code == 200):
            team = json.loads(response.text)
            if(team != None) :
                return team['name']
        else:
            return None
    
    def get_project_status(self, account_id, project_id):
        url = self.base_url_project+"rest/projects/"+str(project_id)+"/statuses?account_id="+str(account_id)
        response = requests.request("GET", url)
        if(response.status_code == 200):
            return json.loads(response.text)
        else:
            return None
    
    def get_project_channel(self, account_id, channel_id):
        url = self.base_url_project+"rest/channels/"+str(channel_id)+"?account_id="+str(account_id)
        response = requests.request("GET", url)
        if(response.status_code == 200):
            return json.loads(response.text)
        else:
            return None

    def get_lead_list(self, accountId, invokerId, since, until):
        url = self.base_url_lead+"leads?account_id="+str(accountId)+"&invoker_id="+str(invokerId)

        if(since !=None and until != None):
            since = json.dumps(since)
            until = json.dumps(until)
            filters =  '(filters: {createdAt: {since: " + since +", until: " + until + "}})'
        else:
            filters = ''

        data = {"query": "query {getLeadList"+filters+" {id name phone note channel{channelId channel} log{createdAt modifiedAt} owner{user userId} status{status}}}"}

        response = requests.request("POST", url = url, json=data, headers={ 'Content-Type': 'application/json','Accept': 'application/json',})

        if(response.status_code == 200):
            jsons = json.loads(response.text)
            res = jsons['data']['getLeadList']
            return res
        else:
            return None
    
    def follow_up_lead(self, accountId, invokerId, lead_id, status_id, note):
        url = self.base_url_lead+"leads?account_id="+str(accountId)+"&invoker_id="+str(invokerId)

        data = {"query": "mutation {followupLead(id: \""+lead_id+"\", data: {statusId: "+str(status_id)+" note: \" "+note+"\"  } ) {id }}"}

        response = requests.request("POST", url = url, json=data, headers={ 'Content-Type': 'application/json','Accept': 'application/json',})
        print(response.status_code)
        if(response.status_code == 200):
            jsons = json.loads(response.text)
            return jsons
        else:
            return None
    
    def distribute_lead(self, accountId, invokerId, lead_id, status_id, user_id, channel_id, note):
        url = self.base_url_lead+"leads?account_id="+str(accountId)+"&invoker_id="+str(invokerId)
        
        data = {"query": "mutation {followupLead(id: \""+lead_id+"\" , data: {statusId: "+str(status_id)+" note: \" "+note+"\"  } ) {id} distributeLead(data: {userIds:"+str(user_id)+" channelId: "+str(channel_id)+" leadIds: \""+lead_id+"\"} ) {id}}"}
        # print(data)
        response = requests.request("POST", url = url, json=data, headers={ 'Content-Type': 'application/json','Accept': 'application/json',})
        # print(json.loads(response.text))
        if(response.status_code == 200):
            jsons = json.loads(response.text)
            return jsons
        else:
            return None
    
    def post_lead(self, channel_code, data_lead):
        url = self.base_url_lead+"public/submit_external_lead?code="+str(channel_code)

        data = data_lead
        response = requests.request("POST", url = url, json=data, headers={ 'Content-Type': 'application/json','Accept': 'application/json',})
        # print(json.loads(response.text))
        logger = logging.getLogger(__name__)

        if(response.status_code == 200):
            jsons = json.loads(response.text)
            return response
        else:
            logger.error(url +" => " + str(response.status_code) + str(response.text))
            return response
    
    def get_channel_by_id(self, account_id, channel_id):
        url = self.base_url_project+"rest/channels/"+str(channel_id)+"?account_id="+str(account_id)
        logger = logging.getLogger(__name__)
        logger.error(url)
        response = requests.request("GET", url)
        if(response.status_code == 200):
            team = json.loads(response.text)
            return team
        else:
            return None
    
    def patch_lead(self, account_id, sheetid, ws, email, row):
        url = "http://54.251.71.7:8021/test_trigger?sheet_id="+str(sheetid)+"&worksheet="+str(ws)+"&row="+str(row)+"&email="+str(email)+"&account_id="+str(account_id)

        response = requests.request("GET", url)
        if(response.status_code == 200):
            team = json.loads(response.text)
            return team
        else:
            return None