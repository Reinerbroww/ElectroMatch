from django.shortcuts import render
from .models import Product, ProductValue


def catalog(request):
    products = Product.objects.select_related('category').all()
    values = ProductValue.objects.select_related('criteria').filter(product__in=products)
    value_map = {}
    for pv in values:
        value_map.setdefault(pv.product_id, []).append(pv)

    items = []
    for p in products:
        items.append({'product': p, 'values': value_map.get(p.id, [])})

    return render(request, 'core/catalog.html', {'items': items})
