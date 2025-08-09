from typing import List
from pathlib import Path

from ..core.utils import apply_mapping
from ..core.utils import load_schema


class MaterialCoefficient:
    def __init__(self, raw_material_coefficient: dict, schema: dict):
        self._material_coefficient = apply_mapping(raw_material_coefficient, schema)

    def __getitem__(self, field_alias):
        return self._material_coefficient[field_alias]

    def get_data(self):
        return self._material_coefficient


class MaterialCoefficientRegistry:
    current_dir = Path(__file__).resolve().parent.parent
    schema = load_schema(current_dir / 'schemas/material_coefficients.schema.json')

    def __init__(self, raw_material_coefficients: list[dict]):
        self._material_coefficients = [
            MaterialCoefficient(raw_material_coefficient, self.schema)
            for raw_material_coefficient in raw_material_coefficients
        ]

    def get_coefficient(self, field_alias: str) -> float:
        try:
            k = self._material_coefficients[0][field_alias]['coefficient']
            return k if k is not None else 1
        except KeyError:
            return 1

    def get_all(self) -> List[MaterialCoefficient]:
        return self._material_coefficients
