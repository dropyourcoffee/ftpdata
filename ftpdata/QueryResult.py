import os.path
from ftpdata.util import _override_with
import paramiko.sftp_client
import pandas as pd
import mysql
import re


_get_vals = lambda fpm, r: ", ".join([desc.get('fn', lambda x: x)(r[idx]) for (idx, desc) in enumerate(fpm) if desc is not None])
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
        p.vals = {}
        for idx, (_, d) in enumerate(df.iterrows()):
            p.qvals = _get_vals(mapper, d)
            p.vals = dict(zip([m.get('column_name') for m in mapper if m is not None],
                              [d for idx, d in enumerate(d) if mapper[idx] is not None]
                              ))
            qstr = insert_fn(p)
            cursor.execute(qstr)
        cursor.close()
        cnx.commit()

tabulated = _override_with(tabulate=tabulate)

class FileInst:
    def __init__(self, sess, path, fname):
        self.sess = sess
        self.path = path
        self.name = fname

    def get(self, localpath=None):

        if localpath is None:
            localpath = f"./{self.name}"

        abs_fp = f"{self.path}/{self.name}" if self.path != "/" else f"/{self.name}"

        if isinstance(self.sess, paramiko.sftp_client.SFTPClient):
            self.sess.get(abs_fp, localpath=localpath)
        else:
            if not os.path.isfile(localpath):
                with open(localpath, "wb") as fp:
                    self.sess.retrbinary(f"RETR {abs_fp}", fp.write)

        return localpath


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

        return FileInst(self.cli, path, file)

    def filter_by(self, pattern=""):

        # if pattern is regexp, use '.match()' otherwise check include
        inspect_fn = pattern.math if isinstance(pattern, re.Pattern) else lambda s: bool(pattern in s)

        return QueryResult(self.cli, [(f[0], f[1]) for f in self.l if pattern in f[1]], encoding=self.encoding)
