from django.urls import path
from sheets.callback import Callback
from sheets.cek_gsheet_lead import CekGsheetLeads
from sheets.filter_metadata import AdsListMetadataView, FilterMetadata
from sheets.get_accounts import GetAccounts, GetConnectAccounts, GetRettrieveAccounts
from sheets.get_last_row import GetLastRow

from sheets.get_sheets import GetChannels, GetIdSheets, GetSheets, GetWorkSheets, GetWorkSheetsListRow, TestTrigger
from sheets.gwt_worksheets_row import GetWorkSheetsRow
from sheets.sheets_ads import AdsListCreateView, AdsListHistoryIdView, AdsListHistoryView, AdsRetrieveCreateView
from sheets.sheets_media import SheetSummaryCreateView

urlpatterns = [
   path('list/accounts', GetAccounts.as_view()),
   path('list/accounts/<int:pk>', GetRettrieveAccounts.as_view()),
   path('connect/new', GetConnectAccounts.as_view()),
   path('info/sheets', GetSheets.as_view()),
   path('info/sheets/<str:pk>', GetIdSheets.as_view()),
   path('info/sheets/<str:pk>/worksheets', GetWorkSheets.as_view()),
   path('info/sheets/<str:pk>/worksheets/rows', GetWorkSheetsListRow.as_view()),
   path('test_trigger', TestTrigger.as_view()),
   path('info/sheets/last_row', GetLastRow.as_view()),
   path('info/channels', GetChannels.as_view()),
   # path('spreadsheets/<str:pk>/rows', GetWorkSheetsRow.as_view()),

   path('callback', Callback.as_view()),
   path('check_gsheet_leads', CekGsheetLeads.as_view()),

   path('google_sheet_ads', AdsListCreateView.as_view()),
   path('google_sheet_ads/<int:pk>', AdsRetrieveCreateView.as_view()),
   path('google_sheet_ads/summary', SheetSummaryCreateView.as_view()),
   path('google_sheet_ads/history', AdsListHistoryView.as_view()),
   path('google_sheet_ads/history/<int:pk>', AdsListHistoryIdView.as_view()),

   path('metadata', AdsListMetadataView.as_view()),

   path('filter/metadata', FilterMetadata.as_view()),

]
