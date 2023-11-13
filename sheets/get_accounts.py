from requests import request
from sheets.callback import Callback
from sheets.models import SheetsAccounts
from sheets.serializers import SheetsAccountsSerializer
from sheets.services import BaseParameterMixin
from rest_framework.views import APIView
import os.path
from rest_framework.response import Response
from django.http.response import HttpResponse
from sheets.services import BaseParameterMixin, ExternalService
from rest_framework import mixins, generics
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from django.db.models import Q

class GetAccounts(BaseParameterMixin, mixins.ListModelMixin,
                    mixins.CreateModelMixin, 
                    generics.GenericAPIView):

    queryset = SheetsAccounts.objects.all()
    serializer_class = SheetsAccountsSerializer

    def get(self, request):
        account_id = self.get_account_id()
        invoker_id = self.get_user_id()
        self.queryset = SheetsAccounts.objects.filter(Q(accountId = account_id) | Q(accountId = None))

        if (SheetsAccounts.objects.filter(accountId = None).count() > 0):
            print('update')
            SheetsAccounts.objects.filter(accountId = None).update(accountId=account_id)

        return self.list(request)

class GetRettrieveAccounts(BaseParameterMixin,
                    mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.DestroyModelMixin, 
                    generics.GenericAPIView):

    def get_queryset(self):
        account_id = self.get_account_id()
        
        queryset = SheetsAccounts.objects.all()
        return queryset
    
    serializer_class = SheetsAccountsSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)
    
    def delete(self, request, pk):
        self.destroy(request, pk)
        response = "success delete id "+str(pk)
        return HttpResponse(json.dumps(response, ensure_ascii=False), content_type="application/json")

class GetConnectAccounts(APIView, BaseParameterMixin):
    
    def get(self, request):
        print(Callback().auth_url())
        url = Callback().auth_url()

        res = {'url' : url}

        return Response(status=200, data=res)