# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('races', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organizer',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='race',
            name='description',
            field=models.TextField(blank=True, default='', help_text='A brief description of the race course, ideally.'),
            preserve_default=True,
        ),
    ]
