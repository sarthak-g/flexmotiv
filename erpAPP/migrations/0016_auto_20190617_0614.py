# Generated by Django 2.2 on 2019-06-17 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erpAPP', '0015_auto_20190611_0714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fm_utrans',
            name='utranConfirmed',
            field=models.CharField(default='N', max_length=1),
        ),
    ]
