import pathlib
from pathlib import Path

from ..models.products.armchair import Armchair
from ..models.products.bed import Bed
from ..models.products.chair import Chair
from ..models.products.melochevka import Melochevka
from ..models.products.msp import Msp
from ..models.products.nightstand import Nightstand
from ..models.products.pouf import Pouf
from ..models.products.sofa import Sofa
from ..models.products.table import Table

from ..models.calculations.armchair import ArmchairCalculation
from ..models.calculations.bed import BedCalculation
from ..models.calculations.chair import ChairCalculation
from ..models.calculations.melochevka import MelochevkaCalculation
from ..models.calculations.msp import MspCalculation
from ..models.calculations.nightstand import NightstandCalculation
from ..models.calculations.pouf import PoufCalculation
from ..models.calculations.sofa import SofaCalculation
from ..models.calculations.table import TableCalculation

from ..config.constants import SPCalculationID, SPProductID


current_dir = Path(__file__).resolve().parent.parent

PRODUCT_CALCULATIONS = {
    'armchair': {
        'name': 'armchair',
        'product_schema': pathlib.Path(current_dir / 'schemas/products/armchair.schema.json'),
        'calculation_schema': pathlib.Path(current_dir / 'schemas/calculations/armchair.schema.json'),
        'product_type_id': SPProductID.armchair,
        'calculation_type_id': SPCalculationID.armchair,
        'product': Armchair,
        'calculation': ArmchairCalculation,
    },
    'bed': {
        'name': 'bed',
        'product_schema': pathlib.Path(current_dir / 'schemas/products/bed.schema.json'),
        'calculation_schema': pathlib.Path(current_dir / 'schemas/calculations/bed.schema.json'),
        'product_type_id': SPProductID.bed,
        'calculation_type_id': SPCalculationID.bed,
        'product': Bed,
        'calculation': BedCalculation,
    },
    'chair': {
        'name': 'chair',
        'product_schema': pathlib.Path(current_dir / 'schemas/products/chair.schema.json'),
        'calculation_schema': pathlib.Path(current_dir / 'schemas/calculations/chair.schema.json'),
        'product_type_id': SPProductID.chair,
        'calculation_type_id': SPCalculationID.chair,
        'product': Chair,
        'calculation': ChairCalculation,
    },
    'melochevka': {
        'name': 'melochevka',
        'product_schema': pathlib.Path(current_dir / 'schemas/products/melochevka.schema.json'),
        'calculation_schema': pathlib.Path(current_dir / 'schemas/calculations/melochevka.schema.json'),
        'product_type_id': SPProductID.melochevka,
        'calculation_type_id': SPCalculationID.melochevka,
        'product': Melochevka,
        'calculation': MelochevkaCalculation,
    },
    'msp': {
        'name': 'msp',
        'product_schema': pathlib.Path(current_dir / 'schemas/products/msp.schema.json'),
        'calculation_schema': pathlib.Path(current_dir / 'schemas/calculations/msp.schema.json'),
        'product_type_id': SPProductID.msp,
        'calculation_type_id': SPCalculationID.msp,
        'product': Msp,
        'calculation': MspCalculation,
    },
    'nightstand': {
        'name': 'nightstand',
        'product_schema': pathlib.Path(current_dir / 'schemas/products/nightstand.schema.json'),
        'calculation_schema': pathlib.Path(current_dir / 'schemas/calculations/nightstand.schema.json'),
        'product_type_id': SPProductID.nightstand,
        'calculation_type_id': SPCalculationID.nightstand,
        'product': Nightstand,
        'calculation': NightstandCalculation,
    },
    'pouf': {
        'name': 'pouf',
        'product_schema': pathlib.Path(current_dir / 'schemas/products/pouf.schema.json'),
        'calculation_schema': pathlib.Path(current_dir / 'schemas/calculations/pouf.schema.json'),
        'product_type_id': SPProductID.pouf,
        'calculation_type_id': SPCalculationID.pouf,
        'product': Pouf,
        'calculation': PoufCalculation,
    },
    'sofa': {
        'name': 'sofa',
        'product_schema': pathlib.Path(current_dir / 'schemas/products/sofa.schema.json'),
        'calculation_schema': pathlib.Path(current_dir / 'schemas/calculations/sofa.schema.json'),
        'product_type_id': SPProductID.sofa,
        'calculation_type_id': SPCalculationID.sofa,
        'product': Sofa,
        'calculation': SofaCalculation,
    },
    'table': {
        'name': 'table',
        'product_schema': pathlib.Path(current_dir / 'schemas/products/table.schema.json'),
        'calculation_schema': pathlib.Path(current_dir / 'schemas/calculations/table.schema.json'),
        'product_type_id': SPProductID.table,
        'calculation_type_id': SPCalculationID.table,
        'product': Table,
        'calculation': TableCalculation,
    },
}
