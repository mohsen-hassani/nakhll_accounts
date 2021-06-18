from django.urls import path
from market.views import all_markets, add_market, close_market, view_market

urlpatterns = [
    path('all/', all_markets, name='all_markets'),
    path('add-market/', add_market, name='add_market'),
    path('close-market/<int:market_id>/', close_market, name='close_market'),
    path('<str:market_name>/', view_market, name='view_market'),
]