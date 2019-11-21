from statistics import mean
from typing import List, Any, Tuple, Dict


def is_float(value):
    try:
        float(value)
        return True
    except Exception:
        return False


def create_statistic(results: List[List[Tuple[str, Any]]], statistics=(mean, min, max)) -> Dict[str, Any]:
    data = dict()
    for result in results:
        for key, value in result:
            data.setdefault(key, []).append(value)

    final_data = dict()
    for key, values in data.items():
        # all values are numbers
        if all(map(is_float, values)):
            for stat in statistics:
                final_data[f'{key}_{stat.__name__}'] = stat(map(float, values))
        # otherwise all values must be equals across the measurements
        elif all(map(lambda x: x == values[0], values)):
            final_data[key] = values[0]
        else:
            raise ValueError("Unexpected values")
    return final_data
