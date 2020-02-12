from django.test import TestCase


class OrderTest(TestCase):
    def test_add_success(self):
        vip_product = self.gen_vip_product()
        normal_product = self.gen_normal_product()

        with self.subTest(msg='VIP order VIP product', product=vip_product, is_vip=True):
            order = self.order_product(is_vip=is_vip, product=product, quantity=1)
            self.assertEqual(order.status_code, 204)

        with self.subTest(msg='VIP order normal product', product=normal_product, is_vip=True):
            order = self.order_product(is_vip=is_vip, product=product, quantity=1)
            self.assertEqual(order.status_code, 204)

        with self.subTest(msg='Normal user order normal product', product=normal_product, is_vip=False):
            order = self.order_product(is_vip=is_vip, product=product, quantity=1)
            self.assertEqual(order.status_code, 204)

    def test_add_fail(self):
        vip_product = self.gen_vip_product()

        with self.subTest(msg='normal user order VIP product'):
            order = self.order_product(is_vip=False, product=vip_product, quantity=1)
            self.assertNotEqual(order.status_code, 204)

        with self.subTest(msg='order too many product'):
            order = self.order_product(is_vip=True, product=vip_product, quantity=100)
            self.assertNotEqual(order.status_code, 204)

    def test_remove(self):
        product = self.gen_normal_product()
        order = self.order_product(is_vip=False, product=product, quantity=1)
        product_quantity_after_order = product.quantity

        self.remove_order(order)
        product.refresh()
        product_quantity_after_remove = product.quantity

        self.assertEqual(product_quantity_after_order + 1, product_quantity_after_remove)

    def test_order_status_change(self):
        order = self.gen_order()
        self.assertTrue(order.can_be_fullfilled)
        self.item_sold_out(order)
        self.assertFalse(order.can_be_fullfilled)
        self.buy_in_item(order)
        self.assertTrue(order.can_be_fullfilled)

    def gen_vip_product(self):
        pass

    def gen_normal_product(self):
        pass

    def order_product(self, is_vip, product, quantity):
        pass

    def remove_order(self, order):
        pass

    def item_sold_out(order):
        pass

    def buy_in_item(order):
        pass


class ReportTest(TestCase):
    def test_gen_by_shop(self):
        shop = self.gen_shop()
        self.make_transaction_for(shop)
        report = self.gen_report_for(shop)
        self.assertListEqual(['sale', 'quantity', 'order'], report.keys())

    def test_gen_top_three(self):
        shop = self.gen_shop()
        self.make_transaction_for(shop)
        report = self.get_top_three()
        self.assertEqual(3, len(report))

    def gen_shop(self):
        pass

    def make_transaction_for(self, shop):
        pass

    def gen_report_for(self, shop):
        pass

    def get_top_three(self):
        pass
