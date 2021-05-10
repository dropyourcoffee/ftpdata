import os.path
from ftpdata.util import _override_with
import pandas as pd
import mysql


_get_vals = lambda fpm, r: ", ".join([desc.get('fn', lambda x: x)(r[1][idx]) for (idx, desc) in enumerate(fpm) if desc is not None])
_get_cols = lambda fpm: ", ".join([f"`{desc.get('column_name')}`" for desc in fpm if desc is not None])


def tabulate(self, preset=None, header='infer', sep=','):

    target = list(filter(lambda k: self.name.startswith(k), preset.sync_db.maps.keys()))

    if not len(target):
        raise Exception(f"No map match for found file :: {self.name}")
    else:
        target = list(target)[0]

    insert_fn = preset.sync_db.maps[target].get('insert')
    tbl_name = preset.sync_db.maps[target].get('tb_name')
    mapper = preset.sync_db.maps[target].get('column_mapper')

    df = pd.read_csv(self, header=header, sep=sep)

    class Payloads(object):
        def __init__(self):
            self.database = preset.sync_db.database
            self.tbl_name = tbl_name
            self.qcols = _get_cols(mapper)

    p = Payloads()

    with mysql.connector.connect(
        host=preset.sync_db.host,
        user=preset.sync_db.user,
        password=preset.sync_db.password
    ) as cnx:
        cursor = cnx.cursor(dictionary=True)
        for idx, d in enumerate(df.iterrows()):
            p.qvals = _get_vals(mapper, d)
            qstr = insert_fn(p)
            cursor.execute(qstr)
        cursor.close()
        cnx.commit()

tabulated = _override_with(tabulate=tabulate)


class QueryResult:

    def __init__(self, cli, l, encoding='utf-8'):
        self.cli = cli
        self.l = l
        self._i = 0
        self.encoding = encoding

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
        io = tabulated(open(file, encoding=self.encoding))
        return io

    def filter_by(self, pattern=""):
        return QueryResult(self.cli, [(f[0], f[1]) for f in self.l if pattern in f"{f[0]}/{f[1]}"], encoding=self.encoding)
