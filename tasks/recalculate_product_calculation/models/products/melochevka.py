from typing import Dict, Union

from ...models.products.product_base import ProductBase
from ...models.fabrics import Fabric


class Melochevka(ProductBase):
    def get_fabric(self) -> Dict[int, Fabric]:
        return {}

    def get_fabric_id(self, num: int) -> Union[int, None]:
        pass

    def calc_base_value(self) -> Union[float, None]:
        return 1

    def calc_square_meters(self) -> Union[float, None]:
        return 0

    def calc_linear_meters(self) -> Union[float, None]:
        return 0
