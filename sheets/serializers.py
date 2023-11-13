from os import dup
from django.db.models.base import Model

from sheets.models import ColumnAds, FilterSetup, LogLeads, SheetsAccounts, SheetsAds, FilterMaster
from .services import ExternalService
from django.db.models import fields
from rest_framework import serializers
import json

class SheetsAdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SheetsAds
        fields = '__all__'

class SheetsAccountsSerializer(serializers.ModelSerializer):
    totalIntegration = serializers.SerializerMethodField('get_status')

    def get_status(self, id):
        queryset = SheetsAds.objects.filter(accountId=id.accountId).count()
        return queryset

    class Meta:
        model = SheetsAccounts
        fields = '__all__'

class AdsIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = SheetsAds
        fields = ['id', 'name']

class ColumnIdSerializer(serializers.ModelSerializer):
    text = serializers.CharField()

    class Meta:
        model = ColumnAds
        fields = ['name', 'text']

class FilterAdsIdSerializer(serializers.ModelSerializer):
    filter = serializers.CharField()

    class Meta:
        model = FilterSetup
        fields = ['column', 'filter', 'text']

class SheetsAdsIdSerializer(serializers.ModelSerializer):
    column = serializers.SerializerMethodField('get_column')
    filter = serializers.SerializerMethodField('get_filter')

    def get_column(self, id):
        queryset = ColumnAds.objects.filter(adsId=id)
        field_serializer = ColumnIdSerializer(queryset, many=True)
        return field_serializer.data
    
    def get_filter(self, id):
        queryset = FilterSetup.objects.filter(adsId=id)
        field_serializer = FilterAdsIdSerializer(queryset, many=True)
        return field_serializer.data

    class Meta:
        model = SheetsAds
        fields = '__all__'
    
class SheetsSummarySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SheetsAds
        fields = '__all__'

class FilterMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterMaster
        fields = ['id', 'name']

class LogSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField('get_log')
    notes = serializers.SerializerMethodField('get_notes')
    # channel = serializers.SerializerMethodField('get_channel')
    # project = serializers.SerializerMethodField('get_project')

    def get_log(self, obj):
        log = obj.log
        if obj.log == None and obj.success == True :
            log = 'success'
        else : 
            log = 'stopped'

        return log
    
    def get_project(self, obj):
        projects = SheetsAds.objects.filter(id=obj.adsId_id).values_list('projectId','projectName')

        if projects != None :
            log = {
                'id':projects[0][0],
                'name':projects[0][1],

            }

        return log
    
    def get_channel(self, obj):
        projects = SheetsAds.objects.filter(id=obj.adsId_id).values_list('channelId','channelName')

        if projects != None :
            log = {
                'id':projects[0][0],
                'name':projects[0][1],

            }

        return log
    
    def get_notes(self, obj):
        log = obj.log
        if obj.log == None and obj.success == True :
            log = '-'
        else : 
            if log != None :
                valid_json = log.replace("\'", "\"")
                my_dict = json.loads(valid_json)
                if my_dict.get('messageDetail') != None :
                    log = my_dict['messageDetail'][0]
                elif my_dict.get('message') != None :
                    log = my_dict['message']
                else :
                    log = None

        return log

    class Meta:
        model = LogLeads
        fields = ['id', 'createdAt', 'success', 'row', 'status', 'notes', 'skip', 'adsId', 'adsName', 'lead_name']

class LogIdSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField('get_log')
    notes = serializers.SerializerMethodField('get_notes')
    ads = serializers.SerializerMethodField('get_ads')
    lead = serializers.SerializerMethodField('get_lead')
    
    def get_log(self, obj):
        log = obj.log
        if obj.log == None and obj.success == True :
            log = 'success'
        else : 
            log = 'stopped'

        return log
    
    def get_notes(self, obj):
        log = obj.log
        if obj.log == None and obj.success == True :
            log = '-'
        else : 
            if log != None :
                valid_json = log.replace("\'", "\"")
                my_dict = json.loads(valid_json)
                if my_dict.get('messageDetail') != None :
                    log = my_dict['messageDetail'][0]
                elif my_dict.get('message') != None :
                    log = my_dict['message']
                else :
                    log = None

        return log

    def get_ads(self, obj):
        ids = LogLeads.objects.filter(id=obj.id).values_list('adsId', flat=True)
        acc = {
            'id': ids[0],
            'name': str(obj.adsName)
        }

        return acc
    
    def get_lead(self, obj):
        ids = LogLeads.objects.filter(id=obj.id).values('lead_name', 'lead_phone', 'lead_email', 'lead_notes')
        acc = {}
        acc.update(ids[0])

        id = LogLeads.objects.filter(id=obj.id).values_list('adsId', flat=True)
        spr = SheetsAds.objects.filter(id=id[0]).values('spreadsheet_name', 'worksheet_name')
        acc.update({
            'spreadsheet': spr[0]['spreadsheet_name'],
            'worksheet' : spr[0]['worksheet_name']
        })
        return acc
    
    class Meta:
        model = LogLeads
        fields = ['id', 'createdAt', 'success', 'row', 'status', 'notes', 'skip', 'ads', 'lead']

class SheetsAdsProjectSer(serializers.ModelSerializer):

    class Meta:
        model = SheetsAds
        fields = '__all__'