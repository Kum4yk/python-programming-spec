import json
import functools

def to_json(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        data = func(*args, **kwargs)
        return json.dumps(data)
    return wrapped


@to_json
def magic_func(some=45):
    return {"answer": 42}


if __name__ == "__main__":
    print(magic_func())
