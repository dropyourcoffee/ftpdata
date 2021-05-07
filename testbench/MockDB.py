import mysql
import os
import dotenv
from mysql.connector import errorcode
from unittest import TestCase
from unittest.mock import patch
from preset_a import preset
dotenv.load_dotenv(override=True)
print(os.environ)

TEST_DB_HOST = os.environ.get("TEST_DB_HOST")
TEST_DB_USER = os.environ.get("TEST_DB_USER")
TEST_DB_PWD = os.environ.get("TEST_DB_PWD")
TEST_DB_PORT = os.environ.get("TEST_DB_PORT")
TEST_DB_SCHEMA = os.environ.get("TEST_DB_SCHEMA")


class MockDB(TestCase):

    @classmethod
    def setUpClass(cls):
        cnx = mysql.connector.connect(
            host=TEST_DB_HOST,
            user=TEST_DB_USER,
            password=TEST_DB_PWD,
            port=TEST_DB_PORT
        )
        cursor = cnx.cursor(dictionary=True)
        try:
            cursor.execute("DROP DATABASE {}".format(TEST_DB_SCHEMA))
            cursor.close()
            # print("DB dropped")
        except mysql.connector.Error as err:
            print("{}{}".format(TEST_DB_SCHEMA, err))

        cursor = cnx.cursor(dictionary=True)
        # create database
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(TEST_DB_SCHEMA))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
        cnx.database = TEST_DB_SCHEMA

        # create table

        query = """CREATE TABLE `test_table` (
                    `id` varchar(30) NOT NULL PRIMARY KEY ,
                    `text` text NOT NULL,
                    `int` int NOT NULL
                  )"""
        try:
            cursor.execute(query)
            cnx.commit()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("test_table already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

        # insert data

        insert_data_query = """INSERT INTO `test_table` (`id`, `text`, `int`) VALUES
                              ('1', 'test_text', 1),
                              ('2', 'test_text_2',2)"""
        try:
            cursor.execute(insert_data_query)
            cnx.commit()
        except mysql.connector.Error as err:
            print("Data insertion to test_table failed \n" + err)
        cursor.close()
        cnx.close()

        testconfig ={
            'host': TEST_DB_HOST,
            'user': TEST_DB_USER,
            'password': TEST_DB_PWD,
            'database': TEST_DB_SCHEMA
        }
        cls.mock_db_config = patch.dict(preset['sync_db'], testconfig)

    # @classmethod
    # def tearDownClass(cls):
    #     cnx = mysql.connector.connect(
    #         host=TEST_DB_HOST,
    #         user=TEST_DB_USER,
    #         password=TEST_DB_PWD
    #     )
    #     cursor = cnx.cursor(dictionary=True)
    #
    #     # drop test database
    #     try:
    #         cursor.execute("DROP DATABASE {}".format(TEST_DB_SCHEMA))
    #         cnx.commit()
    #         cursor.close()
    #     except mysql.connector.Error as err:
    #         print("Database {} does not exists. Dropping db failed".format(TEST_DB_SCHEMA))
    #     cnx.close()
