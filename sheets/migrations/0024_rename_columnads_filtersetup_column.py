# Generated by Django 3.2.4 on 2023-02-25 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0023_auto_20230225_1636'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filtersetup',
            old_name='columnAds',
            new_name='column',
        ),
    ]
