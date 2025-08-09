from typing import List
from pathlib import Path

from ..core.utils import apply_mapping
from ..core.utils import load_schema
from ..models.fot import mapped_ids


class FotCoefficient:
    def __init__(self, raw_fot_coefficient: dict, schema: dict):
        self._fot_coefficient = apply_mapping(raw_fot_coefficient, schema)

    def __getitem__(self, field_alias):
        return self._fot_coefficient[field_alias]

    def get_data(self):
        return self._fot_coefficient

    def get_cost_per_unit(self, fot_name: str):
        return self._fot_coefficient[fot_name]['cost_per_unit']

    def get_cost_per_hour(self, fot_name: str):
        return self._fot_coefficient[fot_name]['cost_per_hour']

    def get_staff_count(self, fot_name: str):
        return self._fot_coefficient[fot_name]['staff_count']

    def get_base_salary_rate(self, fot_name: str):
        return self._fot_coefficient[fot_name]['base_salary_rate']


class FotCoefficientRegistry:
    current_dir = Path(__file__).resolve().parent.parent
    schema = load_schema(current_dir / 'schemas/fot_coefficients.schema.json')

    def __init__(self, raw_fot_coefficients: list[dict]):
        self._fot_coefficients = [
            FotCoefficient(raw_fot_coefficient, self.schema)
            for raw_fot_coefficient in raw_fot_coefficients
        ]

    def get_coefficients(self, product_type_id: int):
        for fot_coefficient in self._fot_coefficients:
            if fot_coefficient['type_product'] == mapped_ids[product_type_id]:
                return fot_coefficient

    def get_all(self) -> List[FotCoefficient]:
        return self._fot_coefficients
