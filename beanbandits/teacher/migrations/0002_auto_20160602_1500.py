# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-02 15:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modes',
            name='mode',
            field=models.PositiveIntegerField(choices=[(0, b'Random'), (1, b'Wrong Stay Correct Shift'), (2, b'Improved Wrong Stay Correct Shift'), (3, b'Multi-armed Bandit')], primary_key=True, serialize=False),
        ),
    ]
