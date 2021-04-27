import paramiko
from ftpdata.Navigator import Navigator


def create_engine(url, username=None, pwd=None, port=None, pkey=None):
    dialect = url[:7]

    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    setattr(Navigator, "conn", conn)
    setattr(Navigator, "url", url)
    setattr(Navigator, "username", username)
    setattr(Navigator, "pkey", pkey)

    return Navigator

