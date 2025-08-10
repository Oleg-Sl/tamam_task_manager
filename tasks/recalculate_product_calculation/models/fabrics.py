from typing import List, Dict, Any, Union
from pathlib import Path

from ..core.utils import apply_mapping
from ..core.utils import load_schema
from ..config.constants import ID_FABRIC


class Fabric:
    def __init__(self, raw_data: dict, schema: dict):
        self.schema = schema
        self.id = raw_data['id']
        self.entity_type_id = ID_FABRIC
        self._raw_data = raw_data
        self._data = apply_mapping(raw_data, schema)

    def __getitem__(self, field: str) -> Any:
        return self._data.get(field, self._raw_data.get(field))

    def __contains__(self, field: str) -> bool:
        return field in self._data or field in self._raw_data

    def __iter__(self):
        return iter(self._data)

    # 1: `${this.getFabricName1()} (${this.getFabricCollection1()} - ${this.getFabricPrice1()})`,


class FabricRegistry:
    current_dir = Path(__file__).resolve().parent.parent
    schema = load_schema(current_dir / 'schemas/fabric.schema.json')

    def __init__(self, raw_data: List[Dict]):
        self._raw_data = raw_data
        self._fabrics = [Fabric(fabric, self.schema) for fabric in raw_data]

    def get(self, fabric_id: int):
        for fabric in self._fabrics:
            if fabric_id and fabric.id == int(fabric_id):
                return fabric

    def get_all(self) -> List[Fabric]:
        return self._fabrics

    def filter(self, filter_data: dict) -> Union[Fabric, None]:
        for fabric in self._fabrics:
            if all(key in fabric and fabric[key] == val for key, val in filter_data.items()):
                return fabric
