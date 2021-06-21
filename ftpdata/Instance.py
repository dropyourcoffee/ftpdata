
class Instance:

    def __init__(self, cli, path, file):
        self.cli = cli
        self.path = path
        self.file = file

    def read(self):

        self.cli.get(self.path + "/" + self.file, f"./{self.file}")
        return open(f"./{self.file}").read()
