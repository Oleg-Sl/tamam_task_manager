import math
from typing import List, Dict, Union
from pydantic import BaseModel

from ...models.fot_coefficient import FotCoefficient
from ...models.fot import Fot
from ...config.constants import ID_FOT


class ValueField(BaseModel):
    value: Union[float, int, str, None]
    field: Union[str, None]


class FotData(BaseModel):
    fot_name: str
    title: str
    basic_salary: float
    checksum: float
    estimate: ValueField
    coefficient: ValueField
    total: ValueField
    allocated_hours: ValueField
    comment: ValueField


class CalculationFotBase:
    def __init__(self, fot_coef: FotCoefficient, fot: Union[Fot, None]):
        self.fot_coef = fot_coef
        self.fot = fot

        self.id = fot.id if fot else None
        self.fot_type_id = ID_FOT

        self.fot_items: Union[List[FotData], None] = None
        self.summary_cost = self.fot.summary_cost if self.fot else 0

    def initialize(self):
        if self.fot is None:
            print(f'Fot not found')
            return

        self.fot_items = []
        for fot_name in self.fot:
            fot_data = self.fot[fot_name]
            fot_field = self.fot.get_field(fot_name)
            self.fot_items.append(FotData(
                fot_name=fot_name,
                title=fot_data.get('title', ''),
                basic_salary=self.fot_coef.get_base_salary_rate(fot_name),
                checksum=0,
                estimate=ValueField(
                    value=fot_data.get('estimated_amount', 0),
                    field=fot_field['estimated_amount']
                ),
                allocated_hours=ValueField(
                    value=fot_data.get('allocated_hours', 0),
                    field=fot_field['allocated_hours']
                ),
                coefficient=ValueField(
                    value=fot_data.get('growth_coefficient', 0),
                    field=fot_field['growth_coefficient']
                ),
                total=ValueField(
                    value=fot_data.get('final_amount', 0),
                    field=fot_field['final_amount']
                ),
                comment=ValueField(
                    value=fot_data.get('comment', 0),
                    field=fot_field['comment']
                )
            ))

    def get_field(self, field_alias: str) -> str:
        return self.fot.get_field(field_alias)

    def get_fots(self) -> List[FotData]:
        return self.fot_items

    def get_update_fields(self) -> Dict[str, Union[str, float, str, None]]:
        data = {
            self.fot.get_field('summary_cost'): self.summary_cost
        }
        for fot in self.fot_items:
            data[fot.estimate.field] = fot.estimate.value
            data[fot.allocated_hours.field] = fot.allocated_hours.value
            data[fot.coefficient.field] = fot.coefficient.value
            data[fot.total.field] = fot.total.value
            data[fot.comment.field] = fot.comment.value

        return data

    def recalculate(self, cost_of_service_packed: float, cost_of_management: float, cost_of_rent: float):
        for fot in self.fot_items:
            cost_per_hour = self.fot_coef.get_cost_per_hour(fot.fot_name)
            fot.estimate.value = math.ceil(fot.allocated_hours.value * cost_per_hour / 100) * 100
            fot.total.value = math.ceil(fot.estimate.value + fot.coefficient.value * cost_per_hour)

        self.summary_cost = self.calc_summary_cost(cost_of_service_packed, cost_of_management, cost_of_rent)

    def calc_summary_cost(self, cost_of_service_packed: float, cost_of_management: float, cost_of_rent: float):
        summary_cost = sum(fot.total.value for fot in self.fot_items) if self.fot_items else 0
        summary_cost += cost_of_service_packed or 0
        summary_cost += cost_of_management or 0
        summary_cost += cost_of_rent or 0
        return math.ceil(summary_cost)

    def get_summary_cost(self):
        return self.summary_cost

