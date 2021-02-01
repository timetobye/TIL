import os
from pathlib import Path


def get_parent_path():
    current_path = os.getcwd()
    path_object = Path(current_path)

    parent_path = str(path_object.parent)

    return parent_path


if __name__ == "__main__":
    result = get_parent_path()
    print(result)
    print(os.getcwd())
