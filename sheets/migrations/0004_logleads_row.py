# Generated by Django 3.2.4 on 2022-06-28 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0003_auto_20220624_0821'),
    ]

    operations = [
        migrations.AddField(
            model_name='logleads',
            name='row',
            field=models.CharField(blank=True, db_column='lastrow', max_length=1000, null=True, verbose_name='Laast Row'),
        ),
    ]
