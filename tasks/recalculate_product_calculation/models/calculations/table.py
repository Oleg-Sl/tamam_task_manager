import math
from ...models.calculations.calculation_base import CalculationBase


class TableCalculation(CalculationBase):
    def calc_service_packed_amount(self) -> float:
        cost_per_hour_packaging = self.context.fot_coef_registry.get_coefficients(self.product_type_id).get_cost_per_hour('packaging')
        cost_work_painting = self.fot_data['painting']['final_amount'] if self.fot_data else 0
        fot_coef = self.context.fot_coef_registry.get_coefficients(self.product_type_id)
        cost_per_hour_painting = fot_coef.get_cost_per_hour('painting')
        cost_of_service = cost_work_painting / cost_per_hour_painting * cost_per_hour_packaging
        return math.ceil(cost_of_service)

    def calc_management_amount(self) -> float:
        cost_per_hour_management = self.context.fot_coef_registry.get_coefficients(self.product_type_id).get_cost_per_hour('management')
        cost_work_painting = self.fot_data['painting']['final_amount'] if self.fot_data else 0
        fot_coef = self.context.fot_coef_registry.get_coefficients(self.product_type_id)
        cost_per_hour_painting = fot_coef.get_cost_per_hour('painting')
        cost_of_service = cost_work_painting / cost_per_hour_painting * cost_per_hour_management
        return math.ceil(cost_of_service)

    def calc_rent_amount(self) -> float:
        cost_per_hour_rent = self.context.fot_coef_registry.get_coefficients(self.product_type_id).get_cost_per_hour('rent')
        cost_work_painting = self.fot_data['painting']['final_amount'] if self.fot_data else 0
        fot_coef = self.context.fot_coef_registry.get_coefficients(self.product_type_id)
        cost_per_hour_painting = fot_coef.get_cost_per_hour('painting')
        cost_of_service = cost_work_painting / cost_per_hour_painting * cost_per_hour_rent
        return math.ceil(cost_of_service)
