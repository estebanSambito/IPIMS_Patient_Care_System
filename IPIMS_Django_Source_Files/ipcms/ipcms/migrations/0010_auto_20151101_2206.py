# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipcms', '0009_addmedicalhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temppatientdata',
            name='DOB',
            field=models.DateField(null=True, blank=True),
        ),
    ]
