"""
Django command for app service to wait for database to finish loading.
"""
# used for applying sleep function
import time
# This is the error thrown by psycopg2 when db is not ready.
from psycopg2 import OperationalError as Psycopg2OpError
# The error that Django throws when the db is not ready.
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """ Django command for waiting database. """

    def handle(self, *args, **options):
        """handle is the standard entry point for commands in Django"""
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                # if db is not ready check() will throw an error
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
