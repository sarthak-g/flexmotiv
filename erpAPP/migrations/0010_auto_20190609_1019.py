# Generated by Django 2.2.1 on 2019-06-09 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erpAPP', '0009_delete_csvfilestorage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csv_fm_txn',
            name='txnAuditFile',
            field=models.CharField(max_length=20),
        ),
    ]