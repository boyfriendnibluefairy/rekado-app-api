"""
 Samples tests for the ff files:
   calc.py
"""
from django.test import SimpleTestCase
from app import calc

class CalcTests(SimpleTestCase):
    """ Test the calc module"""

    def test_add_numbers(self):
        """ Test the function add() """
        result = calc.add(6,9)
        self.assertEqual(result, 15)

    def test_subtract_numbers(self):
        """ Test the function sub() """
        result = calc.subtract(9,16)
        self.assertEqual(result, -7)