from testbench.MockDB import MockDB
from unittest.mock import patch
from preset_a import preset
from ftpdata import create_engine
import os
import pandas as pd


ftp_host = os.environ.get("FTP_HOST")
ftp_user = os.environ.get("FTP_USER")
ftp_pkey = os.environ.get("FTP_PKEY")

class TestEngine(MockDB):

    engine = create_engine(ftp_host, ftp_user, pkey=ftp_pkey)
    sess = engine()

    def test_1_tabulate_happypath(self):
        with self.mock_db_config:

            for instance in TestEngine.sess.query("/var/ftp/ibk/uploads").filter_by(pattern="isa_fund_pool_"):
                if "20210412" in instance.name:
                    # print(pd.read_csv(instance, sep="|", engine='c', header=None))
                    instance.tabulate(sep="|", preset=preset)

    def test_2_tabulate_onduplicate(self):
        with self.mock_db_config:

            for instance in TestEngine.sess.query("/var/ftp/ibk/uploads").filter_by(pattern="isa_fund_pool_"):
                if "20210412" in instance.name:
                    # print(pd.read_csv(instance, sep="|", engine='c', header=None))
                    instance.tabulate(sep="|", preset=preset, upsert_duplicate=True)




