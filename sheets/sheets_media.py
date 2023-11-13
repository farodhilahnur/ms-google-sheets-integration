from rest_framework.views import APIView
from rest_framework.response import Response
import json

from sheets.models import LogLeads, SheetsAds

class SheetSummaryCreateView(APIView):
    
    def get(self, request):
        account_id = self.request.GET.get('account_id')
        list_gsheet = SheetsAds.objects.filter(accountId=account_id).values_list('id', flat=True)
        total_channel = SheetsAds.objects.filter(accountId=account_id).distinct('channelId').count()
        total_lead = LogLeads.objects.filter(adsId__in = list(list_gsheet)).distinct('row').count()
        res = {
            'media' : "Google Sheet",
            'total_channel' : total_channel,
            'total_lead': total_lead
            }
        return Response(status=200, data=res)
