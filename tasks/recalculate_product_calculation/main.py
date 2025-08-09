from typing import Dict

from .core.bitrix_client import BitrixClient
from .core.calculation_factory import CalculationFactory
from .calc_manager import CalculationManager

from .data_context import DataContext
from .fetchers.common_data import CommonDataFetcher
from .fetchers.entities import EntityFetcher
from .config.constants import ID_FOT, ID_FABRIC
from .config.product_map import PRODUCT_CALCULATIONS


def setup():
    for name, meta in PRODUCT_CALCULATIONS.items():
        CalculationFactory.register(
            name=meta['name'],
            product_type_id=meta['product_type_id'],
            calculation_type_id=meta['calculation_type_id'],
            product=meta['product'],
            calculation=meta['calculation'],
            product_schema=meta['product_schema'],
            calculation_schema=meta['calculation_schema'],
        )


def recalculate() -> Dict[str, int]:
    setup()

    bitrix_client = BitrixClient()
    common_data_fetcher = CommonDataFetcher(bitrix_client)
    entity_fetcher = EntityFetcher(bitrix_client)

    print('Получение общих данных')
    common_data = common_data_fetcher.fetch()

    print('Получение списка тканей')
    fabrics = common_data_fetcher.fetch_all(
        'crm.item.list',
        {'entityTypeId': ID_FABRIC}
    )

    print('Поучение ФОТ')
    fot_data = entity_fetcher.fetch(entity_type_id=ID_FOT)

    data_context = DataContext.from_services(
        common_data['material_prices'],
        common_data['material_coefficients'],
        common_data['fot_coefficients'],
        common_data['queries'],
        fot_data,
        fabrics
    )

    calc_manager = CalculationManager(entity_fetcher, data_context)

    print('Выполнение расчетов')
    # entity_types = ['armchair', 'bed', 'chair', 'melochevka', 'msp', 'nightstand', 'pouf', 'sofa', 'table']
    entity_types = ['chair', ]
    results = {}
    for entity_type in entity_types:
        count = calc_manager.recalculate(entity_type)
        results[entity_type] = count

    return results

if __name__ == '__main__':
    recalculate()
