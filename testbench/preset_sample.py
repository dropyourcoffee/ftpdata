import pandas as pd
from ftpdata.preset import tabulate_preset

mapper = [
    None,
    {"column_name": "id",  "fn": lambda v:f"'{v}'"},
    {"column_name": "text",  "fn": lambda v:str(v)},
    {"column_name": "int", "fn": lambda v:f"'{v}'"},
]


@tabulate_preset(mapper)
def updateAll(self, **kwargs):
    return f"INSERT INTO `{self.tbl_name}` ({self.qcols}) VALUES ({self.qvals})"


preset = {
    'sync_db': {
        'host': "localhost",
        'user': "user",
        'password': "password",
        'database': "testdb",
        'maps' : {
            'fund_pool':{
                'tb_name': 'test_table',
                'column_mapper': mapper,
                'insert': updateAll,
            }
        },
    },
}
