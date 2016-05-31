# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 00:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Modes',
            fields=[
                ('mode', models.PositiveIntegerField(choices=[(0, b'Random'), (1, b'Least used'), (2, b'Bean Bandit')], primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=-1)),
                ('score', models.IntegerField(default=-1)),
                ('is_finished', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=-1)),
                ('is_correct', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=10)),
                ('definition', models.CharField(max_length=255)),
                ('pinyin', models.CharField(max_length=40)),
                ('rank', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='WordSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='word',
            name='wordset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.WordSet'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='mode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.Modes'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='wordset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.WordSet'),
        ),
    ]
