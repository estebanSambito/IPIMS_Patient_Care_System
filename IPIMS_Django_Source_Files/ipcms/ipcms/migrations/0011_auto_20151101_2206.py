# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipcms', '0010_auto_20151101_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temppatientdata',
            name='DOB',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
