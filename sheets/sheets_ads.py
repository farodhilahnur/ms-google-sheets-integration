from django.http.response import HttpResponse
from rest_framework import mixins, generics
import rest_framework
import json
from django.db import transaction, IntegrityError
from sheets.get_sheets import GetSheets
from sheets.models import ColumnAds, FilterSetup, LogLeads, SheetsAds
from sheets.serializers import LogIdSerializer, LogSerializer, SheetsAdsIdSerializer, SheetsAdsSerializer
from .utils import invalid_handler, succ_resp
from django.db.models import Q
from django.utils import timezone
import re

from sheets.services import BaseParameterMixin, ExternalService

class AdsListCreateView(BaseParameterMixin,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    
    serializer_class = SheetsAdsSerializer

    def get(self, request):
        account_id = self.get_account_id()
        self.queryset = SheetsAds.objects.filter(accountId=account_id).order_by('-createdAt')
        kosong = SheetsAds.objects.filter(Q(channelName= None) | Q(campaignName=None) | Q(projectName=None) | Q(channelCode=None), accountId=account_id).values_list('channelId', flat=True).order_by('-createdAt')
        
        if(list(kosong) != []) :
            for a in list(kosong):
                channellist = ExternalService().get_channel_by_account_id(account_id=account_id)

                name = next((x for x in channellist if x['id'] == a), 0)
                if(name != 0):
                    SheetsAds.objects.filter(accountId=account_id, channelId=a).update(channelName = name['name'], channelCode = name['uniqueCode'], campaignId = name['campaign']['id'], campaignName = name['campaign']['name'], projectId= name['campaign']['project']['id'], projectName= name['campaign']['project']['name'])

        return self.list(request)
    
    @transaction.atomic
    def post(self, request):
        account_id = self.get_account_id()
        user_id = self.get_user_id()

        temp_data = request.data
        for temp in temp_data:
            name = temp.get("name")
            # head = temp.get("head")
            ssId = temp.get("spreadsheet")['id']
            worksName = temp.get("worksheet")["name"]
            worksId = temp.get("worksheet")["id"]
            account_sheet = temp.get("account_sheet")
            channelId = temp.get("channel")["id"]
            formId = temp.get("channel")["form"]
            lastrow = temp.get("lastrow")

            channelid = ExternalService().get_channel_by_id(account_id=account_id, channel_id=channelId)
            print(channelid)
            code = None
            chname = None
            caid = None
            caname = None
            pid = None
            pname = None
            if(channelid != None):
                code = channelid['uniqueCode']
                chname=channelid['name'],
                caid = channelid['campaign']['id'],
                caname =channelid['campaign']['name'],
                pid = channelid['campaign']['project']['id']
                pname = channelid['campaign']['project']['name']

            if lastrow != None : 
                lastrow = [int(s) for s in lastrow.split() if s.isdigit()]

                new_ads = SheetsAds(
                    name = name,
                    spreadsheetId = ssId,
                    worksheetId = worksId,
                    worksheet_name = worksName,
                    account_sheet = account_sheet,
                    channelId = channelId,
                    formId = formId,
                    accountId = account_id,
                    createdBy = user_id,
                    channelCode = code,
                    channelName=chname[0],
                    campaignId = caid[0],
                    campaignName = caname[0],
                    projectId = pid,
                    projectName = pname,
                    lastrow=lastrow[0]
                )
                message = "error"
            else :
                new_ads = SheetsAds(
                    name = name,
                    spreadsheetId = ssId,
                    worksheetId = worksId,
                    worksheet_name = worksName,
                    account_sheet = account_sheet,
                    channelId = channelId,
                    formId = formId,
                    accountId = account_id,
                    createdBy = user_id,
                    channelCode = code,
                    channelName=chname[0],
                    campaignId = caid[0],
                    campaignName = caname[0],
                    projectId = pid,
                    projectName = pname
                )

            try:
                new_ads.save()

                column = temp.get("column")
                if(column != None) :
                
                    for c in column:
                        cname = c.get("name")
                        text = c.get("text")
                        new_column_ads = ColumnAds(
                            adsId_id = new_ads.id,
                            name = cname,
                            text = text,
                            accountId = account_id,
                            createdBy = user_id
                        )
                        new_column_ads.save()

                filter = temp.get("filter")
                if(filter != None) :
                    if(filter != []) :
                        SheetsAds.objects.filter(id=new_ads.id).update(isFilter=True)
                        for f in filter:
                            fcolumn = f.get("column")
                            ffilter = f.get("filter")
                            ftext = f.get("text")
                            new_filter = FilterSetup(
                                adsId_id = new_ads.id,
                                column=fcolumn,
                                filter=ffilter,
                                text = ftext,
                                accountId = account_id,
                                createdBy = user_id
                            )
                            new_filter.save()
                
                if lastrow != None : 
                    new_logs = LogLeads(
                            adsId_id = new_ads.id,
                            lead_phone = None,
                            success = True,
                            row = lastrow[0],
                        )
                    new_logs.save()

            except IntegrityError:
                return HttpResponse(json.dumps(invalid_handler(message), ensure_ascii=False), content_type="application/json", status=rest_framework.status.HTTP_400_BAD_REQUEST)   
 
        self.queryset = SheetsAds.objects.filter(accountId=account_id)

        return self.list(request)

class AdsRetrieveCreateView(BaseParameterMixin,
                    mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.DestroyModelMixin, 
                    generics.GenericAPIView):

    def get_queryset(self):
        account_id = self.get_account_id()
        
        queryset = SheetsAds.objects.filter(accountId=account_id)
        return queryset
    
    serializer_class = SheetsAdsIdSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

    @transaction.atomic
    def put(self, request, pk):
        account_id = self.get_account_id()
        user_id = self.get_user_id()
        temp = request.data
        
        status =  temp.get("status")
        name = temp.get("name")
        account_sheet = temp.get("account_sheet")

        if(temp.get("channel") != None):
            channelId = temp.get("channel")["id"]
            formId = temp.get("channel")["form"]

            # update campaign n project
            channellist = ExternalService().get_channel_by_account_id(account_id=account_id)
            name = next((x for x in channellist if x['id'] == channelId), 0)

            if(name != 0):
                SheetsAds.objects.filter(id=pk).update(channelCode= name['uniqueCode'], channelName = name['name'], campaignId = name['campaign']['id'], campaignName = name['campaign']['name'], projectId= name['campaign']['project']['id'], projectName= name['campaign']['project']['name'])

            SheetsAds.objects.filter(id=pk).update(channelId=channelId, formId=formId)
        
        if(temp.get("spreadsheet") != None):
            ssId = temp.get("spreadsheet")['id']
            SheetsAds.objects.filter(id=pk).update(spreadsheetId=ssId)
        
        if(temp.get("worksheet") != None):
            worksId = temp.get("worksheet")["id"]
            worksname = temp.get("worksheet")["name"]
            SheetsAds.objects.filter(id=pk).update(worksheetId=worksId, worksheet_name=worksname)
        
        column = temp.get("column")
        if(column != None) :
            columnlist = ColumnAds.objects.filter(adsId=pk)
            newcol = []

            for c in column:
                cname = c.get("name")
                text = c.get("text")
                newcol.append(c.get("name"))
                ColumnAds.objects.filter(adsId=pk, name=cname).update(text=text)

                if(cname not in list(columnlist.values_list('name', flat=True))):
                    new_column_ads = ColumnAds(
                        adsId_id = pk,
                        name = cname,
                        text = text,
                        accountId = account_id,
                        createdBy = user_id
                    )
                    new_column_ads.save()

            for a in columnlist :
                if a.name not in newcol:
                    a.delete()
        
        filter = temp.get("filter")
        if(column != None) :
            columnlist = FilterSetup.objects.filter(adsId=pk).values('column', "filter", "text", "adsId")
            
            for f in filter:
                fcolumn = f.get("column")
                ffilter = f.get("filter")
                ftext = f.get("text")
                f.update({"adsId" : pk})
                
                if f not in list(columnlist):
                    new_filter = FilterSetup(
                        adsId_id = pk,
                        column=fcolumn,
                        filter=ffilter,
                        text = ftext,
                        accountId = account_id,
                        createdBy = user_id
                    )
                    new_filter.save()
            
            for b in list(columnlist) :
                if b not in filter:
                    FilterSetup.objects.filter(adsId=pk, column=b['column'], filter=b['filter'], text=b['text']).delete()

        status_now = SheetsAds.objects.filter(id=pk).values_list('status', flat=True)

        if(status_now[0] == 'running'):
            if(status == 'stop' or status == 'hold'):
                SheetsAds.objects.filter(id=pk).update(end_date = timezone.now())
        else:
            if(status == 'running'):
                SheetsAds.objects.filter(id=pk).update(end_date = None)

        return self.update(request, pk)
    
    def delete(self, request, pk):
        self.destroy(request, pk)
        response = "success delete id "+str(pk)
        return HttpResponse(json.dumps(response, ensure_ascii=False), content_type="application/json")

class AdsListHistoryView(BaseParameterMixin,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    
    serializer_class = LogSerializer

    def get(self, request):
        account_id = self.get_account_id()
        filter_date = self.filter_date()
        filter_project = self.filter_project()
        filter_channel = self.filter_channel()
        filter_ads_id = self.filter_ads_id()
        size = self.get_size()
        skip = self.get_skip()

        if(size != None):
            if(skip != None) :
                size = self.page_limit(size=size, skip=skip)
                skip = int(skip)
            else :
                size = self.page_limit(size=size, skip=0)
                skip = None
        else :
            skip = None
            size = None
        size = 300
        self.queryset = LogLeads.objects.filter(adsId__accountId=account_id, **filter_date, **filter_project, **filter_channel, **filter_ads_id).exclude(row=1).order_by('-id')[skip:size]

        serializer = LogSerializer(self.queryset, many=True)
        projects = SheetsAds.objects.filter(accountId=account_id).values_list('id', 'projectId','projectName', 'channelId','channelName')

        if(serializer.data != None):
            for s in serializer.data :
                s.update({'ads' : {
                    'id': s['adsId'],
                    'name': s['adsName']
                }})
                pname = next((x for x in projects if x[0] == s['adsId']), 0)
                if pname != 0 :
                    s.update({
                        'project': {
                            'id': projects[0][1],
                            'name': projects[0][2]
                        },
                        'channel': {
                            'id': projects[0][3],
                            'name': projects[0][4]
                        }
                    })
                else :
                    s.update({
                        'project': {
                            'id': None,
                            'name': None
                        },
                        'channel': {
                            'id': None,
                            'name': None
                        }
                    })

        return succ_resp(data=serializer.data)

class AdsListHistoryIdView(BaseParameterMixin,
                    mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.DestroyModelMixin, 
                    generics.GenericAPIView):

    def get_queryset(self):
        account_id = self.get_account_id()
        
        queryset = LogLeads.objects.all()
        return queryset
    
    serializer_class = LogIdSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)