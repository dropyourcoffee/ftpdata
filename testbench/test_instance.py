import pytest
from ftpdata import create_engine
import os
import pandas as pd
import dotenv
dotenv.load_dotenv(override=True)


class TestInstance:

    ftp_host = os.environ.get("FTP_HOST")
    ftp_port = os.environ.get("FTP_PORT")
    ftp_user = os.environ.get("FTP_USER")
    ftp_pkey = os.environ.get("FTP_PKEY")

    engine = create_engine(f"sftp://{ftp_host}:{ftp_port}", ftp_user, pkey=ftp_pkey)
    sess = engine()

    def test_1_happypath(self):

        rawdata_df = None
        for instance in TestInstance.sess.query("/var/ftp/ibk/uploads").filter_by(pattern="isa_fund_pool_20210412"):
            raw_df = pd.read_csv(instance.get(), sep='|', encoding='cp949')



    @pytest.mark.skip("todo")
    def test_2_different_encoding(self):
        pass
