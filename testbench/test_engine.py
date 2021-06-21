import unittest
import pytest
import os
import rsa
import re
from ftpdata import create_engine
from ftpdata.exceptions import DialectValidationError, AuthenticationError, SSHError
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

        with pytest.raises(SSHError):
            create_engine(self.mock_sftp_config.url, username=self.mock_sftp_config.username, pkey=1)


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

    def test_7_spec_filter_by_str(self):
        engine = create_engine(self.mock_sftp_config.url, username=self.mock_sftp_config.username, pkey=self.mock_sftp_config.keyfile)
        sess = engine()
        files = [f.name for f in sess.query("/testdata").filter_by("sample")]
        self.assertEqual(files, ['sample.csv'])

    def test_8_spec_filter_by_regex(self):
        engine = create_engine(self.mock_sftp_config.url, username=self.mock_sftp_config.username, pkey=self.mock_sftp_config.keyfile)
        sess = engine()
        files = [f.name for f in sess.query("/testdata").filter_by(re.compile('^sample'))]
        self.assertEqual(files, ['sample.csv'])


if __name__ == "__main__":
    unittest.main()
