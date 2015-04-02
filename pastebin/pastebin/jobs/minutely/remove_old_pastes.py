from django_extensions.management.jobs import MinutelyJob
from django.db.models import Q
from pastebin.models import Paste

class Job(MinutelyJob):
    help = "Job removes Pastes that have expired"

    def execute(self):
        Paste.objects.filter(expires_in__gt=0).extra(where=["NOW() > DATE_ADD(created, INTERVAL expires_in SECOND)"]).delete()