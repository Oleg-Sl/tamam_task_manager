import math
from ...models.calculations.calculation_base import CalculationBase


class MelochevkaCalculation(CalculationBase):
    def calc_service_packed_amount(self) -> int:
        fot_coef = self.context.fot_coef_registry.get_coefficients(self.product_type_id)
        cost_per_hour_packaging = fot_coef.get_cost_per_hour('packaging')
        cost_work_upholstery = self.fot_data['upholstery']['final_amount'] if self.fot_data else 0
        cost_per_hour_upholstery = fot_coef.get_cost_per_hour('upholstery')
        staff_count_upholstery = fot_coef.get_staff_count('upholstery')
        cost_of_service = cost_work_upholstery / cost_per_hour_upholstery / staff_count_upholstery * cost_per_hour_packaging
        return math.ceil(cost_of_service) or 0

    def calc_management_amount(self) -> int:
        cost_per_hour_management = self.context.fot_coef_registry.get_coefficients(self.product_type_id).get_cost_per_hour('management')
        cost_work_upholstery = self.fot_data['upholstery']['final_amount'] if self.fot_data else 0
        cost_per_hour_upholstery = self.context.fot_coef_registry.get_coefficients(self.product_type_id).get_cost_per_hour('upholstery')
        staff_count_upholstery = self.context.fot_coef_registry.get_coefficients(self.product_type_id).get_staff_count('upholstery')
        cost_of_management = cost_work_upholstery / cost_per_hour_upholstery / staff_count_upholstery * cost_per_hour_management
        return math.ceil(cost_of_management) or 0

    def calc_rent_amount(self) -> int:
        cost_per_hour_rent = self.context.fot_coef_registry.get_coefficients(self.product_type_id).get_cost_per_hour('rent')
        cost_work_upholstery = self.fot_data['upholstery']['final_amount'] if self.fot_data else 0
        cost_per_hour_upholstery = self.context.fot_coef_registry.get_coefficients(self.product_type_id).get_cost_per_hour('upholstery')
        staff_count_upholstery = self.context.fot_coef_registry.get_coefficients(self.product_type_id).get_staff_count('upholstery')
        cost_of_rent = cost_work_upholstery / cost_per_hour_upholstery / staff_count_upholstery * cost_per_hour_rent
        return math.ceil(cost_of_rent) or 0
