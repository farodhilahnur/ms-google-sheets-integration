# Generated by Django 3.2.4 on 2023-02-25 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0022_auto_20230225_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logleads',
            name='isFilter',
        ),
        migrations.AddField(
            model_name='logleads',
            name='skip',
            field=models.BooleanField(db_column='skip', default=False, verbose_name='skip'),
        ),
    ]
