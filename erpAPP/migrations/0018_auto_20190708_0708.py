# Generated by Django 2.2 on 2019-07-08 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erpAPP', '0017_auto_20190701_0835'),
    ]

    operations = [
        migrations.AddField(
            model_name='fm_ptctrans',
            name='ptcAccounted',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='fm_ptctrans',
            name='ptcAudited',
            field=models.BooleanField(default=0),
        ),
    ]
