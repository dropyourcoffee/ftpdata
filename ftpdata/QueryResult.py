import os.path
from ftpdata.util import _override_with
import pandas as pd


_get_vals = lambda fpm, r: ", ".join([desc.get('fn', lambda x: x)(r[1][idx]) for (idx, desc) in enumerate(fpm) if desc is not None])
_get_cols = lambda fpm: ", ".join([f"`{desc.get('column_name')}`" for desc in fpm if desc is not None])


def tabulate(self, preset=None, sep=','):

    target = list(filter(lambda k: self.name.startswith(k), preset.sync_db.maps.keys()))

    if not len(target):
        raise Exception("no map match for found file")
    else:
        target = list(target)[0]

    insert_fn = preset.sync_db.maps[target].get('insert')
    tbl_name = preset.sync_db.maps[target].get('tb_name')
    mapper = preset.sync_db.maps[target].get('column_mapper')

    df = pd.read_csv(self, sep=sep)

    class Payloads(object):
        def __init__(self):
            self.tbl_name = tbl_name
            self.qcols = _get_cols(mapper)

    p = Payloads()

    for idx, d in enumerate(df.iterrows()):
        p.qvals = _get_vals(mapper, d)
        ql = insert_fn(p)
        print(ql)

tabulated = _override_with(tabulate=tabulate)


class QueryResult:

    def __init__(self, cli, l):
        self.cli = cli
        self.l = l
        self._i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._i >= len(self.l):
            raise StopIteration

        ret = self.l[self._i]
        self._i += 1
        (path, file) = ret

        landing = f"./{file}"
        if not os.path.isfile(landing):
            self.cli.get(path+"/"+file, landing)
        io = tabulated(open(file))
        return io

    def filter_by(self, pattern=""):
        return QueryResult(self.cli, [(f[0], f[1]) for f in self.l if pattern in f"{f[0]}/{f[1]}"])