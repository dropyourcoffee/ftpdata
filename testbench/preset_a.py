import pandas as pd
from ftpdata.preset import render_query_values as qvals
from ftpdata.preset import render_query_columns as qcols

fund_pool_mapper = [
    None,
    {"column_name": "IBK_CD",  "fn": lambda v:str(v)},
    {"column_name": "FUND_NM",  "fn": lambda v:f"'{v}'"},
    {"column_name": "INTT_FUND_CD",  "fn": lambda v:f"'{v}'"},
    {"column_name": "BASE_FUND_CD",  "fn": lambda v:f"'{v}'"},
    {"column_name": "INTERNET_YN",  "fn": lambda v:f"'{v}'"},
    {"column_name": "BASIC_YN",  "fn": lambda v:f"'{v}'"},
    {"column_name": "PERSONAL_YN",  "fn": lambda v:f"'{v}'"},
    {"column_name": "FUND_RISK_REVERSE_LEVL_CD",  "fn": lambda v:str(v)},
    {"column_name": "FUND_RISK_LEVL_NM",  "fn": lambda v:f"'{v}'"} # [9]
]

get_vals = lambda r, fpm : ", ".join([desc.get('fn', lambda x: x)(r[1][idx]) for (idx, desc) in enumerate(fpm) if desc is not None])
get_cols = lambda r, fpm : ", ".join([f"`{desc.get('column_name')}`" for desc in fpm if desc is not None])

def upsertAll(fileIO, mapper):
    d = pd.read_csv(fileIO, engine="c", sep="|", header=None)

    tbl_name = "ibk_fund_pool"

    queries = [
        f"INSERT INTO `{tbl_name}` ({qcols(r, fund_pool_mapper)}) VALUES ({qvals(r, fund_pool_mapper)})"
        for r in d.iterrows()
    ]
    print('vals cols')

    return queries

preset = {
    'sync_db': {
        'host': "10.0.0.5",
        'port': 3306,
        'schema': "qraft_zeroin",
        'upsertAll': upsertAll,
    },

}

