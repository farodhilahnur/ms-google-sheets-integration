# Generated by Django 3.2.4 on 2023-06-13 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0027_auto_20230613_0311'),
    ]

    operations = [
        migrations.AddField(
            model_name='logleads',
            name='channelName',
            field=models.CharField(blank=True, db_column='channel_name', max_length=1000, null=True, verbose_name='Channel Name'),
        ),
        migrations.AddField(
            model_name='logleads',
            name='projectName',
            field=models.CharField(blank=True, db_column='project_name', max_length=1000, null=True, verbose_name='project Name'),
        ),
    ]
