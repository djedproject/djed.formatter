""" formatter tests """
import pytz
from datetime import datetime, timedelta
from pyramid.config import Configurator
from pyramid.exceptions import ConfigurationConflictError

from base import BaseTestCase


class TestFormatter(BaseTestCase):

    def test_formatter_registration(self):
        def simple(request, v):
            return 'simple-%s'%v

        self.config.add_formatter('simple', simple)

        request = self.make_request()
        self.assertEqual(request.format.simple('test'), 'simple-test')
        self.assertIs(request.format.simple.callable, simple)

    def test_formatter_cache(self):
        def simple(request, v):
            return 'simple-%s'%v

        self.config.add_formatter('simple', simple)

        simple = self.request.format['simple']
        self.assertIs(simple, self.request.format['simple'])
        self.assertIs(self.request.format['simple'], self.request.format.simple)

        request = self.make_request()
        self.assertIsNot(simple, request.format.simple)

    def test_formatter_unknown(self):
        request = self.make_request()
        self.assertRaises(
            AttributeError, request.format.__getattr__, 'simple')
        self.assertRaises(
            KeyError, request.format.__getitem__, 'simple')

    def test_formatter_registration_duplicate(self):
        def simple1(v):
            """ """

        def simple2(v):
            """ """

        config = Configurator()
        config.include('djed.formatter')

        config.add_formatter('test', simple1)
        config.add_formatter('test', simple2)

        self.assertRaises(ConfigurationConflictError, config.commit)

    def test_formatter_introspector(self):
        def simple(v):
            """ doc """

        self.config.add_formatter('simple', simple)

        from djed.formatter import ID_FORMATTER

        discr = (ID_FORMATTER, 'simple')
        intr = self.config.introspector.get(ID_FORMATTER, discr)

        self.assertIsNotNone(intr)
        self.assertEqual(intr['name'], 'simple')
        self.assertEqual(intr['description'], ' doc ')
        self.assertEqual(intr['callable'], simple)

    def test_date_formatter(self):
        format = self.request.format

        # format only datetime
        self.assertEqual(format.date('text string'), 'text string')

        dt = datetime(2011, 2, 6, 10, 35, 45, 80)
        self.assertEqual(format.date(dt, 'short'),
                         '2/6/11')
        self.assertEqual(format.date(dt, 'medium'),
                         'Feb 6, 2011')
        self.assertEqual(format.date(dt, 'long'),
                         'February 6, 2011')
        self.assertEqual(format.date(dt, 'full'),
                         'Sunday, February 6, 2011')

    def test_date_formatter_locale(self):
        format = self.request.format

        dt = datetime(2011, 2, 6, 10, 35, 45, 80)
        self.assertEqual(format.date(dt, 'full', 'es'),
                         'domingo, 6 de febrero de 2011')

    def test_time_formatter(self):
        format = self.request.format

        # format only datetime
        self.assertEqual(format.time('text string'), 'text string')

        dt = datetime(2011, 2, 6, 10, 35, 45, 80, pytz.UTC)
        self.assertEqual(format.time(dt, 'short'),
                         '10:35 AM')
        self.assertEqual(format.time(dt, 'medium'),
                         '10:35:45 AM')
        self.assertEqual(format.time(dt, 'long'),
                         '10:35:45 AM +0000')
        self.assertEqual(format.time(dt, 'full'),
                         '10:35:45 AM GMT+00:00')

    def test_time_formatter_timezone(self):
        format = self.request.format

        dt = datetime(2011, 2, 6, 10, 35, 45, 80, pytz.UTC)
        self.assertEqual(format.time(dt, 'long', 'US/Central'),
                         '4:35:45 AM CST')

    def test_time_formatter_locale(self):
        format = self.request.format

        dt = datetime(2011, 2, 6, 10, 35, 45, 80, pytz.UTC)
        self.assertEqual(format.time(dt, 'full', locale_name='es'),
                         '10:35:45 GMT+00:00')

    def test_datetime_formatter(self):
        format = self.request.format

        # format only datetime
        self.assertEqual(format.datetime('text string'), 'text string')

        dt = datetime(2011, 2, 6, 10, 35, 45, 80, pytz.UTC)
        self.assertEqual(format.datetime(dt, 'short'),
                         '2/6/11, 10:35 AM')
        self.assertEqual(format.datetime(dt, 'medium'),
                         'Feb 6, 2011, 10:35:45 AM')
        self.assertEqual(format.datetime(dt, 'long'),
                         'February 6, 2011 at 10:35:45 AM +0000')
        self.assertEqual(format.datetime(dt, 'full'),
                         'Sunday, February 6, 2011 at 10:35:45 AM GMT+00:00')

    def test_datetime_formatter_locale(self):
        format = self.request.format

        dt = datetime(2011, 2, 6, 10, 35, 45, 80, pytz.UTC)
        self.assertEqual(format.datetime(dt, 'long', locale_name='es'),
                         '6 de febrero de 2011 10:35:45 +0000')

    def test_datetime_formatter_timezone(self):
        format = self.request.format

        dt = datetime(2011, 2, 6, 10, 35, 45, 80, pytz.UTC)
        self.assertEqual(format.datetime(dt, 'long', 'US/Central'),
                         'February 6, 2011 at 4:35:45 AM CST')

    def test_timedelta_formatter(self):
        format = self.request.format

        # format only timedelta
        self.assertEqual(format.timedelta('text string'), 'text string')

        td = timedelta(hours=10, minutes=5, seconds=45)

        # medium format
        self.assertEqual(format.timedelta(td, format='medium'),
                         '10 hours')

        # short format
        self.assertEqual(format.timedelta(td, format='short'),
                         '10 hrs')

        # default format
        self.assertEqual(format.timedelta(td), '10 hours')

        # locale format
        self.assertEqual(format.timedelta(td, locale_name='es'), '10 horas')

    def test_size_formatter(self):
        format = self.request.format

        # format only size
        self.assertEqual(format.size('text string'), 'text string')

        v = 1024
        self.assertEqual(format.size(v, 'b'), '1024 B')

        self.assertEqual(format.size(v, 'k'), '1.00 KB')

        self.assertEqual(format.size(1024*768, 'm'), '0.75 MB')
        self.assertEqual(format.size(1024*768*768, 'm'), '576.00 MB')

        self.assertEqual(format.size(1024*768*768, 'g'), '0.56 GB')
