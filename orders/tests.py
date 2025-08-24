from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import reverse




from cart.models import Cart, CartItem
from categories.models import Category
from orders.models import Address, Order
from products.models import Product, Discount


class OrderViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='test_user124')
        self.user.set_password('123pass')
        self.user.save()
        self.category = Category.objects.create(
            name='test category',
            image='test.jpg',
        )
        self.discount = Discount.objects.create(
            value=15,
            start_date=timezone.now() - timezone.timedelta(days=1),
            expire_date=timezone.now() + timezone.timedelta(days=1)
        )

        self.product = Product.objects.create(
            category=self.category,
            name='product test name',
            main_image='test.jpg',
            short_description='test short description',
            description='test description',
            price=72000000,
            discount=self.discount,
            stock=5,
        )
        self.cart = Cart.objects.create(
            user=self.user
        )
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=1,
        )

        self.address = Address.objects.create(
            user=self.user,
            full_name='test address',
            phone='981231231234',
            country='iran',
            state='tehran',
            city='tehran',
            postal_code=123456789,
            full_address='test address',
        )
    def test_order_create_view(self):
        self.client.login(username='test_user124', password='123pass')

        response = self.client.post(reverse('checkout-cart'), {
            'shipping_address':self.address.id,
            'notes':'test note',
            'payment_method':Order.PaymentMethodChoices.CARD,
            'shipping_method':Order.ShippingMethod.FAST,
        })
        self.assertEqual(response.status_code, 302)

        order = Order.objects.first()
        self.assertIsNotNone(order)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.items.count(), 1)

    def test_order_detail_view_requires_login(self):
        response = self.client.get(reverse('order-detail'))
        self.assertRedirects(response, f'/accounts/login/?next={reverse("order-detail")}')

    def test_order_detail_view_authenticated(self):
        self.client.login(username='test_user124', password='123pass')

        order = Order.objects.create(
            user=self.user,
            shipping_address=self.address,
            status=Order.OrderStatus.PENDING_PAYMENT,
            subtotal=1000,
            discount_total=100,
            shipping_total=28,
            tax_total=10,
            grand_total=938,
        )
        response = self.client.get(reverse('order-detail'))
        self.assertEqual(response.status_code, 200)

