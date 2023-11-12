import inspect
from typing import Any


def get_path_to_class(class_: Any) -> str:
    return inspect.getfile(class_.__class__)
