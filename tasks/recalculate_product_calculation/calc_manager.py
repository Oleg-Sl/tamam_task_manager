import time
from typing import List, Callable, Dict

from .core.calculation_factory import CalculationFactory
from .core.interfaces import IEntityFetcher
from .data_context import DataContext
from .models.products.product_base import ProductBase
from .models.calculations.calculation_base import CalculationBase


REQUEST_TIMEOUT = 1


class CalculationManager:
    request_timeout = REQUEST_TIMEOUT

    def __init__(self, entity_fetcher: IEntityFetcher, data_context: DataContext):
        self.entity_fetcher = entity_fetcher
        self.data_context = data_context

    def update_calculation_summary_cost(self, calc_type: str):
        calculations = self._get_calculations(calc_type)
        products = self._get_products(calc_type)
        self._register_calculation_to_product(products, calculations)
        product_calculations = [calculation for calculation in calculations if calculation.data_callback]

        for calculation in product_calculations:
            calculation.initialize()

            materials_summary_cost_current = calculation.get_materials_summary_cost()
            materials_summary_cost_new = calculation.calc_summary_cost()
            cost_price_current = calculation.get_cost_price()
            cost_price_new = calculation.calc_cost_price()
            cost_price_total_current = calculation.get_cost_price_total()
            cost_price_total_new = calculation.calc_cost_price_total()

            fot_summary_cost_current = calculation.calculation_fot.get_summary_cost()
            fot_summary_cost_new = calculation.calc_fot_summary_cost()

            print('Calculation id = ', calculation.calculation_id, ' fot_id = ', calculation.calculation_fot.id)
            print('materials_summary_cost = ', materials_summary_cost_current, materials_summary_cost_new)
            print('cost_price = ', cost_price_current, cost_price_new)
            print('cost_price_total = ', cost_price_total_current, cost_price_total_new)
            print('fot_summary_cost = ', fot_summary_cost_current, fot_summary_cost_new)

            # time.sleep(self.request_timeout)
            # result_calculation_updated = self._update_entity(
            #     calculation.calculation_type_id,
            #     calculation.calculation_id,
            #     {
            #         calculation.get_field('total_materials'): calculation.calc_summary_cost(),
            #         calculation.get_field('cost_price'): calculation.calc_cost_price(),
            #         calculation.get_field('cost_price_total'): cost_price_total_new
            #     }
            # )

            # time.sleep(self.request_timeout)
            # result_fot_updated = self._update_entity(
            #     calculation.calculation_fot.fot_type_id,
            #     calculation.calculation_fot.id,
            #     {
            #         calculation.calculation_fot.get_field('summary_cost'): calculation.calculation_fot.calc_summary_cost()
            #     }
            # )

    def recalculate(self, calc_type: str):
        calculations = self._get_calculations(calc_type)
        products = self._get_products(calc_type)
        self._register_calculation_to_product(products, calculations)

        template_calculations = [
            calculation for calculation in calculations if calculation.product_data.get('is_template_potochka')
        ]
        print(calc_type, ' - ', len(template_calculations))

        for calculation in template_calculations:
            calculation.initialize()
            print('*'*88)
            print('product_id = ', calculation.product_data['product_id'])
            print('calculation_id = ', calculation.calculation_id)
            print('fot_id = ', calculation.calculation_fot.id)
            calculation.recalculate()

            print(calculation.get_calculation_update_fields())
            print(calculation.get_fot_update_fields())

            result_calculation_update = self._update_entity(
                calculation.calculation_type_id,
                calculation.calculation_id,
                calculation.get_calculation_update_fields()
            )
            time.sleep(self.request_timeout)
            print('result_calculation_update = ', result_calculation_update)
            result_fot_update = self._update_entity(
                calculation.calculation_fot.fot_type_id,
                calculation.calculation_fot.id,
                calculation.get_fot_update_fields()
            )
            print('result_fot_update = ', result_fot_update)
            time.sleep(self.request_timeout)

        return len(template_calculations)

    def update_field_is_template_potochka(self, calc_type: str):
        calculations = self._get_calculations(calc_type)
        products = self._get_products(calc_type)
        self._register_calculation_to_product(products, calculations)

        template_calculations = [
            calculation for calculation in calculations if calculation.product_data.get('is_template_potochka')
        ]
        print(calc_type, ' - ', len(template_calculations))
        for calculation in template_calculations:
            time.sleep(self.request_timeout)
            result_calculation_updated = self._update_entity(
                calculation.calculation_type_id,
                calculation.calculation_id,
                {
                    calculation.get_field('is_template_potochka'): 'Y'
                }
            )
            print('result_calculation_updated = ', result_calculation_updated)

            time.sleep(self.request_timeout)
            result_fot_updated = self._update_entity(
                calculation.calculation_fot.fot_type_id,
                calculation.calculation_fot.id,
                {
                    calculation.calculation_fot.get_field('is_template_potochka'): 'Y'
                }
            )
            print('result_fot_updated = ', result_fot_updated)

    def _register_calculation_to_product(self, products: List[ProductBase], calculations: List[CalculationBase]):
        product_map = {str(product.product_id): product for product in products}
        for calculation in calculations:
            parent_product_id = calculation['parent_product']
            if parent_product_id and str(parent_product_id) in product_map:
                product = product_map.get(str(parent_product_id))
                product.calculation = calculation
                calculation.register_data_callback(product.get_data_for_calculation)

    def _get_calculations(self, entity_type: str) -> List[CalculationBase]:
        calculation_type_id = CalculationFactory.get_calculation_type_id(entity_type)
        raw_calculations = self.entity_fetcher.fetch(entity_type_id=calculation_type_id)
        return [
            CalculationFactory.create_calculation(entity_type, raw_calculation, self.data_context)
            for raw_calculation in raw_calculations
        ]

    def _get_products(self, entity_type: str) -> List[ProductBase]:
        product_type_id = CalculationFactory.get_product_type_id(entity_type)
        raw_products = self.entity_fetcher.fetch(entity_type_id=product_type_id)
        return [
            CalculationFactory.create_product(entity_type, raw_product, self.data_context)
            for raw_product in raw_products
        ]

    def _update_entity(self, entity_type_id: int, entity_id: int, updated_fields: Dict[str, int | float | str | None]):
        if entity_type_id is None or entity_id is None or not updated_fields:
            return
        response = self.entity_fetcher.update(
            entity_type_id=entity_type_id,
            entity_id=entity_id,
            data=updated_fields
        )
        return response






    # def update_entity_fields(self, entity: dict | None):
    #     if not entity:
    #         return
    #
    #     # print("entity = ", entity.model_dump())
    #     # data = {
    #     #     field.field: field.new_value
    #     #     for field in entity.data
    #     #     if not field.old_value or field.old_value != field.new_value
    #     # }
    #     response = self.entity_fetcher.update(
    #         entity_type_id=entity['entity_type_id'],
    #         entity_id=entity['entity_id'],
    #         data=entity['data']
    #     )

    # def update_entity(self, entity: EntityFieldSchema | None):
    #     if not entity:
    #         return
    #
    #     print("entity = ", entity.model_dump())
    #     data = {
    #         field.field: field.new_value
    #         for field in entity.data
    #         if not field.old_value or field.old_value != field.new_value
    #     }
    #     if not data:
    #         return
    #

    # def process_entity_type(self, entity_type: str):
    #     calculations = self.get_calculations(entity_type)
    #     products = self.get_products(entity_type)
    #
    #     calculation_map: Dict[str, CalculationBase] = {
    #         str(calculation['id']): calculation for calculation in calculations
    #     }
    #
    #     for product in products:
    #         if product['calculation_id'] is not None and product['calculation_id']:
    #             calculation = calculation_map.get(str(product['calculation_id']))
    #             if calculation:
    #                 product.calculation = calculation
    #                 calculation.register_data_callback(product.get_data_for_calculation)
    #                 calculation.execute()
    #                 calculation_summary_cost = calculation.get_calculation_summary_cost()
    #                 fot_summary_cost = calculation.get_fot_summary_cost()
    #                 self.update_entity(calculation_summary_cost)
    #                 self.update_entity(fot_summary_cost)
    #             else:
    #                 print(f'Calculation with id = "{product["calculation_id"]}" not found,'
    #                       f'for product {entity_type} with id = {product["id"]}')


































        # print("data = ", data)
        # response = self.entity_fetcher.update(
        #     entity_type_id=entity.entity_type_id,
        #     entity_id=entity.entity_id,
        #     data=data
        # )
        # print("response = ", response)

        # updated_product_list = []
        # updated_fot_list = []

        # for raw_calculation in raw_calculations:
        #     # print('product_calculation_id = ', raw_calculation['id'])
        #     calculation = CalculationFactory.create_calculation(entity_type, raw_calculation, self.data_context)
        #     # print(calculation.calculation_type_id)
        #     # break
        #
        #     materials_summary_cost = product_calculation.calc_materials_summary_cost()
        #     current_materials_summary_cost = product_calculation.get_field_data('total_materials')
        #
        #     # print(materials_summary_cost, current_materials_summary_cost, current_materials_summary_cost == materials_summary_cost)
        #
        #     rent_cost = math.ceil(product_calculation.calc_rent_cost())
        #     # print('rent_cost = ', rent_cost)
        #
        #     if not current_materials_summary_cost:
        #         # updated_product_list.append({
        #         #
        #         # })
        #         self.calculation_resolver.get_fot()
        #         updated_fot_list.append({
        #
        #         })