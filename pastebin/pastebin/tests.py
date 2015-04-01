from django.test import TestCase
from django.contrib.auth.models import User

from pastebin.models import Syntax, Paste
from pastebin.jobs.minutely import remove_old_pastes 

import random, string, datetime


def _create_random_string():
    "Creates random string with length of 10"
    return ''.join(random.SystemRandom().choice(string.uppercase + string.digits) for _ in xrange(10))


def _create_syntax(name):
    syntax = Syntax()
    syntax.name = name
    syntax.string_id = name.lower()
    syntax.save()

    return syntax


def _create_random_paste(user, syntax, date=datetime.datetime.now(), expires_in=10 * 60):
    paste = Paste()
    paste.title = _create_random_string()
    paste.content = _create_random_string()
    paste.syntax = syntax
    paste.expires_in = expires_in
    paste.author = user
    paste.created = date
    paste.save()

    return paste


def _run_job(obj):
   instance = obj() 
   instance.execute()

class RemoveOldPastesJobTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.syntax = _create_syntax('text')

    def test_deletes_expired_pastes(self):
        paste_to_delete = _create_random_paste(self.user, self.syntax, date=datetime.datetime.now() - datetime.timedelta(minutes=360))
        paste_to_omit = _create_random_paste(self.user, self.syntax, date=datetime.datetime.now() + datetime.timedelta(minutes=360))

        self.assertEqual(2, Paste.objects.all().count())

        _run_job(remove_old_pastes.Job)

        self.assertEqual(1, Paste.objects.all().count())