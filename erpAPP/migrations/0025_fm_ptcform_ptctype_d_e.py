# Generated by Django 2.2 on 2019-07-23 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erpAPP', '0024_auto_20190723_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='fm_ptcform',
            name='ptcType_D_E',
            field=models.CharField(max_length=1, null=True),
        ),
    ]
