from django.urls import path
from market.views import all_markets, add_market, add_product,\
     close_market, close_product, view_market, view_product
from market.simple_api import markets_json, objects_json, products_json

urlpatterns = [
    path('api/objects/', objects_json, name='objects_json'),
    path('all/', all_markets, name='all_markets'),
    path('add-market/', add_market, name='add_market'),
    path('<str:market_name>/add-product/', add_product, name='add_product'),
    path('close-market/<int:market_id>/', close_market, name='close_market'),
    path('close-product/<int:product_id>/', close_product, name='close_product'),
    path('<str:market_name>/', view_market, name='view_market'),
    path('<str:market_name>/<str:product_name>/', view_product, name='view_product'),
]