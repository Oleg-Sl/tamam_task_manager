from typing import Dict, Union

from ...models.products.product_base import ProductBase
from ...models.fabrics import Fabric


class Msp(ProductBase):
    def get_fabric(self) -> Dict[int, Fabric]:
        fabric_id_1 = self._data['upholstery_fabric_collection']
        fabric_id_2 = self._data['upholstery_fabric_collection_1']
        fabric_id_3 = self._data['upholstery_fabric_collection_2']
        return {
            1: self.context.fabric_registry.get(fabric_id_1),
            2: self.context.fabric_registry.get(fabric_id_2),
            3: self.context.fabric_registry.get(fabric_id_3),
        }

    def get_fabric_id(self, num: int) -> Union[int, None]:
        if num == 1:
            return self._data['upholstery_fabric_collection']
        if num == 2:
            return self._data['upholstery_fabric_collection_1']
        if num == 3:
            return self._data['upholstery_fabric_collection_2']

    def calc_base_value(self) -> Union[float, None]:
        return self.calc_square_meters()

    def calc_square_meters(self) -> Union[float, None]:
        try:
            # print(f"w = ", self['common_dimensions_width'])
            # print(f"d = ", self['common_dimensions_height'])
            w = float(self['common_dimensions_width'])
            d = float(self['common_dimensions_height'])
            return w * 0.001 * d * 0.001
        except (TypeError, ValueError):
            pass

    def calc_linear_meters(self) -> Union[float, None]:
        return 0
