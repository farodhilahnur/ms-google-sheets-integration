# Generated by Django 3.2.4 on 2023-01-09 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0016_sheetsads_head'),
    ]

    operations = [
        migrations.AddField(
            model_name='sheetsads',
            name='process',
            field=models.BooleanField(db_column='process', default=False, verbose_name='process'),
        ),
    ]
