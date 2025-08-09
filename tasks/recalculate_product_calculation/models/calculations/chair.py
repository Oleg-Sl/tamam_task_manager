import math
from ...models.calculations.calculation_base import CalculationBase


class ChairCalculation(CalculationBase):
    def calc_service_packed_amount(self) -> int:
        frame_variant = self.product_data['frame_variant']
        print('frame_variant = ', frame_variant)
        if frame_variant == 5459:
            # расчет по Столярка + Столярка (Сборка)
            cost_work_carpentry = self.fot_data['carpentry']['final_amount'] if self.fot_data else 0
            cost_work_carpentry_assembly = self.fot_data['carpentry_assembly']['final_amount'] if self.fot_data else 0
            cost_work = cost_work_carpentry + cost_work_carpentry_assembly
            fot_coef = self.context.fot_coef_registry.get_coefficients(self.product_type_id)
            cost_per_hour_carpentry = fot_coef.get_cost_per_hour('carpentry')
            cost_per_hour_carpentry_assembly = fot_coef.get_cost_per_hour('carpentry_assembly')
            cost_per_hour_working = cost_per_hour_carpentry + cost_per_hour_carpentry_assembly
            cost_per_hour_packaging = fot_coef.get_cost_per_hour('packaging')
            service_packed_amount = cost_work / cost_per_hour_working * cost_per_hour_packaging
        else:
            # расчет по обтяжке
            cost_work_upholstery = self.fot_data['upholstery']['final_amount'] if self.fot_data else 0
            cost_per_hour_upholstery = self.context.fot_coef_registry.get_coefficients(self.product_type_id).get_cost_per_hour('upholstery')
            staff_count_upholstery = self.context.fot_coef_registry.get_coefficients(self.product_type_id).get_staff_count('upholstery')
            fot_coef = self.context.fot_coef_registry.get_coefficients(self.product_type_id)
            cost_per_hour_packaging = fot_coef.get_cost_per_hour('packaging')
            service_packed_amount = cost_work_upholstery / cost_per_hour_upholstery / staff_count_upholstery * cost_per_hour_packaging

        return math.ceil(service_packed_amount)

    def calc_management_amount(self) -> int:
        frame_variant = self.product_data['frame_variant']
        if frame_variant == 5459:
            # расчет по Столярка + Столярка (Сборка)
            cost_work_carpentry = self.fot_data['carpentry']['final_amount'] if self.fot_data else 0
            cost_work_carpentry_assembly = self.fot_data['carpentry_assembly']['final_amount'] if self.fot_data else 0
            cost_work = cost_work_carpentry + cost_work_carpentry_assembly
            fot_coef = self.context.fot_coef_registry.get_coefficients(self.product_type_id)
            cost_per_hour_carpentry = fot_coef.get_cost_per_hour('carpentry')
            cost_per_hour_carpentry_assembly = fot_coef.get_cost_per_hour('carpentry_assembly')
            cost_per_hour_working = cost_per_hour_carpentry + cost_per_hour_carpentry_assembly
            cost_per_hour_management = fot_coef.get_cost_per_hour('management')
            management_amount = cost_work / cost_per_hour_working * cost_per_hour_management
        else:
            # расчет по обтяжке
            cost_work_upholstery = self.fot_data['upholstery']['final_amount'] if self.fot_data else 0
            cost_per_hour_upholstery = self.context.fot_coef_registry.get_coefficients(self.product_type_id).get_cost_per_hour('upholstery')
            staff_count_upholstery = self.context.fot_coef_registry.get_coefficients(self.product_type_id).get_staff_count('upholstery')
            fot_coef = self.context.fot_coef_registry.get_coefficients(self.product_type_id)
            cost_per_hour_management = fot_coef.get_cost_per_hour('management')
            management_amount = cost_work_upholstery / cost_per_hour_upholstery / staff_count_upholstery * cost_per_hour_management

        return math.ceil(management_amount)

    def calc_rent_amount(self) -> int:
        frame_variant = self.product_data['frame_variant']
        if frame_variant == 5459:
            # расчет по Столярка + Столярка (Сборка)
            cost_work_carpentry = self.fot_data['carpentry']['final_amount'] if self.fot_data else 0
            cost_work_carpentry_assembly = self.fot_data['carpentry_assembly']['final_amount'] if self.fot_data else 0
            cost_work = cost_work_carpentry + cost_work_carpentry_assembly
            fot_coef = self.context.fot_coef_registry.get_coefficients(self.product_type_id)
            cost_per_hour_carpentry = fot_coef.get_cost_per_hour('carpentry')
            cost_per_hour_carpentry_assembly = fot_coef.get_cost_per_hour('carpentry_assembly')
            cost_per_hour_working = cost_per_hour_carpentry + cost_per_hour_carpentry_assembly
            cost_per_hour_rent = fot_coef.get_cost_per_hour('rent')
            rent_amount = cost_work / cost_per_hour_working * cost_per_hour_rent
        else:
            # расчет по обтяжке
            cost_work_upholstery = self.fot_data['upholstery']['final_amount'] if self.fot_data else 0
            cost_per_hour_upholstery = self.context.fot_coef_registry.get_coefficients(self.product_type_id).get_cost_per_hour('upholstery')
            staff_count_upholstery = self.context.fot_coef_registry.get_coefficients(self.product_type_id).get_staff_count('upholstery')
            fot_coef = self.context.fot_coef_registry.get_coefficients(self.product_type_id)
            cost_per_hour_rent = fot_coef.get_cost_per_hour('rent')
            rent_amount = cost_work_upholstery / cost_per_hour_upholstery / staff_count_upholstery * cost_per_hour_rent

        return math.ceil(rent_amount)
