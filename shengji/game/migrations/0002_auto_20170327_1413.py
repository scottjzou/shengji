# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 21:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'verbose_name': 'player'},
        ),
        migrations.RemoveField(
            model_name='player',
            name='test',
        ),
        migrations.AlterField(
            model_name='player',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.TextField(),
        ),
    ]
