# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipcms', '0008_delete_patientmedicalreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddMedicalHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('allergies', models.CharField(default=b'', max_length=255)),
                ('medical_conditions', models.CharField(default=b'', max_length=255)),
                ('patient', models.ForeignKey(default=b'', to='ipcms.Patient')),
            ],
        ),
    ]
