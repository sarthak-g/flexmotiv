# Generated by Django 2.2 on 2019-06-30 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erpAPP', '0013_auto_20190626_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='fm_ptcform',
            name='txnID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='erpAPP.fm_txn'),
        ),
    ]
