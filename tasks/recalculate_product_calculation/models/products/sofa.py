from typing import Dict, Union

from ...models.products.product_base import ProductBase
from ...models.fabrics import Fabric


class Sofa(ProductBase):
    def get_fabric(self) -> Dict[int, Fabric]:
        fabric_id_1 = self._data['upholstery_fabric_collection']
        return {
            1: self.context.fabric_registry.get(fabric_id_1),
        }

    def get_fabric_id(self, num: int) -> Union[int, None]:
        if num == 1:
            return self._data['upholstery_fabric_collection_2']

    def calc_base_value(self) -> Union[float, None]:
        return self.calc_linear_meters()

    def calc_square_meters(self) -> Union[float, None]:
        shape = self['shape']
        w = self['common_dimensions_width'] or 0
        d = self['common_dimensions_depth'] or 0
        d1 = self['depth_one'] or 0
        d2 = self['depth_two'] or 0
        d3 = self['depth_three'] or 0
        try:
            if shape == 3703 or shape == '3703':
                return w * 0.001 * d * 0.001
            elif shape == 3705 or shape == '3705':
                return (w * 0.001 + d1 * 0.001 + d3 * 0.001 - d2 * 0.001) * d2 * 0.001
            elif shape == 3707 or shape == '3707':
                return (w * 0.001 + d1 * 0.001 + d3 * 0.001 - d2 * 0.001) * d2 * 0.001
            elif shape == 3709 or shape == '3709':
                return (w * 0.001 + d1 * 0.001 + d3 * 0.001 - 2 * d2 * 0.001) * d2 * 0.001
            elif shape == 3711 or shape == '3711':
                return 1.2 * w * 0.001 * d * 0.001
            elif shape == 3713 or shape == '3713':
                return 0
        except TypeError:
            pass
        return 0

    def calc_linear_meters(self) -> Union[float, None]:
        shape = self['shape']
        w = self['common_dimensions_width'] or 0
        d = self['common_dimensions_depth'] or 0
        d1 = self['depth_one'] or 0
        d2 = self['depth_two'] or 0
        d3 = self['depth_three'] or 0
        try:
            if shape == 3703 or shape == '3703':
                return w * 0.001
            elif shape == 3705 or shape == '3705':
                return w * 0.001 + d1 * 0.001 + d3 * 0.001 - d2 * 0.001
            elif shape == 3707 or shape == '3707':
                return w * 0.001 + d1 * 0.001 + d3 * 0.001 - d2 * 0.001
            elif shape == 3709 or shape == '3709':
                return w * 0.001 + d1 * 0.001 + d3 * 0.001 - 2 * d2 * 0.001
            elif shape == 3711 or shape == '3711':
                return 1.2 * w * 0.001
            elif shape == 3713 or shape == '3713':
                return 0
        except TypeError:
            pass

        return 0
