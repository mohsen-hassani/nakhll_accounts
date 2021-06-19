from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _
from market.models import Market, Product, Redirect, Status
from market.forms import AddMarketForm, CloseObjectForm, AddProductForm

# Create your views here.
FORM_TEMPLATE = 'form.html'
MARKET_TEMPLATE = 'market.html'
PRODUCT_TEMPLATE = 'product.html'
ALL_MARKETS_TEMPLATE = 'all_markets.html'

def all_markets(requset):
    active_markets = Market.markets.active()
    closed_markets = Market.markets.deactive()
    data = {
        'active_markets': active_markets,
        'closed_markets': closed_markets,
    }
    return render(requset, ALL_MARKETS_TEMPLATE, data)

def view_market(request, market_name):
    market = get_object_or_404(Market, name=market_name)
    if market.status == Status.DEACTIVE:
        market_content_type = ContentType.objects.get_for_model(market)
        market_id = market.id
        redirect_object = Redirect.objects.filter(src_content_type=market_content_type, src_object_id=market_id).first()
        if redirect_object:
            return redirect(redirect_object.dst_content_object, permanent=redirect_object.redirect_permanently)
        else:
            raise Http404()
    return render(request, MARKET_TEMPLATE, {'market': market})

def view_product(request, market_name, product_name):
    market = get_object_or_404(Market, name=market_name)
    product = get_object_or_404(Product, market=market, name=product_name)
    if product.status == Status.DEACTIVE:
        product_content_type = ContentType.objects.get_for_model(product)
        product_id = product.id
        redirect_object = Redirect.objects.filter(src_content_type=product_content_type, src_object_id=product_id).first()
        if redirect_object:
            return redirect(redirect_object.dst_content_object, permanent=redirect_object.redirect_permanently)
        else:
            raise Http404()
    return render(request, PRODUCT_TEMPLATE, {'product': product})

   

@login_required
def add_market(request):
    if request.method == 'POST':
        form = AddMarketForm(request.POST)
        if form.is_valid():
            market = form.save(commit=False)
            market.user = request.user
            market.save()
            return redirect('view_market', market_name=market.name)
    else:
        form = AddMarketForm()
    data = {
        'title': _('ایجاد حجره جدید'),
        'form': form
    }
    return render(request, FORM_TEMPLATE, data)

@login_required
def add_product(request, market_name):
    market = get_object_or_404(Market, name=market_name) #, user=request.user)
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.market = market
            product.save()
            return redirect('view_market', market_name=market.name)
    else:
        form = AddProductForm()
    data = {
        'title': _('ایجاد محصول جدید'),
        'subtitle': _(f'برای حجره {market}'),
        'form': form
    }
    return render(request, FORM_TEMPLATE, data)



@staff_member_required
def close_market(request, market_id):
    market = get_object_or_404(Market, id=market_id)
    market_content_type = ContentType.objects.get_for_model(market)
    market_id = market.id
    redirect_object, created = Redirect.objects.get_or_create(src_content_type=market_content_type, src_object_id=market_id)
    if request.method == 'POST':
        form = CloseObjectForm(request.POST, instance=redirect_object)
        if form.is_valid():
            form.save()
            return redirect('all_markets')
    else:
        form = CloseObjectForm(instance=redirect_object)
    data = {
        'title': _('انتقال آدرس حجره'),
        'subtitle': _(f'شما در حال انتقال حجره {market} هستید'),
        'form': form,
        'extra_script_file': 'js/object_loader.js',
    }
    return render(request, FORM_TEMPLATE, data)


@staff_member_required
def close_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_content_type = ContentType.objects.get_for_model(product)
    product_id = product.id
    redirect_object, created = Redirect.objects.get_or_create(src_content_type=product_content_type, src_object_id=product_id)
    if request.method == 'POST':
        form = CloseObjectForm(request.POST, instance=redirect_object)
        if form.is_valid():
            form.save()
            return redirect('view_market', market_name=product.market.name)
    else:
        form = CloseObjectForm(instance=redirect_object)
    data = {
        'title': _('انتقال آدرس حجره'),
        'subtitle': _(f'شما در حال انتقال حجره {product} هستید'),
        'form': form,
        'extra_script_file': 'js/object_loader.js',
    }
    return render(request, FORM_TEMPLATE, data)


