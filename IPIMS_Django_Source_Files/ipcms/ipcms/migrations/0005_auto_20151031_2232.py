# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ipcms', '0004_auto_20151031_2154'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabReports',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lab_results', models.CharField(max_length=255, choices=[(b'positive', b'Positive'), (b'negative', b'Negative')])),
                ('lab_test', models.CharField(max_length=255, choices=[(b'Blood pressure screening', b'Blood pressure screening'), (b'C-reactive protein test', b'C-reactive protein test'), (b'Colonoscopy', b'Colonoscopy'), (b'Diabetes risk tests', b'Diabetes risk tests'), (b'Pap smear', b'Pap smear'), (b'Skin cancer exam', b'Skin cancer exam'), (b'Blood Tests', b'Blood Tests')])),
                ('lab_notes', models.TextField(default=b'Insert Notes For Lab Test')),
                ('lab_patient', models.ForeignKey(default=b'0', to='ipcms.Patient')),
            ],
        ),
        migrations.CreateModel(
            name='LabTech',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lab_first_name', models.CharField(default=b'', max_length=256)),
                ('lab_last_name', models.CharField(default=b'', max_length=256)),
                ('lab_user', models.OneToOneField(default=b'', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='labreports',
            name='lab_tech',
            field=models.ForeignKey(default=b'', to='ipcms.LabTech'),
        ),
    ]
