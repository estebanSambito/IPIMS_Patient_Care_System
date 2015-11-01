# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipcms', '0002_auto_20151030_0247'),
    ]

    operations = [
        migrations.AddField(
            model_name='emedication',
            name='prescribed_by_doctor',
            field=models.OneToOneField(default=b'0', to='ipcms.Doctor'),
        ),
        migrations.AddField(
            model_name='emedication',
            name='reminder',
            field=models.IntegerField(default=0),
        ),
    ]
