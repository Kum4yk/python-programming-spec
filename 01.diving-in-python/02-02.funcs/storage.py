import argparse
import os
import tempfile
import json


def check_dir_is_exist(path):
    return os.path.exists(path)


def get_dict_from_file(path):
    with open(path, "r") as file:
        dict_from_file = json.loads(file.read())
    return dict_from_file


def write_dict_in_file(path, in_dict):
    with open(path, "w") as file:
        file.write(json.dumps(in_dict))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--key")
    parser.add_argument("--val")
    args = parser.parse_args()

    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')

    if not check_dir_is_exist(storage_path):
        if args.val is None:
            print(None)
        else:
            dict_data = {args.key: [args.val]}
            write_dict_in_file(storage_path, dict_data)
    else:
        dict_data: dict = get_dict_from_file(storage_path)
        result = dict_data.get(args.key, [])
        if args.val is None:
            print(*result, sep=", ")
        else:
            result.append(args.val)
            dict_data.update({args.key: result})
            write_dict_in_file(storage_path, dict_data)
