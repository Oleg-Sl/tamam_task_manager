from django.urls import include, path

from tasks.views import recalculate_product_calculations
from tasks.views import recalculate_product


app_name = 'tasks'


urlpatterns = [
    path('recalculate_potocka_products', recalculate_product_calculations),
    path('recalculate_product/', recalculate_product),

]
