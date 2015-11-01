# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipcms', '0006_auto_20151031_2235'),
    ]

    operations = [
        migrations.CreateModel(
            name='patientMedicalReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(default=b'', max_length=256)),
                ('last_name', models.CharField(default=b'', max_length=256)),
                ('age', models.IntegerField(default=18)),
                ('gender', models.CharField(default=b'Select a gender', max_length=256, choices=[(b'male', b'Male'), (b'female', b'Female'), (b'other', b'Other'), (b'prefer not to say', b'Prefer Not To Say')])),
                ('race', models.CharField(default=b'Other', max_length=256, choices=[(b'white', b'White'), (b'american_indian_alaskan_native', b'American Indian or Alaskan Native'), (b'hawaiian', b'Native Hawaiian or Other Pacific Islander'), (b'black', b'Black or African American'), (b'asian', b'Asian'), (b'other', b'Other')])),
                ('DOB', models.DateField(default=b'')),
                ('allergies', models.CharField(default=b'', max_length=256)),
                ('medications', models.CharField(default=b'', max_length=256)),
                ('insurance_provider', models.CharField(max_length=256)),
                ('insurance_policy_number', models.IntegerField()),
            ],
        ),
    ]
