# Generated by Django 3.2.4 on 2022-06-20 17:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SheetsAds',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, db_column='name', max_length=1000, null=True, verbose_name='Name')),
                ('detail', models.CharField(blank=True, db_column='detail', max_length=1000, null=True, verbose_name='Detail')),
                ('createdAt', models.DateTimeField(blank=True, db_column='createdAt', default=django.utils.timezone.now, null=True, verbose_name='Created At')),
                ('createdBy', models.IntegerField(blank=True, db_column='createdBy', null=True, verbose_name='Created By')),
                ('modifiedAt', models.DateTimeField(blank=True, db_column='modifiedAt', null=True, verbose_name='Modified At')),
                ('modifiedBy', models.IntegerField(blank=True, db_column='modifiedBy', null=True, verbose_name='Modified By')),
                ('accountId', models.IntegerField(blank=True, db_column='accountId', null=True, verbose_name='Account Id')),
                ('account_sheets', models.CharField(blank=True, db_column='account_sheets', max_length=1000, null=True, verbose_name='Account sheets')),
                ('status', models.CharField(blank=True, db_column='status', max_length=1000, null=True, verbose_name='Status')),
                ('channelCode', models.CharField(blank=True, db_column='channelCode', max_length=1000, null=True, verbose_name='Channel code')),
                ('channelId', models.CharField(blank=True, db_column='channel_id', max_length=1000, null=True, verbose_name='Channel Id')),
                ('spreadsheetId', models.CharField(blank=True, db_column='spreadsheet_id', max_length=1000, null=True, verbose_name='SpreadSheet Id')),
                ('spreadsheet_name', models.CharField(blank=True, db_column='spreadsheet_name', max_length=1000, null=True, verbose_name='SpreadSheet Name')),
                ('worksheetId', models.CharField(blank=True, db_column='worksheet_id', max_length=1000, null=True, verbose_name='WorkSheet Id')),
                ('worksheet_name', models.CharField(blank=True, db_column='worksheet_name', max_length=1000, null=True, verbose_name='WorkSheet Name')),
            ],
            options={
                'db_table': 'tbl_sheets_ads',
            },
        ),
        migrations.CreateModel(
            name='LogLeads',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('lead_phone', models.CharField(blank=True, db_column='lead_phone', max_length=1000, null=True, verbose_name='lead phone')),
                ('detail', models.CharField(blank=True, db_column='detail', max_length=1000, null=True, verbose_name='Detail')),
                ('createdAt', models.DateTimeField(blank=True, db_column='createdAt', default=django.utils.timezone.now, null=True, verbose_name='Created At')),
                ('createdBy', models.IntegerField(blank=True, db_column='createdBy', null=True, verbose_name='Created By')),
                ('modifiedAt', models.DateTimeField(blank=True, db_column='modifiedAt', null=True, verbose_name='Modified At')),
                ('modifiedBy', models.IntegerField(blank=True, db_column='modifiedBy', null=True, verbose_name='Modified By')),
                ('accountId', models.IntegerField(blank=True, db_column='accountId', null=True, verbose_name='Account Id')),
                ('success', models.BooleanField(db_column='success', default=False, verbose_name='success')),
                ('adsId', models.ForeignKey(blank=True, db_column='ads_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ads_id', to='sheets.sheetsads')),
            ],
            options={
                'db_table': 'tbl_log_leads',
            },
        ),
    ]
