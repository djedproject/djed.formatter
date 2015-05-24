""" date/time formatters """
from datetime import (
    date,
    datetime,
    time,
    timedelta
)
from babel.dates import (
    format_date,
    format_datetime,
    format_time,
    format_timedelta,
    get_timezone
)
from pyramid.compat import text_type


def date_formatter(request, value, format='medium', locale_name=None):
    """Date formatter
    """
    if not isinstance(value, datetime) and not isinstance(value, date):
        return value

    if not locale_name:
        locale_name = request.locale_name

    return text_type(format_date(value, format, locale_name))


def time_formatter(request, value, format='medium',
                   tzname=None, locale_name=None):
    """Time formatters
    """
    if not isinstance(value, datetime) and not isinstance(value, time):
        return value
    tzinfo = None

    if tzname:
        tzinfo = get_timezone(tzname)

    if not tzinfo:
        settings = request.registry.settings
        tzinfo = get_timezone(settings['pyramid.default_timezone_name'])

    if not locale_name:
        locale_name = request.locale_name

    return text_type(format_time(value, format, tzinfo, locale_name))


def datetime_formatter(request, value, format='medium',
                       tzname=None, locale_name=None):
    """DateTime formatter

    Short::

      >> dt = datetime(2011, 2, 6, 10, 35, 45, 80, pytz.UTC)

      >> request.format.datetime(dt, 'short')
      '02/06/11 04:35 AM'


    Medium::

      >> request.format.datetime(dt, 'medium')
      'Feb 06, 2011 04:35 AM'

    Long::

      >> request.format.datetime(dt, 'long')
      'February 06, 2011 04:35 AM -0600'

    Full::

      >> request.format.datetime(dt, 'full')
      'Sunday, February 06, 2011 04:35:45 AM CST'

    """
    if not isinstance(value, datetime):
        return value

    tzinfo = None

    if tzname:
        tzinfo = get_timezone(tzname)

    if not tzinfo:
        settings = request.registry.settings
        tzinfo = get_timezone(settings['pyramid.default_timezone_name'])

    if not locale_name:
        locale_name = request.locale_name

    return text_type(format_datetime(value, format, tzinfo, locale_name))


def timedelta_formatter(request, value, granularity='second', threshold=.85,
                        add_direction=False, format='medium',
                        locale_name=None):
    """Timedelta formatter

    Format::

      >> td = timedelta(hours=10, minutes=5, seconds=45)
      >> request.format.timedelta(td, format='medium')
      '10 hours'
      >> request.format.timedelta(td, format='short')
      '10 hrs'


    Default::

      >> request.format.timedelta(td)
      '10 hours'

    """
    if not isinstance(value, timedelta):
        return value

    if not locale_name:
        locale_name = request.locale_name

    return text_type(format_timedelta(
        value, format=format, granularity=granularity, threshold=threshold,
        add_direction=add_direction, locale=locale_name))
