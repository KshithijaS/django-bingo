# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-02-23 16:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bingo', '0009_make_word_and_site_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Topic'), (2, 'Middle'), (3, 'Meta')]),
        ),
    ]
