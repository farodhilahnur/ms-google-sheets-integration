# Generated by Django 3.2.4 on 2022-07-20 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0012_auto_20220708_0203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sheetsaccounts',
            name='status',
            field=models.CharField(blank=True, db_column='status', default='connected', max_length=1000, null=True, verbose_name='Status'),
        ),
    ]
