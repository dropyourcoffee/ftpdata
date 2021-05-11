from testbench.MockDB import MockDB
from unittest.mock import patch
import pytest
from ftpdata import preset
from ftpdata import create_engine
import os
import mysql
import pandas as pd


ftp_host = os.environ.get("FTP_HOST")
ftp_user = os.environ.get("FTP_USER")
ftp_pkey = os.environ.get("FTP_PKEY")


class TestEngine(MockDB):

    engine = create_engine(ftp_host, ftp_user, pkey=ftp_pkey)
    sess = engine(encoding='cp949')

    def test_1_tabulate_happypath(self):
        with self.mock_db_config:
            cfg = preset.Config('preset_a')

            rawdata_df = None
            for instance in TestEngine.sess.query("/var/ftp/ibk/uploads").filter_by(pattern="fund_pool_20210412"):
                if not instance.name.startswith("isa"):
                    instance.tabulate(cfg, header=None, sep='|')

                    # Make rawdata in df to compare with sql data
                    instance.seek(0,0)
                    rawdata_df = pd.read_csv(instance, sep='|', header=None).drop([0], axis=1)
                    rawdata_df.columns = [col.get('column_name') for col in cfg.sync_db.maps['fund_pool']['column_mapper'] if col is not None]

            compare_df = None
            with mysql.connector.connect(host=cfg.sync_db.host, user=cfg.sync_db.user, password=cfg.sync_db.password) as cnx:
                cursor = cnx.cursor(dictionary=True)
                cursor.execute(f"SELECT * FROM `{cfg.sync_db.database}`.`{cfg.sync_db.maps['fund_pool']['tb_name']}`;")
                compare_df = pd.DataFrame(cursor.fetchall())

            pd.testing.assert_frame_equal(rawdata_df, compare_df)
            cursor.close()


    @pytest.mark.skip("todo")
    def test_2_different_encoding(self):
        pass


    @pytest.mark.skip('todo')
    def test_3_payloads_for_tabulated_instance(self):
        pass
