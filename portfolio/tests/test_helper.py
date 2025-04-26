import calendar
from datetime import datetime
from django.test import TestCase
from ..helper import get_date_query


class HelperTest(TestCase):

    def test_jan_valid(self):
        dt = datetime(2020, 1, 25)
        min, max = get_date_query(dt)
        last_day = calendar.monthrange(dt.year, dt.month)[1]
        self.assertEqual(min.year, dt.year)
        self.assertEqual(min.month, dt.month)
        self.assertEqual(min.day, 1)
        self.assertEqual(max.year, dt.year)
        self.assertEqual(max.month, dt.month)
        self.assertEqual(max.day, last_day)

    def test_june_valid(self):
        dt = datetime(2020, 6, 15)
        min, max = get_date_query(dt)
        last_day = calendar.monthrange(dt.year, dt.month)[1]
        self.assertEqual(min.year, dt.year)
        self.assertEqual(min.month, dt.month)
        self.assertEqual(min.day, 1)
        self.assertEqual(max.year, dt.year)
        self.assertEqual(max.month, dt.month)
        self.assertEqual(max.day, last_day)

    def test_dec_valid(self):
        dt = datetime(2020, 12, 1)
        min, max = get_date_query(dt)
        last_day = calendar.monthrange(dt.year, dt.month)[1]
        self.assertEqual(min.year, dt.year)
        self.assertEqual(min.month, dt.month)
        self.assertEqual(min.day, 1)
        self.assertEqual(max.year, dt.year)
        self.assertEqual(max.month, dt.month)
        self.assertEqual(max.day, last_day)
