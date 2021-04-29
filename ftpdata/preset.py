from importlib import import_module
from collections import namedtuple


def Config(filename):
    cfg = import_module(filename, package=None)

    # Make 'Config' type object and map all (key value) sets into attribute within itself.
    return type("Config", (), {
        'sync_db': namedtuple('sync_db', cfg.preset['sync_db'].keys())(*cfg.preset['sync_db'].values())
    })()

