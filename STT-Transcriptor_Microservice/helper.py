# Note: abc = abstract base classes
from collections.abc import Mapping
from typing import Any, List


class Read_Only_Dict(Mapping):
    def __init__(self, data):
        self._data = data

    def __setitem__(self, key, data):
        self._data[key] = data

    def __getitem__(self, key):
        return self._data[key]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)


def chunk(xs: List[Any], size: int) -> List[List[Any]]:
    return [xs[i : i + size] for i in range(0, len(xs), size)]
