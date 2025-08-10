import time
from ..core.interfaces import IEntityFetcher
from ..core.bitrix_client import BitrixClient


class EntityFetcher(IEntityFetcher):
    def __init__(self, client: BitrixClient):
        self.client = client

    def fetch(self, **kwargs) -> list[dict]:
        entity_type_id = kwargs.get('entity_type_id')
        data = kwargs.get('filter_data', {})
        if not entity_type_id:
            raise ValueError('product_type_id is required')

        entities = []
        entity_id = 0

        while True:
            data[">id"] = entity_id
            response = self.client.call('crm.item.list', {
                'entityTypeId': entity_type_id,
                'order': {'id': 'ASC'},
                "filter": data,
                # "filter": {">id": entity_id},
                'start': -1
            })

            result = response.get('result', {}).get('items')
            if not result:
                break

            entities.extend(result)
            entity_id = result[-1]['id']
            time.sleep(0.5)

        return entities

    def update(self, **kwargs) -> dict:
        entity_type_id = kwargs.get('entity_type_id')
        entity_id = kwargs.get('entity_id')
        data = kwargs.get('data')
        if not entity_type_id or not entity_id or not data:
            print(entity_type_id, entity_id, data)
            raise ValueError('Cannot update entity')

        response = self.client.call('crm.item.update', {
            'entityTypeId': entity_type_id,
            'id': entity_id,
            'fields': data
        })

        result = response.get('result', {})
        return result
