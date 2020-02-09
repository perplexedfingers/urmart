from django.db import models


class User(models):
    pass


class Shop(models):
    @property
    def total_sale_gained(self):
        sum_ = sum(product.price * detail.quantity
                   for product in self.product_set.objects.all()
                   for detail in product.orderdetail_set.objects.all()
                   )
        return sum_

    @property
    def total_orders_taken(self):
        sum_ = sum(detail.order_set.objects.distinct().count()
                   for product in self.product_set.objects.all()
                   for detail in product.orderdetail_set.objects.all()
                   )
        return sum_

    @property
    def total_quantity_sold(self):
        sum_ = sum(detail.quantity
                   for product in self.product_set.objects.all()
                   for detail in product.orderdetail_set.objects.all()
                   )
        return sum_


class Product(models):
    from_shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    intentory_count = models.IntegerField()
    price = models.IntegerField()
    is_vip_only = models.BooleanField()

    @property
    def ordered(self):
        ordered_ = sum(detail.quantity for detail in self.orderdetail_set.objects.all())
        return ordered_

    @property
    def is_available(self):
        return self.intentory_count > self.ordered

    def is_order_accepted(self, quantity):
        remaining = self.intentory_count - self.ordered
        return quantity > remaining


class Order(models):
    by_user = models.ForeignKey(User, on_delete=models.CASCADE)


class OrderDetail(models):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
