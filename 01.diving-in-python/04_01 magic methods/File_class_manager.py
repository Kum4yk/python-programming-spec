import os
import tempfile


class File:
    __counter = 0

    def __init__(self, path_to_file):
        self.path = path_to_file
        File.__counter += 1
        if not os.path.exists(path_to_file):
            self.write("")

    def read(self):
        with open(self.path, "r") as file:
            return file.read()

    def write(self, text):
        with open(self.path, "w") as file:
            file.write(text)

    def __add__(self, other):
        new_path = os.path.join(tempfile.gettempdir(), f"temp_{File.__counter}.txt")
        res = File(new_path)
        res.write(self.read() + other.read())
        return res

    def __str__(self):
        return self.path

    def __iter__(self):
        return open(self.path, "r")


if __name__ == "__main__":
    some_file = File("my_file")
    some_text = "\n".join(map(str, range(10)))
    some_file.write(some_text)
    for some in some_file:
        print(ascii(some))
