class FileReader:
    def __init__(self, path):
        self.path = path

    def read(self):
        try:
            text = open(self.path, "r").read()  # bad practice style
        except FileNotFoundError:
            text = ""
        return text

    @staticmethod
    def read_text_from_file(path):
        try:
            text = open(path, "r").read()  # bad practice style
        except FileNotFoundError:
            text = ""
        return text


if __name__ == "__main__":
    __text = FileReader.read_text_from_file("some")
    print(__text)
