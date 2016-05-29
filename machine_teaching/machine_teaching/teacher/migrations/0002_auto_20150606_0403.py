# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='dataset',
        ),
        migrations.RemoveField(
            model_name='user',
            name='num_teaching_images',
        ),
        migrations.RemoveField(
            model_name='user',
            name='num_testing_images',
        ),
        migrations.RemoveField(
            model_name='user',
            name='strategy',
        ),
        migrations.RemoveField(
            model_name='userresponse',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='userresponse',
            name='class_id',
        ),
        migrations.RemoveField(
            model_name='userresponse',
            name='dataset',
        ),
        migrations.RemoveField(
            model_name='userresponse',
            name='sample_id',
        ),
        migrations.RemoveField(
            model_name='userresponse',
            name='stage',
        ),
        migrations.RemoveField(
            model_name='userresponse',
            name='stage_image_num',
        ),
        migrations.RemoveField(
            model_name='userresponse',
            name='strategy',
        ),
        migrations.RemoveField(
            model_name='userresponse',
            name='time',
        ),
    ]
