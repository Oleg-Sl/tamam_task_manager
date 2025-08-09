import math
from pydantic import BaseModel
from typing import Any, Dict, List, Callable
from datetime import datetime

from ...core.utils import apply_mapping
from ...data_context import DataContext
from ...models.calculations.calculation_fot_base import CalculationFotBase
from ...models.fabrics import Fabric


class ValueField(BaseModel):
    value: float | int | str | None
    field: str | None


class MaterialData(BaseModel):
    alias: str
    title: str
    type_material: str | None
    num_fabric: int | None
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

        self.data_callback: Callable[[], Dict] | None = None

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
        queries = self.context.query_registry.get_by_type_product(self.product_type)

    def init_fot(self):
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

    def get_calculation_update_fields(self) -> Dict[str, str | float | str | None]:
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

    def get_fot_update_fields(self) -> Dict[str, str | float | str | None]:
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
            print('material = ', material)
            if material.type_material == 'fabric':
                fabric = fabrics.get(material.num_fabric)
                material.price.value = fabric['price'] or 0 if fabric else 0
                material.amount.value = material.price.value * material.value.value * material.coefficient
                material.comment.value = f'{fabric["name"]} ({fabric["collection"]} - {fabric["price"]})' if fabric else ''
            elif material.type_material in ['material', 'others', 'package']:
                material.price.value = self.data[material.alias]['price'] if material.has_price else material_prices[material.alias]
                material.price.value = float(material.price.value or 0)
                material.amount.value = material.price.value * material.value.value * material.coefficient
            print('material.amount.value = ', material.amount.value)

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





    # def execute(self):
    #     print(f'\ncalculation_id={self.calculation_id}********************************')
    #     print(f'product_id={self.product_data["product_id"]}********************************')
    #
    #     fabrics = self.product_data['fabrics']
    #
    #     self.material_calculator.initialize(fabrics)
    #     self.fot_calculator.initialize()
    #
    #     material_summary_cost = self.material_calculator.get_summary_cost()
    #     material_summary_cost_new = self.material_calculator.calc_summary_cost(
    #         self.context.fot_coef_registry.get_coefficients(self.product_type_id).get_cost_per_unit('packaging'),
    #         self.product_data['base_value']
    #     )
    #
    #     fot_summary_cost = self.fot_calculator.get_summary_cost()
    #     fot_summary_cost_new = self.fot_calculator.calc_summary_cost(
    #         self.calc_service_packed_amount(),
    #         self.calc_management_amount(),
    #         self.calc_rent_amount()
    #     )
    #
    #     new_cost_price = self.calc_cost_price()
    #     new_cost_price_total = self.calc_cost_price_total()
    #

    # def get_calculation_summary_cost(self) -> EntityFieldSchema:
    #     material_summary_cost = self.material_calculator.get_summary_cost()
    #     material_summary_cost_new = self.material_calculator.calc_summary_cost(
    #         self.context.fot_coef_registry.get_coefficients(self.product_type_id).get_cost_per_unit('packaging'),
    #         self.product_data['base_value']
    #     )
    #
    #     new_cost_price = self.calc_cost_price()
    #     new_cost_price_total = self.calc_cost_price_total()
    #
    #     return EntityFieldSchema(
    #         entity_type_id=self.calculation_type_id,
    #         entity_id=self.calculation_id,
    #         data=[
    #             FieldSchema(
    #                 field=self.schema['total_materials'],
    #                 new_value=material_summary_cost_new,
    #                 old_value=material_summary_cost
    #             ),
    #             FieldSchema(
    #                 field=self.schema['cost_price'],
    #                 new_value=new_cost_price,
    #                 old_value=self.cost_price
    #             ),
    #             FieldSchema(
    #                 field=self.schema['cost_price_total'],
    #                 new_value=new_cost_price_total,
    #                 old_value=self.cost_price_total
    #             )
    #         ]
    #     )

    # def get_fot_summary_cost(self) -> EntityFieldSchema | None:
    #     fot_summary_cost = self.fot_calculator.get_summary_cost()
    #     fot_summary_cost_new = self.fot_calculator.calc_summary_cost(
    #         self.calc_service_packed_amount(),
    #         self.calc_management_amount(),
    #         self.calc_rent_amount()
    #     )
    #
    #     if not self.fot_data:
    #         return None
    #
    #     return EntityFieldSchema(
    #         entity_type_id=self.fot_data.entity_type_id,
    #         entity_id=self.fot_data.id,
    #         data=[
    #             FieldSchema(
    #                 field=self.fot_data.get_field('summary_cost'),
    #                 new_value=fot_summary_cost_new,
    #                 old_value=fot_summary_cost
    #             )
    #         ]
    #     )












    # def calc_package(self) -> float | None:
    #     price = self.context.fot_coef_registry.get_coefficients(self.product_type_id).get_cost_per_unit('packaging')
    #     base_value = self.product_data['base_value']
    #     amount = None
    #     try:
    #         amount = base_value * price
    #     except ValueError:
    #         pass
    #     return amount

    # def calc_cost_price(self):
    #     markup_workshop = self.context.material_coef_registry.get_coefficient('markup_workshop')
    #     self.cost_price = int(self.summary_materials + self.summary_fots / 100) * 100
    #     self.total_cost_price = int(self.cost_price * markup_workshop / 100) * 100

    # def calc_summary_materials(self) -> float | None:
    #     if self.materials:
    #         amount = sum(material.amount for material in self.materials if material.amount) + self.calc_package()
    #         return amount

    # def calc_summary_fots(self):
    #     summary_fot = sum(fot.total for fot in self.fot_items) if self.fot_items else 0
    #     summary_fot += self.cost_of_service_packed or 0
    #     summary_fot += self.cost_of_management or 0
    #     summary_fot += self.cost_of_rent or 0
    #     return summary_fot



    # def init_materials(self):
    #     self.materials = []
    #     for field_alias, field_data in self.schema.items():
    #         if not isinstance(field_data, dict):
    #             continue
    #
    #         if field_data.get('type') in ['material', 'fabric', 'others', 'package']:
    #             self.materials.append(MaterialData(
    #                 alias=field_alias,
    #                 title='',
    #                 coefficient=self.context.material_coef_registry.get_coefficient(field_alias),
    #                 price=self._get_material_price(field_alias, field_data),
    #                 value=self.data[field_alias]['value'],
    #                 amount=self.data[field_alias]['amount'],
    #                 comment=self.data[field_alias]['comments']
    #             ))
    #
    #     self.summary_cost_of_fot = self.fot.summary_cost

    # def init_fot_items(self):
    #     if self.fot is None:
    #         print(f'Fot for calculation id ={self.data["id"]} not found')
    #         return
    #
    #     # print(f'Fot id = {self.fot.id} for calculation id ={self.data["id"]}')
    #     self.fot_items = []
    #     # for fot_name in self.fot.get_names():
    #     for fot_name in self.fot:
    #         fot_data = self.fot[fot_name]
    #         self.fot_items.append(FotData(
    #             fot_name=fot_name,
    #             title=fot_data.get('title', ''),
    #             estimate=fot_data.get('estimated_amount', 0),
    #             allocated_hours=fot_data.get('allocated_hours', 0),
    #             coefficient=fot_data.get('growth_coefficient', 0),
    #             total=fot_data.get('final_amount', 0),
    #             checksum=0,
    #             basic_salary=self.context.fot_coef_registry.get_coefficients(self.product_type_id).get_base_salary_rate(fot_name),
    #             comment=fot_data.get('comment', '')
    #         ))

    # def _get_material_price(self, field_alias: str, field_data: dict) -> float:
    #     if 'price' in field_data:
    #         price = self.data[field_alias]['price']
    #     elif field_data.get('type') == 'fabric':
    #         price = 0
    #     else:
    #         date_of_calculation_str = self.data['date_of_calculation']
    #         date_of_calculation = datetime.datetime.strptime(date_of_calculation_str, '%Y-%m-%dT%H:%M:%S%z')
    #         material = self.context.material_price_registry.get_closest_before(date_of_calculation)
    #         price = material[field_alias]
    #
    #     return float(price) if isinstance(price, str) else price if isinstance(price, int) or isinstance(price, float) else 0
