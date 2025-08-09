from typing import List
from pathlib import Path

from ..core.utils import apply_mapping
from ..core.utils import load_schema


PRODUCT_TYPE_FOR_QUERY = {
    'sofa': 4777,
    'armchair': 4779,
    'bed': 4781,
    'pouf': 4783,
    'msp': 4785,
    'nightstand': 4787,
    'table': 4789,
    'chair': 4791,
    'melochevka': 4835,
}


class Query:
    def __init__(self, raw_query: dict, schema: dict):
        self.schema = schema
        self.id = raw_query['id']
        self.entity_type_id = raw_query['entityTypeId']
        self._query = apply_mapping(raw_query, schema)

    def __getitem__(self, field_alias):
        return self._query[field_alias]

    # def update_field(self, schema):
    #     for field_key, field_data in schema.items():
    #         self._query[field_key]['title'] = field_data['title']

    def get_data(self):
        return self._query


class QueryRegistry:
    current_dir = Path(__file__).resolve().parent.parent
    schema = load_schema(current_dir / 'schemas/query.schema.json')

    def __init__(self, raw_queries: list[dict]):
        self._queries = [Query(raw_query, self.schema) for raw_query in raw_queries]

    # def get(self, fot_id: int):
    #     for fot in self._queries:
    #         if fot.id == fot_id:
    #             return fot

    def get_by_type_product(self, product_type: str):
        type_product = PRODUCT_TYPE_FOR_QUERY[product_type]
        return [query for query in self._queries if query['type_product'] == type_product]

    def get_all(self) -> List[Query]:
        return self._queries
