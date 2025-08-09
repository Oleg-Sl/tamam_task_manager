from typing import List, Dict, Any
from pathlib import Path

from ..core.utils import apply_mapping
from ..core.utils import load_schema


mapped_ids = {
    158: 4741,
    165: 4743,
    189: 4745,
    167: 4749,
    172: 4747,
    188: 4755,
    186: 4751,
    150: 4753,
    162: 4757
}


class Fot:
    def __init__(self, raw_fot: dict, schema: dict):
        self.schema = schema
        self.id = raw_fot['id']
        self.entity_type_id = raw_fot['entityTypeId']
        self._raw_fot = raw_fot
        self._data = apply_mapping(raw_fot, schema)
        self.summary_cost = self._data['summary_cost']
        self.field_template_potochka = self.schema['is_template_potochka']
        self._data.pop('summary_cost')
        self._data.pop('is_template_potochka')
        self.update_field(schema)

    def __getitem__(self, field: str) -> Any:
        return self._data.get(field, self._raw_fot.get(field))

    def __contains__(self, field: str) -> bool:
        return field in self._data or field in self._raw_fot

    def __iter__(self):
        return iter(self._data)

    def get_field_template_potochka(self):
        return self.field_template_potochka

    def get_field(self, field_alias: str) -> str | Dict:
        return self.schema[field_alias]

    def update_field(self, schema):
        for field_key, field_data in schema.items():
            if isinstance(field_data, dict):
                self._data[field_key]['title'] = field_data['title']

    def get_data(self) -> Dict:
        return self._data

    def get_names(self) -> str:
        for fot_name in self._data.keys():
            yield fot_name


class FotRegistry:
    current_dir = Path(__file__).resolve().parent.parent
    schema = load_schema(current_dir / 'schemas/fot.schema.json')

    def __init__(self, raw_fots: list[dict]):
        self._fots = [Fot(raw_fot, self.schema) for raw_fot in raw_fots]

    def get(self, fot_id: int):
        for fot in self._fots:
            if fot.id == fot_id:
                return fot

    def filter(self, filter_data: dict) -> Fot | None:
        for fot in self._fots:
            for key, val in filter_data.items():
                if key not in fot or fot[key] != val:
                    break
            else:
                return fot

    def get_all(self) -> List[Fot]:
        return self._fots
