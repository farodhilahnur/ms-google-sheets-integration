from django.db import models
from django.utils import timezone
import django

# Create your models here.
class SheetsAccounts(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(db_column='name', max_length=1000, blank=True, null=True, verbose_name='Name')
    email = models.CharField(db_column='email',  max_length=1000, blank=True, null=True,  verbose_name='Email')
    token = models.CharField(db_column='token',  max_length=1000, blank=True, null=True,  verbose_name='Token')
    refresh_token = models.CharField(db_column='refresh_token',  max_length=1000, blank=True, null=True,  verbose_name='Refresh Token')
    accountId = models.IntegerField(db_column='accountId', blank=True, null=True,  verbose_name='Account Id')
    createdAt = models.DateTimeField(db_column='createdAt', blank=True, null=True, default=django.utils.timezone.now, verbose_name='Created At')
    createdBy = models.IntegerField(db_column='createdBy', blank=True, null=True,  verbose_name='Created By')
    modifiedAt = models.DateTimeField(db_column='modifiedAt', blank=True, null=True,  verbose_name='Modified At')
    modifiedBy = models.IntegerField(db_column='modifiedBy', blank=True, null=True,  verbose_name='Modified By')
    status = models.CharField(db_column='status', max_length=1000, blank=True, null=True, default="connected", verbose_name='Status')
    totalIntegration = models.IntegerField(db_column='total_integration', default=0, blank=True, null=True, verbose_name='total Integration')

    class Meta:
        db_table = 'tbl_sheets_accounts'
    def save(self, *args, **kwargs):
        self.modifiedAt = timezone.now()
        return super(SheetsAccounts, self).save(*args, **kwargs)

class SheetsAds(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(db_column='name', max_length=1000, blank=True, null=True, verbose_name='Name')
    detail = models.CharField(db_column='detail',  max_length=1000, blank=True, null=True,  verbose_name='Detail')
    createdAt = models.DateTimeField(db_column='createdAt', blank=True, null=True, default=django.utils.timezone.now, verbose_name='Created At')
    end_date = models.DateTimeField(db_column='end_date', blank=True, null=True,  verbose_name='End date')
    createdBy = models.IntegerField(db_column='createdBy', blank=True, null=True,  verbose_name='Created By')
    modifiedAt = models.DateTimeField(db_column='modifiedAt', blank=True, null=True,  verbose_name='Modified At')
    modifiedBy = models.IntegerField(db_column='modifiedBy', blank=True, null=True,  verbose_name='Modified By')
    accountId = models.IntegerField(db_column='accountId', blank=True, null=True,  verbose_name='Account Id')
    account_sheet = models.CharField(db_column='account_sheet', max_length=1000, blank=True, null=True, verbose_name='Account sheets')
    adsAccId = models.ForeignKey(SheetsAccounts, db_column='adsAccId', on_delete=models.CASCADE, blank=True, null=True, related_name='adsAccId')
    status = models.CharField(db_column='status', max_length=1000, blank=True, null=True, default="running", verbose_name='Status')
    channelCode = models.CharField(db_column='channelCode', max_length=1000, blank=True, null=True, verbose_name='Channel code')
    channelId = models.IntegerField(db_column='channel_id', blank=True, null=True, verbose_name='Channel Id')
    channelName = models.CharField(db_column='channel_name', max_length=1000, blank=True, null=True, verbose_name='Channel Name')
    campaignId = models.IntegerField(db_column='campaign_id', blank=True, null=True, verbose_name='Campaign Id')
    campaignName = models.CharField(db_column='campaign_name', max_length=1000, blank=True, null=True, verbose_name='Campaign Name')
    projectId = models.IntegerField(db_column='project_id', blank=True, null=True, verbose_name='project Id')
    projectName = models.CharField(db_column='project_name', max_length=1000, blank=True, null=True, verbose_name='project Name')
    formId = models.IntegerField(db_column='form_id', blank=True, null=True,  verbose_name='Form Id')
    spreadsheetId = models.CharField(db_column='spreadsheet_id', max_length=1000, blank=True, null=True, verbose_name='SpreadSheet Id')
    spreadsheet_name = models.CharField(db_column='spreadsheet_name', max_length=1000, blank=True, null=True, verbose_name='SpreadSheet Name')
    worksheetId = models.CharField(db_column='worksheet_id', max_length=1000, blank=True, null=True, verbose_name='WorkSheet Id')
    worksheet_name = models.CharField(db_column='worksheet_name', max_length=1000, blank=True, null=True, verbose_name='WorkSheet Name')
    media = models.CharField(db_column='media', default="Google Sheets", max_length=1000, blank=True, null=True, verbose_name='Media')
    head = models.IntegerField(db_column='head_column', blank=True, null=True, default=0, verbose_name='Head Column')
    isFilter = models.BooleanField(db_column='is_filter', default=False, verbose_name='is filter')
    lastrow = models.CharField(db_column='lastrow', max_length=1000, blank=True, null=True, verbose_name='Laast Row')

    class Meta:
        db_table = 'tbl_sheets_ads'
    def save(self, *args, **kwargs):
        self.modifiedAt = timezone.now()
        return super(SheetsAds, self).save(*args, **kwargs)

class LogLeads(models.Model):
    id = models.AutoField(primary_key=True)
    adsId = models.ForeignKey(SheetsAds, db_column='ads_id', on_delete=models.CASCADE, blank=True, null=True, related_name='sheetsads')
    adsName = models.CharField(db_column='ads_name', max_length=1000, blank=True, null=True, verbose_name='ads Name')
    lead_phone = models.CharField(db_column='lead_phone', max_length=1000, blank=True, null=True, verbose_name='lead phone')
    lead_name = models.CharField(db_column='lead_name', max_length=1000, blank=True, null=True, verbose_name='lead name')
    lead_email = models.CharField(db_column='lead_email', max_length=1000, blank=True, null=True, verbose_name='lead email')
    lead_notes = models.CharField(db_column='lead_notes', max_length=1000, blank=True, null=True, verbose_name='lead notes')
    detail = models.CharField(db_column='detail',  max_length=1000, blank=True, null=True,  verbose_name='Detail')
    createdAt = models.DateTimeField(db_column='createdAt', blank=True, null=True, default=django.utils.timezone.now, verbose_name='Created At')
    createdBy = models.IntegerField(db_column='createdBy', blank=True, null=True,  verbose_name='Created By')
    modifiedAt = models.DateTimeField(db_column='modifiedAt', blank=True, null=True,  verbose_name='Modified At')
    modifiedBy = models.IntegerField(db_column='modifiedBy', blank=True, null=True,  verbose_name='Modified By')
    accountId = models.IntegerField(db_column='accountId', blank=True, null=True,  verbose_name='Account Id')
    success = models.BooleanField(db_column='success', default=False, verbose_name='success')
    row = models.CharField(db_column='lastrow', max_length=1000, blank=True, null=True, verbose_name='Laast Row')
    skip = models.BooleanField(db_column='skip', default=False, verbose_name='skip')
    log = models.CharField(db_column='log', max_length=1000, blank=True, null=True, verbose_name='Log')
    projectName = models.CharField(db_column='project_name', max_length=1000, blank=True, null=True, verbose_name='project Name')
    channelName = models.CharField(db_column='channel_name', max_length=1000, blank=True, null=True, verbose_name='Channel Name')

    class Meta:
        db_table = 'tbl_log_leads'
    def save(self, *args, **kwargs):
        self.modifiedAt = timezone.now()
        return super(LogLeads, self).save(*args, **kwargs)

class ColumnAds(models.Model):
    id = models.AutoField(primary_key=True)
    adsId = models.ForeignKey(SheetsAds, db_column='ads_id', on_delete=models.CASCADE, blank=True, null=True, related_name='sheets_id')
    name = models.CharField(db_column='name',  max_length=1000, blank=True, null=True,  verbose_name='Name')
    columnAds = models.CharField(db_column='column_ads',  max_length=1000, blank=True, null=True,  verbose_name='column Ads name')
    text = models.CharField(db_column='text',  max_length=1000, blank=True, null=True,  verbose_name='text')
    createdAt = models.DateTimeField(db_column='createdAt', blank=True, null=True, default=django.utils.timezone.now, verbose_name='Created At')
    createdBy = models.IntegerField(db_column='createdBy', blank=True, null=True,  verbose_name='Created By')
    modifiedAt = models.DateTimeField(db_column='modifiedAt', blank=True, null=True,  verbose_name='Modified At')
    modifiedBy = models.IntegerField(db_column='modifiedBy', blank=True, null=True,  verbose_name='Modified By')
    accountId = models.IntegerField(db_column='accountId', blank=True, null=True,  verbose_name='Account Id')

    class Meta:
        db_table = 'tbl_column_ads'
    def save(self, *args, **kwargs):
        self.modifiedAt = timezone.now()
        return super(ColumnAds, self).save(*args, **kwargs)

class FilterSetup(models.Model):
    id = models.AutoField(primary_key=True)
    adsId = models.ForeignKey(SheetsAds, db_column='ads_id', on_delete=models.CASCADE, blank=True, null=True, related_name='sheets_ads')
    column = models.CharField(db_column='column_ads',  max_length=1000, blank=True, null=True,  verbose_name='Column Ads')
    filter = models.CharField(db_column='filter',  max_length=1000, blank=True, null=True,  verbose_name='Filter')
    text = models.CharField(db_column='text',  max_length=1000, blank=True, null=True,  verbose_name='text')
    createdAt = models.DateTimeField(db_column='createdAt', blank=True, null=True, default=django.utils.timezone.now, verbose_name='Created At')
    createdBy = models.IntegerField(db_column='createdBy', blank=True, null=True,  verbose_name='Created By')
    modifiedAt = models.DateTimeField(db_column='modifiedAt', blank=True, null=True,  verbose_name='Modified At')
    modifiedBy = models.IntegerField(db_column='modifiedBy', blank=True, null=True,  verbose_name='Modified By')
    accountId = models.IntegerField(db_column='accountId', blank=True, null=True,  verbose_name='Account Id')

    class Meta:
        db_table = 'tbl_filter_setup'
    def save(self, *args, **kwargs):
        self.modifiedAt = timezone.now()
        return super(FilterSetup, self).save(*args, **kwargs)

class FilterMaster(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(db_column='name',  max_length=1000, blank=True, null=True,  verbose_name='name')
    createdAt = models.DateTimeField(db_column='createdAt', blank=True, null=True, default=django.utils.timezone.now, verbose_name='Created At')
    createdBy = models.IntegerField(db_column='createdBy', blank=True, null=True,  verbose_name='Created By')

    class Meta:
        db_table = 'tbl_master_filter'
    def save(self, *args, **kwargs):
        return super(FilterMaster, self).save(*args, **kwargs)