from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_extensions.db import fields
from .utils import create_paste_hash
from model_utils.managers import PassThroughManager

import datetime
import json


class SyntaxManager(models.Manager):

    def to_json(self):
        pastes_list = [{'name': s.name, 'id': s.string_id} for s in self.all()]

        return json.dumps(pastes_list)


class Syntax(models.Model):

    class Meta:
        verbose_name = "Syntax"
        verbose_name_plural = "Syntaxes"

        ordering = ['name']

    objects = SyntaxManager()

    name = models.CharField(max_length=64)
    string_id = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class PasteQuerySet(models.query.QuerySet):

    def by_author(self, user):
        return self.filter(author=user)


class Paste(models.Model):

    class Meta:
        verbose_name = "Paste"
        verbose_name_plural = "Pastes"
        ordering = ['-created']

    TEN_MINUTES = 10 * 60
    HALF_OF_AN_HOUR = 3 * TEN_MINUTES
    DAY = 48 * HALF_OF_AN_HOUR
    WEEK = 7 * DAY
    INFINITE = 0

    EVERYONE_WITH_LINK = 'link'
    ONLY_SPECIFIED_USERS = 'users'

    EXPIRATIONS = (
        (INFINITE, 'Infinite'),
        (TEN_MINUTES, '10 minutes'),
        (HALF_OF_AN_HOUR, '30 minutes'),
        (DAY, '24 hours'),
        (WEEK, 'a week')
    )

    VISIBILITY = (
        (EVERYONE_WITH_LINK, 'Everybody with a link'),
        (ONLY_SPECIFIED_USERS, 'Only specified users'),
    )

    objects = PassThroughManager.for_queryset_class(PasteQuerySet)()

    title = models.CharField(max_length=64, blank=True, null=True, default="Unnamed")
    content = models.TextField()
    hash = models.SlugField()

    author = models.ForeignKey(User)
    syntax = models.ForeignKey(Syntax)
    users = models.ManyToManyField(User, related_name='users')

    visibility = models.CharField(choices=VISIBILITY, default=EVERYONE_WITH_LINK, max_length=12)
    expires_in = models.PositiveIntegerField(choices=EXPIRATIONS, default=INFINITE)

    created = fields.CreationDateTimeField()
    modified = fields.ModificationDateTimeField()

    def __unicode__(self):
        return self.title

    def expires(self):
        return self.created + datetime.timedelta(seconds=self.expires_in)

    def expired(self):
        return timezone.now() > self.expires()

    def save(self, *args, **kwargs):
        """
        Overridden save method.
        If the model is yet to be saved, theres the title's hash generated.
        """
        if not self.id:
            self.hash = create_paste_hash(Paste, self.title)

        super(Paste, self).save(*args, **kwargs)
