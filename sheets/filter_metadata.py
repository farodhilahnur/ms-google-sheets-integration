from sheets.services import BaseParameterMixin
from sheets.utils import succ_resp
from .serializers import FilterMasterSerializer, SheetsAdsProjectSer
from .models import FilterMaster, SheetsAds
from rest_framework import mixins, generics
from rest_framework.views import APIView
from rest_framework.response import Response


class FilterMetadata(mixins.ListModelMixin,
                    mixins.CreateModelMixin, 
                    generics.GenericAPIView
                    ):
    queryset = FilterMaster.objects.all()
    serializer_class = FilterMasterSerializer

    def get(self, request):
        return self.list(request)

class AdsListMetadataView(APIView, BaseParameterMixin):
    def get(self, request):
        account_id = self.get_account_id()
        filter = self.request.GET.get('filter')

        pproject = SheetsAds.objects.filter(accountId=account_id).distinct('projectId').extra(
        select={
            'id': 'project_id',
            'name': 'project_name'
        }).values('id', 'name')

        channel = SheetsAds.objects.filter(accountId=account_id).distinct('channelId').extra(
        select={
            'id': 'channel_id',
            'name': 'channel_name'
        }).values('id', 'name')

        res = {}

        if(filter == 'projects'):
            res = pproject
        elif(filter =='channels'):
            res = channel
        else :
            res.update({'projects': pproject})
            res.update({'channel': channel})
        
        return Response(status=200, data=res)