# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField(default=-1)),
                ('strategy', models.IntegerField(default=-1)),
                ('dataset', models.IntegerField(default=-1)),
                ('num_teaching_images', models.IntegerField(default=-1)),
                ('num_testing_images', models.IntegerField(default=-1)),
                ('score', models.IntegerField(default=-1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField(default=-1)),
                ('stage', models.IntegerField(default=-1)),
                ('stage_image_num', models.IntegerField(default=-1)),
                ('class_id', models.IntegerField(default=-1)),
                ('sample_id', models.IntegerField(default=-1)),
                ('answer', models.IntegerField(default=-1)),
                ('is_correct', models.BooleanField(default=False)),
                ('time', models.IntegerField(default=-1)),
                ('dataset', models.IntegerField(default=-1)),
                ('strategy', models.IntegerField(default=-1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
