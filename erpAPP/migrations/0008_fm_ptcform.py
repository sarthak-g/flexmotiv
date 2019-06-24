# Generated by Django 2.2 on 2019-06-24 09:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('erpAPP', '0007_auto_20190622_2024'),
    ]

    operations = [
        migrations.CreateModel(
            name='fm_ptcform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ptcValue', models.IntegerField()),
                ('ptcType', models.CharField(max_length=40)),
                ('ptcDate', models.DateField(auto_now=True)),
                ('ptcApproved', models.BooleanField(default=0)),
                ('ptcApprovedBy', models.CharField(max_length=50, null=True)),
                ('prID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erpAPP.fm_project')),
                ('uID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
