from django.test import TestCase
from django.utils import timezone

from categories.models import Category, Brand
from .models import Product, Discount


class TestProductModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='test category')
        self.brand = Brand.objects.create(name="test brand")
        self.discount = Discount.objects.create(
            value=10,
            is_active=True,
            start_date=timezone.now() - timezone.timedelta(days=1),
            expire_date=timezone.now() + timezone.timedelta(days=1),
        )
        self.product = Product.objects.create(
            name='test product',
            price=100,
            stock=5,
            category=self.category,
            brand=self.brand,
            discount=self.discount,
            is_active=True
        )

    def test_str_method(self):
        self.assertEqual(str(self.product), 'test product')

    def test_slug_auto_creating(self):
        self.assertTrue(self.product.slug)
        self.assertEqual(self.product.slug, 'test-product')

    def test_get_final_price_with_discount(self):
        final_price = self.product.get_final_price()
        expected_price = self.product.price * (1 - self.product.discount.value / 100)
        self.assertEqual(final_price, expected_price)

    def test_get_final_price_without_discount(self):
        self.product.discount = None
        self.assertEqual(self.product.get_final_price(), self.product.price)

    # def test_get_absolute_url(self):
    #     self.assertIn(self.product.slug, self.product.get_absolute_url())

    def test_product_active_manager(self):
        active_products = Product.objects.active()
        self.assertIn(self.product, active_products)

    def test_product_with_discount_manager(self):
        products_with_discount = Product.objects.with_discount()
        self.assertIn(self.product, products_with_discount)

    def test_product_ordering(self):
        p2 = Product.objects.create(
            name='test product 2',
            price=100,
            stock=2,
            category=self.category,
            brand=self.brand,
            is_active=True,
        )
        ordered = list(Product.objects.newest())
        self.assertEqual(ordered[0], p2)

