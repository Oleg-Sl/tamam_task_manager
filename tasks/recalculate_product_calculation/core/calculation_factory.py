import pathlib
from typing import Type, Dict, List
from pydantic import BaseModel

from ..models.products.product_base import ProductBase
from ..models.calculations.calculation_base import CalculationBase
from ..data_context import DataContext
from ..core.utils import load_schema


class ProductInfo(BaseModel):
    product_type_id: int
    calculation_type_id: int
    product: Type[ProductBase]
    calculation: Type[CalculationBase]
    product_schema: dict
    calculation_schema: dict


class CalculationFactory:
    _registry: Dict[str, ProductInfo] = {}
    _registry_product_names: Dict[int, str] = {}
    _registry_calculation_names: Dict[int, str] = {}

    @classmethod
    def register(cls,
                 name: str,
                 product_type_id: int,
                 calculation_type_id: int,
                 product: Type[ProductBase],
                 calculation: Type[CalculationBase],
                 product_schema: pathlib.Path,
                 calculation_schema: pathlib.Path
                 ):
        cls._registry[name] = ProductInfo(
            product_type_id=product_type_id,
            calculation_type_id=calculation_type_id,
            product=product,
            calculation=calculation,
            product_schema=load_schema(product_schema),
            calculation_schema=load_schema(calculation_schema)
        )
        cls._registry_product_names[product_type_id] = name
        cls._registry_calculation_names[calculation_type_id] = name

    @classmethod
    def create_calculation(cls, product_name: str, calculation_data: dict, context: DataContext) -> CalculationBase:
        cls_data: ProductInfo = cls._registry[product_name]
        return cls_data.calculation(
            product_name,
            cls_data.product_type_id,
            cls_data.calculation_type_id,
            calculation_data,
            cls_data.calculation_schema,
            context
        )

    @classmethod
    def create_product(cls,
                       product_name: str,
                       product_data: dict,
                       context: DataContext
                       ) -> ProductBase:
        cls_data: ProductInfo = cls._registry[product_name]
        return cls_data.product(
            cls_data.product_type_id,
            product_data,
            cls_data.product_schema,
            context
        )

    @classmethod
    def get_product_type_id(cls, product_name: str) -> int:
        cls_data: ProductInfo = cls._registry[product_name]
        return cls_data.product_type_id

    @classmethod
    def get_calculation_type_id(cls, product_name: str) -> int:
        cls_data: ProductInfo = cls._registry[product_name]
        return cls_data.calculation_type_id

    @classmethod
    def get_product_name_by_type_id(cls, type_id: int) -> str:
        product_name = cls._registry_product_names[type_id]
        if not product_name:
            product_name = cls._registry_calculation_names[type_id]

        return product_name

