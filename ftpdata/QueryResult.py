import os.path
import paramiko.sftp_client
import re


_get_vals = lambda fpm, r: ", ".join([desc.get('fn', lambda x: x)(r[idx]) for (idx, desc) in enumerate(fpm) if desc is not None])
_get_cols = lambda fpm: ", ".join([f"`{desc.get('column_name')}`" for desc in fpm if desc is not None])


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
        inspect_fn = pattern.match if isinstance(pattern, re.Pattern) else lambda s: bool(pattern in s)

        return QueryResult(self.cli, [(f[0], f[1]) for f in self.l if inspect_fn(f[1])], encoding=self.encoding)
