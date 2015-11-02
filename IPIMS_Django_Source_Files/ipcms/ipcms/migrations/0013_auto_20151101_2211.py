# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipcms', '0012_auto_20151101_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temppatientdata',
            name='insurance_policy_number',
            field=models.IntegerField(blank=True),
        ),
    ]
