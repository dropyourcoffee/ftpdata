import paramiko
from ftpdata.QueryResult import QueryResult


class Navigator:
    def __init__(self):
        self.conn.connect(hostname=self.url, port=10021, username=self.username, pkey=paramiko.RSAKey.from_private_key_file(self.pkey))
        self.sess = self.conn.open_sftp()

        self.cli = paramiko.SFTPClient.from_transport(self.conn.get_transport())

    def is_dir(self, filepath):
        return "d" in str(self.cli.lstat(filepath)).split()[0]

    def query(self, p):

        return QueryResult(self.cli, [(p, f) for f in self.sess.listdir(p) if not self.is_dir(f"{p}/{f}") ])