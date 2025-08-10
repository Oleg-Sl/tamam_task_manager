from typing import Any, Dict, Union

from ...core.utils import apply_mapping
from ...data_context import DataContext
from ...models.calculations.calculation_base import CalculationBase
from ...models.fabrics import Fabric


class ProductBase:
    def __init__(self, product_type_id: int, data: dict, schema: dict, context: DataContext):
        self.product_type_id = product_type_id
        self.product_id = data['id']
        self._raw_data = data
        self._data = apply_mapping(data, schema)
        self.schema = schema
        self.context = context
        self.calculation: Union[CalculationBase, None] = None

    def __getitem__(self, field: str) -> Any:
        return self._data.get(field, self._raw_data.get(field))

    def __contains__(self, field: str) -> bool:
        return field in self._data or field in self._raw_data

    def get_data_for_calculation(self) -> Dict:
        return {
            'product_id': self.product_id,
            'base_value': self.calc_base_value(),
            'square_meters': self.calc_square_meters(),
            'linear_meters': self.calc_linear_meters(),
            'fabrics': self.get_fabric(),
            'frame_variant': self._data.get('frame_variant'),
            'is_template_potochka': self._data.get('is_template_potochka') == 'Y',
            'field_template_potochka': self.schema['is_template_potochka']

        }

    def is_template_of_potochka(self) -> bool:
        return self._data.get('is_template_potochka') == 'Y'

    def get_fabric(self) -> Dict[int, Fabric]:
        raise NotImplementedError

    def get_fabric_id(self, num: int) -> Union[int, None]:
        raise NotImplementedError

    def calc_base_value(self) -> Union[float, None]:
        raise NotImplementedError

    def calc_square_meters(self) -> Union[float, None]:
        raise NotImplementedError

    def calc_linear_meters(self) -> Union[float, None]:
        raise NotImplementedError
