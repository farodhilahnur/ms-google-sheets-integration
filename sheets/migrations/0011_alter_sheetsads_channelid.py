# Generated by Django 3.2.4 on 2022-07-08 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0010_sheetsaccounts_refresh_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sheetsads',
            name='channelId',
            field=models.IntegerField(blank=True, db_column='channel_id', null=True, verbose_name='Channel Id'),
        ),
    ]
