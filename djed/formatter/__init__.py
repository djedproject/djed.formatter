""" formatters """
from pyramid.registry import Introspectable

from djed.formatter.datetime import (
    date_formatter,
    datetime_formatter,
    time_formatter,
    timedelta_formatter,
)
from djed.formatter.size import size_formatter


ID_FORMATTER = 'djed:formatter'


def add_formatter(config, name, callable):
    discr = (ID_FORMATTER, name)

    intr = Introspectable(ID_FORMATTER, discr, name, 'djed-formatter')
    intr['name'] = name
    intr['callable'] = callable
    intr['description'] = callable.__doc__

    def action():
        storage = config.registry.get(ID_FORMATTER)
        if storage is None:
            storage = config.registry[ID_FORMATTER] = {}

        storage[name] = callable

    config.action(discr, action, introspectables=(intr,))


class wrapper(object):

    def __init__(self, request, callable):
        self.request = request
        self.callable = callable

    def __call__(self, *args, **kw):
        return self.callable(self.request, *args, **kw)


class formatters(object):

    def __init__(self, request, default={}):
        self._request = request
        self._f = request.registry.get(ID_FORMATTER, default)
        self._wrappers = {}

    def __getitem__(self, name):
        if name in self._wrappers:
            return self._wrappers[name]

        wrp = self._wrappers[name] = wrapper(self._request, self._f[name])
        setattr(self, name, wrp)

        return wrp

    def __getattr__(self, name):
        if name in self._f:
            return self[name]

        raise AttributeError(name)


def includeme(config):
    settings = config.get_settings()
    settings['pyramid.default_timezone_name'] = settings.get(
        'pyramid.default_timezone_name', 'utc')

    config.add_directive('add_formatter', add_formatter)
    config.add_request_method(formatters, 'format', True, True)
    config.add_formatter('date', date_formatter)
    config.add_formatter('time', time_formatter)
    config.add_formatter('datetime', datetime_formatter)
    config.add_formatter('timedelta', timedelta_formatter)
    config.add_formatter('size', size_formatter)

