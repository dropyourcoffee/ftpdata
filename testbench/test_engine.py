import unittest
import pytest
import os
import rsa
from ftpdata import create_engine
from ftpdata.exceptions import *
from testbench.MockSFTP import MockSFTP


class TestEngine(MockSFTP):

    def test_1_create_engine_sftp(self):
        engine = create_engine(self.mock_sftp_config.url, username=self.mock_sftp_config.username, pkey=self.mock_sftp_config.keyfile)
        engine()

    def test_2_create_engine_ftps(self):
        engine = create_engine(self.mock_sftp_config.url, username=self.mock_sftp_config.username, pkey=self.mock_sftp_config.keyfile)
        sess = engine()
        print([f.name for f in sess.query("/testdata")])

    def test_3_invalid_url(self):
        with pytest.raises(DialectValidationError):
            create_engine("sftp:///s")

    def test_4_auth_info_not_given(self):
        with pytest.raises(AuthenticationError):
            engine = create_engine(self.mock_sftp_config.url)
            engine()

    def test_5_auth_passwd_not_given(self):
        with pytest.raises(AuthenticationError):
            engine = create_engine(self.mock_sftp_config.url, username=self.mock_sftp_config.username)
            engine()

    def test_6_wrong_key_passed(self):
        with pytest.raises(AuthenticationError):
            _, fake_key = rsa.newkeys(2048)
            fake_keyfile = "fake_key.pem"

            with open(fake_keyfile, 'w') as f:
                f.write(fake_key.save_pkcs1().decode('utf8'))
            os.chmod(fake_keyfile, 0o600)
            engine = create_engine(self.mock_sftp_config.url, username=self.mock_sftp_config.username, pkey=fake_keyfile)
            engine()
        os.remove(fake_keyfile)


if __name__ == "__main__":
    unittest.main()
