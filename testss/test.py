
if __name__ == "__main__":
    import pandas as pd
    import os
    from ftpdata import create_engine

    host = os.environ["HOST"]
    username = "username"
    pkey= "../mykey.pem"

    engine = create_engine(host, username=username, pkey=pkey)
    sess = engine()

    for instance in sess.query("/").filter_by(pattern=".csv"):
        data = pd.read_csv(instance, engine="c")
        print(data)


