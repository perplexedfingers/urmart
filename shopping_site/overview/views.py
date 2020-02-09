from functools import wraps

from django.shortcuts import render

from .models import Order, Product, Shop, User


def is_right_role(f, *arg, **kw):
    @wraps
    def _is_right_role(f, request, *args, **kw):
        product = ?
        not_vip = ?
        if product.is_vip_only and not_vip:
            raise
        else:
            return f(request, *args, **kw)
    return _is_right_role


def is_available(f, *arg, **kw):
    @wraps
    def _is_available(f, request, *args, **kw):
        product = ?
        quantity = ?
        if POST:
            if product.is_order_accepted(quantity):
                pass
            else:
                pass
        elif DELETE:
            pass
    return _is_available


@is_right_role
@is_available
def order(request):
    if POST:
        show button if unavailable
    elif DELETE:
        update other orders


def product_top_three(request):
    top_three = Product.objects.annotate(
        total_sale=Sum('orderdetail_quantity'))\
        .order_by('-total_sale')[:3]
    return [product for product in top_three]


def shop_report(request):
    report = {
        shop.pk: {'sale': shop.total_sale_gained,
                  'quantity': shop.total_quantity_sold,
                  'order': shop.total_orders_taken}
        for shop in Shop.objects.all()}
    return report
