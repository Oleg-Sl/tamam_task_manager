import json
import pathlib


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
