from django.urls import include, path

from tasks.views import recalculate_product_calculations


app_name = 'tasks'


urlpatterns = [
    path('recalculate_potocka_products', recalculate_product_calculations)
]
