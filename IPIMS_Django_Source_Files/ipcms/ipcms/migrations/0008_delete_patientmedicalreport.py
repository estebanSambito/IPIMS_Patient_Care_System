# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipcms', '0007_patientmedicalreport'),
    ]

    operations = [
        migrations.DeleteModel(
            name='patientMedicalReport',
        ),
    ]
