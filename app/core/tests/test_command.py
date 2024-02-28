"""
Test custom Django management commands
"""
# We perform mocking to save computing resources.
# Essentiall we will be simulating the behavior of the database.
from unittest.mock import patch
# Psycopg2Error is a possible error when we connect to the database
# before the database is ready.
from psycopg2 import OperationalError as Psycopg2Error
# call_command allows to call the command we are testing by its name
from django.core.management import call_command
# OperationalError is an error thrown by the database
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# @patch() simulates db operation stated as argument.
# The check method is instrinsic to BaseCommand object.
# The result of check method is passed to patched_check object.
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """ Performs test for various commands. """

    def test_wait_for_db_ready(self, patched_check):
        """ Check waiting for database if database is ready. """
        # Initialization : The db returned true because it is ready.
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    # We want to test the behavior if db is not yet ready.
    # After the previous, we want to add a sleep interval so that
    # the execution of next command is not abrupt.
    # The patch below is added as the 2nd argument, while effects of outer
    # patches is added on the next argument, and so on.
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """ Check waiting for database when getting OperationalError. """
        # Initialization : The db will be called five times.
        # The first two times has Psycopg2Error adapter error
        # The next three times has OperationalError
        # The last one is the connection is now ready.
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
