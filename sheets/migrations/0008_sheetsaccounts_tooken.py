# Generated by Django 3.2.4 on 2022-07-07 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0007_alter_sheetsaccounts_totalintegration'),
    ]

    operations = [
        migrations.AddField(
            model_name='sheetsaccounts',
            name='tooken',
            field=models.CharField(blank=True, db_column='token', max_length=1000, null=True, verbose_name='Token'),
        ),
    ]
