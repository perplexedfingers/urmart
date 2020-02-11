from django.db import models


class User(models):
    pass


class Shop(models):
    @property
    def total_sale_gained(self):
        return sum(product.price * detail.quantity
                   for product in self.product_set.objects.all()
                   for detail in product.orderdetail_set.objects.all()
                   )

    @property
    def total_orders_taken(self):
        return sum(detail.order_set.objects.distinct().count()
                   for product in self.product_set.objects.all()
                   for detail in product.orderdetail_set.objects.all()
                   )

    @property
    def total_quantity_sold(self):
        return sum(detail.quantity
                   for product in self.product_set.objects.all()
                   for detail in product.orderdetail_set.objects.all()
                   )


class Product(models):
    from_shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    intentory_count = models.IntegerField()
    price = models.IntegerField()
    is_vip_only = models.BooleanField()

    @property
    def ordered(self):
        return sum(detail.quantity for detail in self.orderdetail_set.objects.all())

    @property
    def is_available(self):
        return self.intentory_count > self.ordered

    def is_order_accepted(self, quantity):
        remaining = self.intentory_count - self.ordered
        return quantity > remaining


class Order(models):
    by_user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def can_be_fullfilled(self):
        return all((detail.quantity <= detail.product.inventory_count
                    for detail in self.orderdetail_set.all()))


class OrderDetail(models):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
