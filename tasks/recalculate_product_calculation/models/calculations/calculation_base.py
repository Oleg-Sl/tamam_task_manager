import math
from pydantic import BaseModel
from typing import Any, Dict, List, Callable, Union
from datetime import datetime

from ...core.utils import apply_mapping
from ...data_context import DataContext
from ...models.calculations.calculation_fot_base import CalculationFotBase
from ...models.fabrics import Fabric


class ValueField(BaseModel):
    value: Union[float, int, str, None]
    field: Union[str, None]


class MaterialData(BaseModel):
    alias: str
    title: str
    type_material: Union[str, None]
    num_fabric: Union[int, None]
    has_price: bool
    coefficient: float
    price: ValueField
    value: ValueField
    amount: ValueField
    comment: ValueField


class CalculationBase:
    def __init__(
            self,
            product_type: str,
            product_type_id: int,
            calculation_type_id: int,
            data: dict,
            schema: dict,
            context: DataContext
    ):
        self.product_type = product_type
        self.product_type_id = product_type_id

        self.calculation_type_id = calculation_type_id
        self.calculation_id: int = data['id']

        self.raw_data = data
        self.data = apply_mapping(data, schema)
        self.schema = schema
        self.context = context

        self.data_callback: Union[Callable[[], Dict], None] = None

        self.fot_coefficient = self.context.fot_coef_registry.get_coefficients(self.product_type_id)
        self.fot_data = self.context.fot_registry.filter({f'parentId{self.calculation_type_id}': self.calculation_id})
        self.calculation_fot = CalculationFotBase(self.fot_coefficient, self.fot_data)

        self.materials: List[MaterialData] = []
        self.summary_materials = self.data.get('total_materials')
        self.cost_price = self.data.get('cost_price')
        self.cost_price_total = self.data.get('cost_price_total')
        self.date_of_calculation = self.data.get('date_of_calculation')

    def __getitem__(self, field: str) -> Any:
        return self.data.get(field, self.raw_data.get(field))

    def __contains__(self, field: str) -> bool:
        return field in self.data or field in self.raw_data

    def initialize(self):
        self.init_materials()
        self.init_queries()
        self.init_fot()

    def init_materials(self):
        print('init_materials')
        self.materials = []
        fabric = self.product_data['fabrics']
        for field_alias, field_data in self.schema.items():
            if isinstance(field_data, dict) and field_data.get('type') in ['material', 'fabric', 'others', 'package']:
                material = MaterialData(
                    alias=field_alias,
                    title='',
                    type_material=field_data.get('type'),
                    num_fabric=field_data.get('number'),
                    has_price='price' in field_data,
                    coefficient=self.context.material_coef_registry.get_coefficient(field_alias),
                    price=ValueField(
                        value=float(self._get_material_price(field_alias, field_data, fabric) or 0),
                        field=field_data.get('price')
                    ),
                    value=ValueField(
                        value=float(self.data[field_alias]['value'] or 0),
                        field=field_data.get('value')
                    ),
                    amount=ValueField(
                        value=float(self.data[field_alias]['amount'] or 0),
                        field=field_data.get('amount')
                    ),
                    comment=ValueField(
                        value=self.data[field_alias]['comments'],
                        field=field_data.get('comments')
                    )
                )
                self.materials.append(material)

    def init_queries(self):
        print('init_queries')
        queries = self.context.query_registry.get_by_type_product(self.product_type)

    def init_fot(self):
        print('init_fot')
        self.calculation_fot.initialize()

    def register_data_callback(self, data_callback: Callable[[], Dict]):
        self.data_callback = data_callback

    def get_product_data(self) -> Dict:
        if self.data_callback is not None:
            return self.data_callback()
        return {}

    @property
    def product_data(self) -> Dict:
        return self.get_product_data()

    def get_field(self, field_alias: str) -> str:
        return self.schema[field_alias]

    def get_materials_summary_cost(self):
        return self.summary_materials

    def get_cost_price(self):
        return self.cost_price

    def get_cost_price_total(self):
        return self.cost_price_total

    def get_calculation_update_fields(self) -> Dict[str, Union[str, float, str, None]]:
        data = {
            self.get_field('date_of_calculation'): datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z'),
            self.get_field('total_materials'): self.summary_materials,
            self.get_field('cost_price'): self.cost_price,
            self.get_field('cost_price_total'): self.cost_price_total,
        }

        for material in self.materials:
            data[material.value.field] = material.value.value
            data[material.amount.field] = material.amount.value
            data[material.comment.field] = material.comment.value
            if material.has_price:
                data[material.price.field] = material.price.value

        return data

    def get_fot_update_fields(self) -> Dict[str, Union[str, float, str, None]]:
        return self.calculation_fot.get_update_fields()

    def recalculate(self):
        self.recalculate_materials()
        self.calculation_fot.recalculate(
            self.calc_service_packed_amount(),
            self.calc_management_amount(),
            self.calc_rent_amount()
        )
        self.cost_price = self.calc_cost_price()
        self.cost_price_total = self.calc_cost_price_total()

    def recalculate_materials(self):
        fabrics = self.product_data['fabrics']
        material_prices = self.context.material_price_registry.get_last()
        for material in self.materials:
            # print('material = ', material)
            if material.type_material == 'fabric':
                fabric = fabrics.get(material.num_fabric)
                material.price.value = fabric['price'] or 0 if fabric else 0
                material.amount.value = material.price.value * material.value.value * material.coefficient
                material.comment.value = f'{fabric["name"]} ({fabric["collection"]} - {fabric["price"]})' if fabric else ''
            elif material.type_material in ['material', 'others', 'package']:
                material.price.value = self.data[material.alias]['price'] if material.has_price else material_prices[material.alias]
                material.price.value = float(material.price.value or 0)
                material.amount.value = material.price.value * material.value.value * material.coefficient
            # print('material.amount.value = ', material.amount.value)

        print('='*88)
        self.summary_materials = self.calc_summary_cost()

    def calc_summary_cost(self):
        packaging_price = self.fot_coefficient.get_cost_per_unit('packaging')
        base_value = self.product_data['base_value']
        total = sum(m.amount.value or 0 for m in self.materials)
        print('base_value = ', base_value)
        print('packaging_price = ', packaging_price)
        try:
            packaging_cost = base_value * packaging_price
            total += packaging_cost
        except (ValueError, TypeError):
            pass
        return math.ceil(total)

    def calc_cost_price(self):
        material_summary_cost_new = self.calc_summary_cost()
        fot_summary_cost_new = self.calculation_fot.calc_summary_cost(
            self.calc_service_packed_amount(),
            self.calc_management_amount(),
            self.calc_rent_amount()
        )
        return math.ceil((material_summary_cost_new + fot_summary_cost_new) / 100) * 100

    def calc_cost_price_total(self):
        markup_workshop = self.context.material_coef_registry.get_coefficient('markup_workshop')
        cost_price = self.calc_cost_price()
        return math.ceil(cost_price * markup_workshop / 100) * 100

    def calc_fot_summary_cost(self):
        return self.calculation_fot.calc_summary_cost(
            self.calc_service_packed_amount(),
            self.calc_management_amount(),
            self.calc_rent_amount()
        )

    def calc_service_packed_amount(self) -> int:
        raise NotImplementedError

    def calc_management_amount(self) -> int:
        raise NotImplementedError

    def calc_rent_amount(self) -> int:
        raise NotImplementedError

    def _get_material_price(self, alias: str, field_data: Dict[str, Any], fabrics: Dict[int, Fabric]):
        if 'price' in field_data:
            price = self.data[alias]['price']
        elif field_data.get('type') == 'fabric':
            num_fabric = field_data.get('number')
            fabric = fabrics.get(num_fabric, {})
            price = 0
            if fabric:
                price = fabric['price']
        else:
            date_of_calculation_str = self.data['date_of_calculation']
            date_of_calculation = datetime.strptime(date_of_calculation_str, '%Y-%m-%dT%H:%M:%S%z')
            material = self.context.material_price_registry.get_closest_before(date_of_calculation)
            price = material[alias]

        return float(price) if isinstance(price, str) \
            else price if isinstance(price, int) or isinstance(price, float) else 0
