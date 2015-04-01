from django.db import models
from django.contrib.auth.models import User
from django_extensions.db import fields
from .utils import create_paste_hash


class Syntax(models.Model):

    class Meta:
        verbose_name = "Syntax"
        verbose_name_plural = "Syntaxes"

    name = models.CharField(max_length=64)
    string_id = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name
    

class Paste(models.Model):

    class Meta:
        verbose_name = "Paste"
        verbose_name_plural = "Pastes"

    TEN_MINUTES = 10 * 60
    HALF_OF_AN_HOUR = 3 * TEN_MINUTES
    DAY = 48 * HALF_OF_AN_HOUR
    WEEK = 7 * DAY
    INFINITE = 0

    EXPIRATIONS = (
        (INFINITE, 'Infinite'),
        (TEN_MINUTES, '10 minutes'),
        (HALF_OF_AN_HOUR, '30 minutes'),
        (DAY, '24 hours'),
        (WEEK, 'a week')
    )

    title = models.CharField(max_length=64, blank=True, null=True, default="Unnamed")
    content = models.TextField()
    hash = models.SlugField()

    author = models.ForeignKey(User)
    syntax = models.ForeignKey(Syntax)

    expires_in = models.PositiveIntegerField(choices=EXPIRATIONS, default=INFINITE)

    created = fields.CreationDateTimeField()
    modified = fields.ModificationDateTimeField()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        "Overriden save method. If the model is yet to be saved, theres the hash generated, based on the titles value."
        if not self.id:
            self.hash = create_paste_hash(Paste, self.title)

        super(Paste, self).save(*args, **kwargs)