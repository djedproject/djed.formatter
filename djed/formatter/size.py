""" file size formatter """

_size_types = {
    'b': (1.0, 'B'),
    'k': (1024.0, 'KB'),
    'm': (1024.0*1024.0, 'MB'),
    'g': (1024.0*1024.0*1024.0, 'GB'),
}


def size_formatter(request, value, type='k'):
    """Size formatter

    bytes::

        >> v = 1024
        >> request.format.size(v, 'b')
        '1024 B'

    kylobytes::

        >> requst.format.size(v, 'k')
        '1.00 KB'

    megabytes::

        >> request.format.size(1024*768, 'm')
        '0.75 MB'

        >> request.format.size(1024*768*768, 'm')
        '576.00 MB'

    terabytes::

        >> request.format.size(1024*768*768, 'g')
        '0.56 GB'

    """
    if not isinstance(value, (int, float)):
        return value

    f, t = _size_types.get(type, (1024.0, 'KB'))

    if t == 'B':
        return '%.0f %s' % (value / f, t)

    return '%.2f %s' % (value / f, t)
