# Generated by Django 2.2 on 2019-06-22 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erpAPP', '0006_auto_20190622_2007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fm_budgethead',
            name='bhTitle',
            field=models.CharField(max_length=50),
        ),
    ]