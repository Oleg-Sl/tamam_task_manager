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


def recalculate(params: Dict) -> Dict[str, int]:
    product_type_id = params.get('product_type_id')
    product_id = params.get('product_id')
    print('product_type_id = ', product_type_id)
    print('product_id = ', product_id)

    setup()

    bitrix_client = BitrixClient()
    common_data_fetcher = CommonDataFetcher(bitrix_client)
    entity_fetcher = EntityFetcher(bitrix_client)

    print('Получение общих данных')
    common_data = common_data_fetcher.fetch()
    # print(common_data)

    # product = entity_fetcher.fetch_one(entity_type_id=product_type_id, entity_id=product_id)

    # fabrics = []
    fabrics = common_data_fetcher.fetch_all(
        'crm.item.list',
        {'entityTypeId': ID_FABRIC}
    )

    print('Поучение ФОТ')
    fot_data = entity_fetcher.fetch(entity_type_id=ID_FOT, filter_data={f'parentId{product_type_id}': product_id})

    data_context = DataContext.from_services(
        common_data['material_prices'],
        common_data['material_coefficients'],
        common_data['fot_coefficients'],
        common_data['queries'],
        fot_data,
        fabrics
    )

    calc_manager = CalculationManager(entity_fetcher, data_context)
    count = calc_manager.recalculate_one_product(product_type_id, product_id)
    return {'count': count}
    # print('Выполнение расчетов')
    # entity_types = ['armchair', 'bed', 'chair', 'melochevka', 'msp', 'nightstand', 'pouf', 'sofa', 'table']
    # # entity_types = ['chair', ]
    # results = {}
    # for entity_type in entity_types:
    #     count = calc_manager.recalculate(entity_type)
    #     results[entity_type] = count
    #
    # return results


if __name__ == '__main__':
    recalculate({
        'product_type_id': 158,
        # 'product_type': 'bed',
        'product_id': 1951,
    })
