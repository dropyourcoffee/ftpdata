import os

class Directory:

    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.split(filepath)[-1]
