import paramiko
from ftpdata.QueryResult import QueryResult
from ftpdata.exceptions import NoSuchDirectoryError


class Navigator:
    def __init__(self, encoding='utf-8'):
        self.conn.connect(hostname=self.url, port=10021, username=self.username, pkey=paramiko.RSAKey.from_private_key_file(self.pkey))
        self.sess = self.conn.open_sftp()

        self.cli = paramiko.SFTPClient.from_transport(self.conn.get_transport())
        self.encoding = encoding

    def is_dir(self, filepath):
        return "d" in str(self.cli.lstat(filepath)).split()[0]

    def query(self, p):

        ls = None
        try:
            ls = self.sess.listdir(p)
        except FileNotFoundError:
            raise NoSuchDirectoryError(f"'{p}' could not be found from the source.")

        return QueryResult(self.cli, [(p, f) for f in ls if not self.is_dir(f"{p}/{f}")], encoding=self.encoding)
