# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pastebin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paste',
            name='users',
            field=models.ManyToManyField(related_name='users', null=True, to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
