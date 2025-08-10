import bisect
import json
import pathlib


def bisect_left_with_key(a, x, key=None):
    if key is None:
        return bisect.bisect_left(a, x)
    keys = [key(item) for item in a]
    return bisect.bisect_left(keys, x)


def load_schema(f_path: pathlib.Path):
    with open(f_path, encoding='cp1251') as f:
        return json.load(f)


def apply_mapping(data, mapping):
    if isinstance(mapping, dict):
        return {
            key: apply_mapping(data, submapping)
            if key not in ["type", "number"]
            else submapping
            for key, submapping in mapping.items()
        }
    elif isinstance(mapping, list):
        return [
            apply_mapping(data, submapping)
            for submapping in mapping
        ]
    return data.get(mapping)


# def apply_mapping(data, mapping):
#     if isinstance(mapping, dict):
#         return {
#             key: apply_mapping(data, submapping)
#             if isinstance(submapping, dict)
#             else data.get(submapping)
#             for key, submapping in mapping.items()
#         }
#     return data.get(mapping)
