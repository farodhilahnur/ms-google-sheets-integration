# Generated by Django 3.2.4 on 2022-07-04 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0004_logleads_row'),
    ]

    operations = [
        migrations.AddField(
            model_name='sheetsads',
            name='media',
            field=models.CharField(blank=True, db_column='media', default='Google Sheets', max_length=1000, null=True, verbose_name='Media'),
        ),
    ]
