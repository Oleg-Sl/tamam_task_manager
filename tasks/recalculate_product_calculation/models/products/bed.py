from typing import Dict, Union

from ...models.products.product_base import ProductBase
from ...data_context import DataContext
from ...models.fabrics import Fabric


class Bed(ProductBase):
    def get_fabric(self) -> Dict[int, Fabric]:
        fabric_id_1 = self._data['upholstery_fabric_collection_2']
        fabric_id_2 = self._data['upholstery_fabric_collection_3']
        return {
            1: self.context.fabric_registry.get(fabric_id_1),
            2: self.context.fabric_registry.get(fabric_id_2),
        }

    def get_fabric_id(self, num: int) -> Union[int, None]:
        if num == 1:
            return self._data['upholstery_fabric_collection_2']
        if num == 2:
            return self._data['upholstery_fabric_collection_3']

    def calc_base_value(self) -> Union[float, None]:
        return 1

    def calc_square_meters(self) -> Union[float, None]:
        w = self['common_dimensions_width']
        d = self['common_dimensions_depth']
        w2 = self['common_dimensions_width_2']
        h2 = self['common_dimensions_height_2']
        h3 = self['common_dimensions_height_3']
        if w and d and w2 and h2 and h3:
            return w2 * 0.001 * h2 * 0.001 + (h3 * 0.001 * d * 0.001) * 2 + h3 * 0.001 * w * 0.001
        return None

    def calc_linear_meters(self) -> Union[float, None]:
        return 0
