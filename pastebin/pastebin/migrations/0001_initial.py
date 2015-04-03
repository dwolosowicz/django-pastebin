# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Paste',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'Unnamed', max_length=64, null=True, blank=True)),
                ('content', models.TextField()),
                ('hash', models.SlugField()),
                ('visibility', models.CharField(default=b'link', max_length=12, choices=[(b'link', b'Everybody with a link'), (b'users', b'Only specified users')])),
                ('expires_in', models.PositiveIntegerField(default=0, choices=[(0, b'Infinite'), (600, b'10 minutes'), (1800, b'30 minutes'), (86400, b'24 hours'), (604800, b'a week')])),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, editable=False, blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'Paste',
                'verbose_name_plural': 'Pastes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Syntax',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('string_id', models.CharField(max_length=64)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Syntax',
                'verbose_name_plural': 'Syntaxes',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='paste',
            name='syntax',
            field=models.ForeignKey(to='pastebin.Syntax'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='paste',
            name='users',
            field=models.ManyToManyField(related_name='users', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
