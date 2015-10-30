# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipcms', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='temppatientdata',
            name='date_created',
        ),
        migrations.AddField(
            model_name='patient',
            name='date_created',
            field=models.CharField(default=b'9-20-1995', max_length=20, null=True),
        ),
    ]
