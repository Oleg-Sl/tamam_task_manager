import pathlib
import math
from typing import Any, Dict, Union

from ..core.utils import apply_mapping
from ..data_context import DataContext
from ..config.product_map import economy_schema
from ..core.utils import load_schema


class Economy:
    def __init__(self, raw_data: dict, context: DataContext):
        self.economy_id = raw_data['id']
        self.economy_type_id = raw_data['entityTypeId']
        self._raw_data = raw_data
        self.schema = load_schema(economy_schema)
        self._data = apply_mapping(raw_data, self.schema)
        self.context = context
        self.update_field(self.schema)
        # print('Economy = ', self._data)

    def __getitem__(self, field: str) -> Any:
        return self._data.get(field, self._raw_data.get(field))

    def __contains__(self, field: str) -> bool:
        return field in self._data or field in self._raw_data

    def update_field(self, schema):
        for field_key, field_data in schema.items():
            if isinstance(field_data, dict):
                self._data[field_key]['category_id'] = field_data['category_id']
                self._data[field_key]['smart_id'] = field_data['smart_id']
                self._data[field_key]['title'] = field_data['title']

    def get_update_fields(self):
        data = {}
        for fabric_type, economy_data in self.schema.items():
            margin_field = economy_data['margin']
            data[margin_field] = self._data[fabric_type]['margin']
        return data

    def recalculate(self, fabric_running_meters, cost_price_total):
        for fabric_type, fabric_data in self._data.items():
            fabric_id = fabric_data['smart_id']
            # print('fabric_id', fabric_id)
            # print('fabric = ', self._data[fabric_type])
            # print('fabric_running_meters', fabric_running_meters)
            fabric = self.context.fabric_registry.get(fabric_id)
            # print('fabric', fabric)
            fabric_price = fabric['price']
            # print('fabric_price', fabric_price)
            fabric_summary = fabric_price * fabric_running_meters
            # print('fabric_summary', fabric_summary)
            total_cost = cost_price_total + fabric_summary
            # print('total_cost', total_cost)
            # margin = math.ceil(1000 * self._data[fabric_type]['price'] / total_cost) / 1000
            margin = math.ceil(1000 * self._data[fabric_type]['price'] / total_cost) / 1000
            margin2 = self._data[fabric_type]['price']

            print('margin', margin)
            self._data[fabric_type]['margin'] = margin
            # self._data[fabric_type]['total_cost'] = total_cost



            # print('fabric_type = ', fabric_type)
            # print('fabric_data = ', fabric_data)
            # fabric_summary = this.economyService.getFabricPrice(economy.code) * fabricRunningMeters;
            # self._data[fabric_type]['margin'] = math.ceil(1000 * self._data[fabric_type]['margin'] / total_cost) / 1000
            # print('fabric_type = ', fabric_type, fabric_data)
            # for category_id, category_data in fabric_data.items():
            #     print(category_id, category_data)
        # this.economies.map((economy) => {
        #     economy.fabricSummary = this.economyService.getFabricPrice(economy.code) * fabricRunningMeters;
        #     economy.totalCost = this.totalPrice + economy.fabricSummary;
        #     // economy.price = Math.ceil((economy.totalCost * economy.margin) / 1000) * 1000;
        #     economy.margin = Math.ceil(1000 * economy.price / economy.totalCost) / 1000;
        # });