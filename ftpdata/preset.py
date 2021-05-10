from importlib import import_module
from collections import namedtuple
from ftpdata.exceptions import PresetValidationError


def Config(filename):
    cfg = import_module(filename, package=None)

    if not hasattr(cfg, 'preset'):
        raise PresetValidationError(f"preset must be defined in the preset file, {filename}")

    if 'sync_db' not in cfg.preset.keys():
        raise PresetValidationError(f"Key Not Found in the preset file:: 'sync_db'")

    # Make 'Config' type object and map all (key value) sets into attribute within itself.
    return type("Config", (), {
        'sync_db': namedtuple('sync_db', cfg.preset['sync_db'].keys())(*cfg.preset['sync_db'].values())
    })()

def tabulate_preset(fpm):
    def decorator(fn):
        def inner(*args, **kwargs):
            return fn(*args, **kwargs)
        return inner
    return decorator


def render_query_values(r, mapper):
    return ", ".join( [m.get('fn', lambda x: x)(r[1][idx]) for (idx, m) in enumerate(mapper) if m is not None])

def render_query_columns(r, mapper):
    return ", ".join([f"`{m.get('column_name')}`" for m in mapper if m is not None])

