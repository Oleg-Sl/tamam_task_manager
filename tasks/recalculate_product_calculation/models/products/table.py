from typing import Dict

from ...models.products.product_base import ProductBase
from ...models.fabrics import Fabric


class Table(ProductBase):
    def get_fabric(self) -> Dict[int, Fabric]:
        fabric_id_1 = self._data['upholstery_fabric_collection_3']
        return {
            1: self.context.fabric_registry.get(fabric_id_1),
        }

    def get_fabric_id(self, num: int) -> int | None:
        if num == 1:
            return self._data['upholstery_fabric_collection_3']

    def calc_base_value(self) -> float | None:
        return 1

    def calc_square_meters(self) -> float | None:
        w = self['common_dimensions_width']
        d = self['common_dimensions_depth']
        w2 = self['common_dimensions_width_2']
        d2 = self['common_dimensions_depth_2']
        if w and d and w2 and d2:
            return w * 0.001 * d * 0.001 + w2 * 0.001 * d2 * 0.001
        return None

    def calc_linear_meters(self) -> float | None:
        w = self['common_dimensions_width']
        return w
