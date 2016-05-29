# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_auto_20150606_0403'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_finished',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
