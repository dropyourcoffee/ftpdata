from importlib import import_module
from collections import namedtuple


def Config(filename):
    cfg = import_module(filename, package=None)

    # Make 'Config' type object and map all (key value) sets into attribute within itself.
    return type("Config", (), {
        'sync_db': namedtuple('sync_db', cfg.preset['sync_db'].keys())(*cfg.preset['sync_db'].values())
    })()


def render_query_values(r, mapper):
    return ", ".join( [m.get('fn', lambda x: x)(r[1][idx]) for (idx, m) in enumerate(mapper) if m is not None])

def render_query_columns(r, mapper):
    return ", ".join([f"`{m.get('column_name')}`" for m in mapper if m is not None])

