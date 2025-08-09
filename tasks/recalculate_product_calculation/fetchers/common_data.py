import time
from typing import List, Dict

from ..core.interfaces import IEntityFetcher


class CommonDataFetcher(IEntityFetcher):
    def __init__(self, client):
        self.client = client

    def fetch(self, **kwargs) -> dict:
        cmd = {
            'material_prices': 'crm.item.list?entityTypeId=152',
            'material_coefficients': 'crm.item.list?entityTypeId=139',
            'queries': 'crm.item.list?entityTypeId=1052',
            'fot_coefficients': 'crm.item.list?entityTypeId=1044',
        }

        response = self.client.call('batch', {
            'halt': 0,
            'cmd': cmd
        })

        result = response.get('result', {}).get('result', {})

        return {
            'material_prices': result.get('material_prices', {}).get('items', []),
            'material_coefficients': result.get('material_coefficients', {}).get('items', []),
            'queries': result.get('queries', {}).get('items', []),
            'fot_coefficients': result.get('fot_coefficients', {}).get('items', [])
        }

    def fetch_all(self, method: str, params: Dict[str, str] = {}, select: List[str] = None) -> List[Dict]:
        body = {
            **params,
            'filter': {},
            'order': {'id': 'ASC'},
            'start': -1
        }
        if select:
            body['select'] = select

        data = []
        i = 0
        while True:
            body['filter']['>id'] = i
            response = self.client.call(method, body)
            items = response.get('result', {}).get('items')
            if not items:
                break
            data.extend(items)
            i = items[-1]['id']
            time.sleep(0.5)
            # break
        return data
