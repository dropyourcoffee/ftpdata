import os.path

class QueryResult:

    def __init__(self, cli, l):
        self.cli = cli
        self.l = l
        self._i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._i >= len(self.l):
            raise StopIteration

        ret = self.l[self._i]
        self._i += 1
        (path, file) = ret

        landing = f"./{file}"
        if not os.path.isfile(landing):
            self.cli.get(path+"/"+file, landing)
        return open(file)

    def filter_by(self, pattern=""):
        return QueryResult(self.cli, [(f[0], f[1]) for f in self.l if pattern in f"{f[0]}/{f[1]}"])