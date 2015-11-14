# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipcms', '0013_auto_20151101_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='emedication',
            name='medication_quantity',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
