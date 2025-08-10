import bisect
from datetime import datetime
from typing import List
from pathlib import Path

try:
    from django.conf import settings
    BASE_DIR = settings.BASE_DIR
except ImportError:
    settings = None

from ..core.utils import apply_mapping
from ..core.utils import load_schema
from ..core.utils import bisect_left_with_key


class MaterialPrice:
    def __init__(self, raw_material: dict, schema: dict):
        self._material = apply_mapping(raw_material, schema)
        self.date = datetime.strptime(self._material['date_of_price_validity'], '%Y-%m-%dT%H:%M:%S%z')

    def __getitem__(self, field_alias):
        return self._material[field_alias]

    def __lt__(self, other_date: datetime):
        return self.date < other_date

    def get_data(self):
        return self._material


class MaterialPriceRegistry:
    current_dir = Path(__file__).resolve().parent.parent
    schema = load_schema(current_dir / 'schemas/material_prices.schema.json')

    def __init__(self, raw_materials: list[dict]):
        self._materials = [MaterialPrice(raw_material, self.schema) for raw_material in raw_materials]
        self._materials.sort(key=lambda el: el.date)

    def get_all(self) -> List[MaterialPrice]:
        return self._materials

    def get_closest_before(self, target_date: datetime) -> MaterialPrice:
        ind = bisect_left_with_key(self._materials, target_date, key=lambda el: el.date)
        return self._materials[ind] if ind < len(self._materials) else self._materials[-1]

    def get_last(self) -> MaterialPrice:
        return self._materials[-1]
