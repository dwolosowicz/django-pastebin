from django_extensions.management.jobs import MinutelyJob
from django.db import connection
from pastebin.models import Paste

class Job(MinutelyJob):
    help = "Job removes Pastes that have expired"

    def execute(self):
        query = "DELETE FROM {} WHERE NOW() > DATE_ADD(created, INTERVAL expires_in SECOND) AND expires_in > 0".format(Paste._meta.db_table)

        connection.cursor().execute(query)