# Generated by Django 2.2.1 on 2019-06-07 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erpAPP', '0005_csv_fm_txn_txnauditfilestorage'),
    ]

    operations = [
        migrations.CreateModel(
            name='CSVfileStorage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txnAuditFileStorage', models.FileField(upload_to='file_link')),
            ],
        ),
        migrations.RemoveField(
            model_name='csv_fm_txn',
            name='txnAuditFileStorage',
        ),
    ]