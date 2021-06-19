import json
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from market.models import Market, Product

def markets_json(request):
    active_markets = Market.markets.active()
    markets = []
    for market in active_markets:
        markets.append({
            'id': market.id,
            'name': market.name,
        })
    return HttpResponse(json.dumps(markets), content_type='application/json')

def products_json(request):
    active_products = Product.products.active()
    products = []
    for product in active_products:
        products.append({
            'id': product.id,
            'name': product.name,
        })
    return HttpResponse(json.dumps(products), content_type='application/json')

def objects_json(request):
    content_type_id = request.GET.get('id')
    content_type = ContentType.objects.get(id=content_type_id)
    objects = content_type.get_all_objects_for_this_type()
    all_objects = []
    for obj in objects:
        all_objects.append({
            'id': obj.id,
            'name': str(obj),
        })
    return HttpResponse(json.dumps(all_objects), content_type='application/json')

