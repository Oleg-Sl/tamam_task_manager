from typing import Dict, Union

from ...models.products.product_base import ProductBase
from ...models.fabrics import Fabric


class Nightstand(ProductBase):
    def get_fabric(self) -> Dict[int, Fabric]:
        fabric_id_1 = self._data['upholstery_fabric_collection_2']
        return {
            1: self.context.fabric_registry.get(fabric_id_1),
        }

    def get_fabric_id(self, num: int) -> Union[int, None]:
        if num == 1:
            return self._data['upholstery_fabric_collection_2']

    def calc_base_value(self) -> Union[float, None]:
        return 1

    def calc_square_meters(self) -> Union[float, None]:
        w = self['common_dimensions_width']
        d = self['common_dimensions_depth']
        if w and d:
            return w * 0.001 * d * 0.001
        return None

    def calc_linear_meters(self) -> Union[float, None]:
        return 0
