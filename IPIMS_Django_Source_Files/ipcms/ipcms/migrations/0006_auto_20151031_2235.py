# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipcms', '0005_auto_20151031_2232'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lab_results', models.CharField(max_length=255, choices=[(b'positive', b'Positive'), (b'negative', b'Negative')])),
                ('lab_test', models.CharField(max_length=255, choices=[(b'Blood pressure screening', b'Blood pressure screening'), (b'C-reactive protein test', b'C-reactive protein test'), (b'Colonoscopy', b'Colonoscopy'), (b'Diabetes risk tests', b'Diabetes risk tests'), (b'Pap smear', b'Pap smear'), (b'Skin cancer exam', b'Skin cancer exam'), (b'Blood Tests', b'Blood Tests')])),
                ('lab_notes', models.TextField(default=b'Insert Notes For Lab Test')),
                ('lab_patient', models.ForeignKey(default=b'0', to='ipcms.Patient')),
                ('lab_tech', models.ForeignKey(default=b'', to='ipcms.LabTech')),
            ],
        ),
        migrations.RemoveField(
            model_name='labreports',
            name='lab_patient',
        ),
        migrations.RemoveField(
            model_name='labreports',
            name='lab_tech',
        ),
        migrations.DeleteModel(
            name='LabReports',
        ),
    ]
