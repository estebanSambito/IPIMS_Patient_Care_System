# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('ipcms', '0002_emedication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temppatientdata',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(default=b'', max_length=128, blank=True),
        ),
    ]
