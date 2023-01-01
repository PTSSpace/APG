from typing import List, Any


def flatten(i: List[Any]) -> List[Any]:
    return [index for row in i for index in row]
