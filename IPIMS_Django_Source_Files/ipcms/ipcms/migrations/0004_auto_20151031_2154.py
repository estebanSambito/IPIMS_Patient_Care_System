# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipcms', '0003_auto_20151031_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emedication',
            name='patient',
            field=models.ForeignKey(default=b'', to='ipcms.Patient'),
        ),
        migrations.AlterField(
            model_name='emedication',
            name='prescribed_by_doctor',
            field=models.ForeignKey(default=b'0', to='ipcms.Doctor'),
        ),
    ]
