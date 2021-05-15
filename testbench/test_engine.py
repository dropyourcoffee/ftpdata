import unittest
from ftpdata import create_engine
from testbench.MockSFTP import MockSFTP


class TestEngine(MockSFTP):

    def test_1_create_engine_sftp(self):
        engine = create_engine(self.mock_sftp_config.url, username=self.mock_sftp_config.username, pkey=self.mock_sftp_config.keyfile)
        engine()

    def test_2_create_engine_ftps(self):
        engine = create_engine(self.mock_sftp_config.url, username=self.mock_sftp_config.username, pkey=self.mock_sftp_config.keyfile)
        sess = engine()
        print([f.name for f in sess.query("/testdata")])


if __name__ == "__main__":
    unittest.main()
