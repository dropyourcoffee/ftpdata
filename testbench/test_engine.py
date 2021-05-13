import pytest
from ftpdata import create_engine
import os
import mysql
import pandas as pd
import unittest


class TestEngine(unittest.TestCase):

    ftp_host_ip = ""
    ftp_user = ""
    ftp_pwd = ""

    def test_1_1_create_engine_ftp(self):
        engine = create_engine(f"ftp://{TestEngine.ftp_host_ip}", username=TestEngine.ftp_user, pwd=TestEngine.ftp_pwd)
        sess = engine()
        print(list(sess.query("/")))

