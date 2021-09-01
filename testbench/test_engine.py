import unittest
import pytest
import os
import rsa
import re
from ftpdata import create_engine, Directory
from ftpdata.exceptions import DialectValidationError, AuthenticationError, SSHError
from testbench.MockSFTP import MockSFTP


class TestEngine(MockSFTP):

    def test_01_create_engine_sftp(self):
        engine = create_engine(self.mock_sftp_config.url, username=self.mock_sftp_config.username, pkey=self.mock_sftp_config.keyfile)
        engine()

    def test_02_create_engine_ftps(self):
        engine = create_engine(self.mock_sftp_config.url, username=self.mock_sftp_config.username, pkey=self.mock_sftp_config.keyfile)
        sess = engine()

        class TargetDirectory(Directory):
            __path__ = '/testdata'

        self.assertEqual([f.name for f in sess.query(TargetDirectory)],
                         ['sample.csv']
                         )

    def test_03_path_not_defined_in_target_directory(self):

        engine = create_engine(self.mock_sftp_config.url, username=self.mock_sftp_config.username, pkey=self.mock_sftp_config.keyfile)
        sess = engine()

        class TargetDirectory(Directory):
            pass

        with pytest.raises(AttributeError):
            [f.name for f in sess.query(TargetDirectory).filter_by(re.compile('^sample'))]

    def test_04_invalid_url(self):
        with pytest.raises(DialectValidationError):
            create_engine("sftp:///s")

    def test_05_auth_info_not_given(self):
        with pytest.raises(AuthenticationError):
            engine = create_engine(self.mock_sftp_config.url)
            engine()

    def test_06_auth_passwd_not_given(self):
        with pytest.raises(AuthenticationError):
            engine = create_engine(self.mock_sftp_config.url, username=self.mock_sftp_config.username)
            engine()

        with pytest.raises(SSHError):
            create_engine(self.mock_sftp_config.url, username=self.mock_sftp_config.username, pkey=1)

    def test_07_wrong_key_passed(self):
        with pytest.raises(AuthenticationError):
            _, fake_key = rsa.newkeys(2048)
            fake_keyfile = "fake_key.pem"

            with open(fake_keyfile, 'w') as f:
                f.write(fake_key.save_pkcs1().decode('utf8'))
            os.chmod(fake_keyfile, 0o600)
            engine = create_engine(self.mock_sftp_config.url, username=self.mock_sftp_config.username, pkey=fake_keyfile)
            engine()
        os.remove(fake_keyfile)

    def test_08_spec_filter_by_str(self):
        engine = create_engine(self.mock_sftp_config.url, username=self.mock_sftp_config.username, pkey=self.mock_sftp_config.keyfile)
        sess = engine()

        class TargetDirectory:
            __path__ = '/testdata'

        files = [f.name for f in sess.query(TargetDirectory).filter_by("sample")]

        self.assertEqual(files,
                         ['sample.csv']
                         )

    def test_09_spec_filter_by_regex(self):
        engine = create_engine(self.mock_sftp_config.url, username=self.mock_sftp_config.username, pkey=self.mock_sftp_config.keyfile)
        sess = engine()

        class TargetDirectory(Directory):
            __path__ = '/testdata'

        files = [f.name for f in sess.query(TargetDirectory).filter_by(re.compile('^sample'))]

        self.assertEqual(files,
                         ['sample.csv']
                         )


    def test_10_inline_fn(self):
        engine = create_engine(self.mock_sftp_config.url, username=self.mock_sftp_config.username, pkey=self.mock_sftp_config.keyfile)
        sess = engine()

        class TargetDirectory(Directory):
            __path__ = '/testdata'

            @staticmethod
            def fn(fstat):
                fstat.filesize_s = f"{fstat.st_size} bytes"
                return fstat

        files = [f.filesize_s for f in sess.query(TargetDirectory).filter_by("sample")]

        self.assertEqual(files,
                         ['41 bytes']
                         )

    def test_11_add_file(self):
        engine = create_engine(self.mock_sftp_config.url, username=self.mock_sftp_config.username, pkey=self.mock_sftp_config.keyfile)

        sess = engine()

        class TargetDirectory(Directory):
            __path__ = '/testdata'

        new_file = TargetDirectory('./newfile')
        sess.add(new_file)

        files = [f.name for f in sess.query(TargetDirectory).filter_by("new")]

        self.assertEqual(files,
                         ['newfile']
                         )

if __name__ == "__main__":
    unittest.main()
