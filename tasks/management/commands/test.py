import json

from django.core.management.base import BaseCommand, CommandError
from django.utils.module_loading import import_string
from django.utils import timezone

from tasks.recalculate_product_calculation.recalculate_product import recalculate


class Command(BaseCommand):
    help = "Recalculation of product calculations"

    def handle(self, *args, **options):
        recalculate({
            'product_type_id': 158,
            'product_id': 1951,
            # 'product_type_id': 189,
            # 'product_id': 1855,
        })
