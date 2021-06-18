from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import ugettext as _
from market.models import Market
from market.forms import AddMarketForm, CloseMarketForm

# Create your views here.
FORM_TEMPLATE = 'form.html'
MARKET_TEMPLATE = 'market.html'
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
    if market.status == Market.MarketStatus.DEACTIVE:
        if market.redirect_to:
            return redirect('view_market', market_name=market.redirect_to.name,
                            permanent=market.redirect_permanently)
        else:
            raise Http404()
    return render(request, MARKET_TEMPLATE, {'market': market})



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


@staff_member_required
def close_market(request, market_id):
    market = get_object_or_404(Market, id=market_id)
    if request.method == 'POST':
        form = CloseMarketForm(request.POST, instance=market)
        if form.is_valid():
            form.save()
            return redirect('all_markets')
    else:
        form = CloseMarketForm(instance=market)
    data = {
        'title': _('انتقال آدرس حجره'),
        'subtitle': _(f'شما در حال انتقال حجره {market} هستید'),
        'form': form
    }
    return render(request, FORM_TEMPLATE, data)



