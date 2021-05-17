from ftpdata.util import unzip


def test_unzip():

    dict_obj = {
        "a": "foo",
        "b": "bar",
        "c": "baz"
    }
    keys = tuple(dict_obj.keys())
    values = tuple(dict_obj.values())

    k, v = unzip(dict_obj)

    assert(keys == k)
    assert(values == v)

