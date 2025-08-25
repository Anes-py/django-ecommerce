from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import reverse

from categories.models import Category
from products.models import Product, Discount
from .models import Cart, CartItem

class CartViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='test_user124')
        self.user.set_password('123pass')
        self.user.save()
        self.discount = Discount.objects.create(
            value=10,
            start_date=timezone.now() - timezone.timedelta(days=1),
            expire_date=timezone.now() + timezone.timedelta(days=1),
        )
        self.category = Category.objects.create(name='test category', image='category.jpg')

        self.product = Product.objects.create(
            category=self.category,
            name='test category',
            main_image='product.jpg',
            short_description='test short description',
            description='test long description',
            price=100,
            discount=self.discount,
            stock=5,
        )
        self.cart, _ = Cart.objects.get_or_create(user=self.user)

    def test_cart_authenticated_user(self):
        self.assertTrue(self.client.login(username='test_user124', password='123pass'))
        url = reverse('cart-detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('cart', response.context)

    def test_cart_guest_user(self):
        url = reverse('cart-detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('cart', response.context)
        self.assertTrue(self.client.session.session_key)

    def test_add_to_cart_authenticated_user(self):
        self.assertTrue(self.client.login(username='test_user124', password='123pass'))
        url = reverse('cart-add', args=[self.product.id])
        data={
            'quantity':2,
            'color':'Red',
            'size':38,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        cart = Cart.objects.get(user=self.user)
        cart_item = CartItem.objects.get(cart=cart, product=self.product)
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart_item.color, 'Red')
        self.assertEqual(cart_item.size, '38')

    def test_add_to_cart_guest_user(self):
        url = reverse('cart-add', args=[self.product.id])
        data = {
            'quantity':3,
            'color':'Blue',
            'size':38,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        session_key = self.client.session.session_key
        self.assertIsNotNone(session_key)
        cart = Cart.objects.get(session_key=self.client.session.session_key)
        cart_item = CartItem.objects.get(cart=cart, product=self.product)
        self.assertEqual(cart_item.quantity, 3)
        self.assertEqual(cart_item.quantity, 3)
        self.assertEqual(cart_item.color, 'Blue')
        self.assertEqual(cart_item.size, '38')

    def test_add_to_cart_invalid_form(self):
        self.client.login(username='test_user124', password='123pass')
        url = reverse('cart-add', args=[self.product.id])
        data = {
            'quantity':0,
            'color':'Black',
            'size':38.
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CartItem.objects.exists())

    def test_remove_from_cart(self):
        self.client.login(username='test_user124', password='123pass')
        url = reverse('cart-add', args=[self.product.id])
        data = {
            'quantity':1,
            'color':'Blue',
            'size':38,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        cart_item = CartItem.objects.get(cart=self.cart, product=self.product)

        response = self.client.post(reverse('cart-remove', args=[cart_item.id]))
        self.assertEqual(response.status_code, 302)

        self.assertFalse(CartItem.objects.filter(id=cart_item.id).exists())

    def test_cart_delete_view(self):
        self.client.login(username='test_user124', password='123pass')
        self.assertTrue(Cart.objects.filter(pk=self.cart.pk).exists())

        response = self.client.post(reverse('cart-delete'))

        self.assertFalse(Cart.objects.filter(pk=self.cart.pk).exists())
        self.assertEqual(response.status_code, 302)
