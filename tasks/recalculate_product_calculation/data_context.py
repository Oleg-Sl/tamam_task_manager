# from services.material_price_service import MaterialPriceService
# from services.material_coefficient_service import MaterialCoefficientService
# from services.fot_coefficient_service import FotCoefficientService
# from services.query_service import QueryService
# from services.fot_service import FotService

from .models.material_price import MaterialPriceRegistry
from .models.material_coefficient import MaterialCoefficientRegistry
from .models.fot_coefficient import FotCoefficientRegistry
from .models.fot import FotRegistry
from .models.query import QueryRegistry
from .models.fabrics import FabricRegistry


class DataContext:
    def __init__(
            self,
            material_price_registry: MaterialPriceRegistry,
            material_coef_registry: MaterialCoefficientRegistry,
            fot_coef_registry: FotCoefficientRegistry,
            query_registry: QueryRegistry,
            fot_registry: FotRegistry,
            fabric_registry: FabricRegistry
    ):
        self.material_price_registry = material_price_registry
        self.material_coef_registry = material_coef_registry
        self.fot_coef_registry = fot_coef_registry
        self.query_registry = query_registry
        self.fot_registry = fot_registry
        self.fabric_registry = fabric_registry

    @classmethod
    def from_services(cls, material_prices: list, material_coef: list, fot_coef: list, queries: list, fots: list, fabrics: list):
        return cls(
            material_price_registry=MaterialPriceRegistry(material_prices),
            material_coef_registry=MaterialCoefficientRegistry(material_coef),
            fot_coef_registry=FotCoefficientRegistry(fot_coef),
            query_registry=QueryRegistry(queries),
            fot_registry=FotRegistry(fots),
            fabric_registry=FabricRegistry(fabrics)
        )
