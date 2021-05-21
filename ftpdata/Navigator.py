import paramiko
from ftpdata.QueryResult import QueryResult
from ftpdata.exceptions import NoSuchDirectoryError


def _is_sftp(sess):
    return isinstance(sess, paramiko.sftp_client.SFTPClient)


class Navigator:
    def __init__(self, encoding='utf-8'):
        self.sess = self.init()

        if _is_sftp(self.sess):
            self.ls = self.sess.listdir
        else:
            def _get_fname(fn):
                def inner(*args, **kwargs):
                    return map(lambda abs_path: abs_path.split("/")[-1], fn(*args, **kwargs))
                return inner

            self.ls = _get_fname(self.sess.nlst)
        self.encoding = encoding

    def _is_dir(self, filepath):
        if _is_sftp(self.sess):
            return "d" in str(self.sess.lstat(filepath)).split()[0]
        else:
            try:
                self.sess.cwd(filepath)
                self.sess.cwd("..")
                return True
            except Exception:
                return False

    def query(self, p):

        try:
            ls = self.ls(p)
        except FileNotFoundError:
            raise NoSuchDirectoryError(f"'{p}' could not be found from the source.")

        return QueryResult(self.sess, [(p, f) for f in ls if not self._is_dir(f"{p}/{f}")], encoding=self.encoding)
