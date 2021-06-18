import paramiko
from ftpdata.Navigator import Navigator
from ftpdata.exceptions import *
import re
from ftplib import FTP

valid_url = re.compile("^(ftp|sftp):\/\/[a-z0-9]+([\-\.]{1}[a-z0-9]+)*(:[0-9]{2,5})?(\/.*)?$")


def create_engine(url, username=None, pwd=None, port=None, pkey=None):

    if not valid_url.match(url):
        raise DialectValidationError(f"URL validation failed: {url}")

    dialect, host_port = url.split("://")

    # Assign port if specified
    s = host_port.split(":")
    host = s[0]
    port = s[1] if len(s) > 1 else None

    if dialect == "ftp":
        port = 21 if port is None else int(port)

        def init(_):
            ftp = FTP()
            ftp.connect(host, port=port)
            if username is not None and pwd is not None:
                ftp.login(username, passwd=pwd)
            else:
                raise AuthenticationError("Authentication Failed.")
            return ftp
        setattr(Navigator, "init", init)

    elif dialect == "sftp":
        port = 22 if port is None else int(port)

        try:
            if pkey is not None:
                paramiko.RSAKey.from_private_key_file(pkey)
        except Exception:
            raise SSHError(f"SSH Error while reading key file :: check your key file, {pkey}")

        def init(_):

            if username is None or (pwd is None and pkey is None):
                raise AuthenticationError("Authentication is not given")

            conn = paramiko.SSHClient()
            conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                conn.connect(hostname=host, port=port, username=username,
                             pkey=paramiko.RSAKey.from_private_key_file(pkey))
            except paramiko.ssh_exception.AuthenticationException:
                raise AuthenticationError(f"Authentication failed :: {pkey}")

            # cli = paramiko.SFTPClient.from_transport(conn.get_transport())
            return conn.open_sftp()
        setattr(Navigator, "init", init)
    else:
        raise DialectValidationError(f"Invalid Dialect, '{dialect}'")

    return Navigator

