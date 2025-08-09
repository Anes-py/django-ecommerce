from django.test import TestCase
from django.utils import timezone
from django.shortcuts import reverse

from categories.models import Category, Brand
from core.models import SliderBanners, SideBanners, MiddleBanners, SiteSettings
from .models import Product, Discount, FeatureOption, Comment


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

    def test_persian_slug(self):
        self.product.name= 'محصول تستی'
        self.product.slug = ''
        self.product.save()
        self.assertEqual(self.product.slug, 'محصول-تستی')

    def test_get_final_price_with_discount(self):
        final_price = self.product.get_final_price()
        expected_price = self.product.price * (1 - self.product.discount.value / 100)
        self.assertEqual(final_price, expected_price)

    def test_get_final_price_without_discount(self):
        self.product.discount = None
        self.assertEqual(self.product.get_final_price(), self.product.price)

    def test_get_absolute_url(self):
        self.assertIn(self.product.slug, self.product.get_absolute_url())

    def test_product_active_manager(self):
        active_products = Product.objects.active()
        self.assertIn(self.product, active_products)

    def test_product_with_discount_manager(self):
        products_with_discount = Product.objects.with_discount()
        self.assertIn(self.product, products_with_discount)

    def test_get_final_price_with_expired_discount(self):
        self.product.discount.expire_date = timezone.now() - timezone.timedelta(days=2)
        self.assertEqual(self.product.get_final_price(), self.product.price)

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


class TestHomeView(TestCase):
    def setUp(self):

        self.parent_category = Category.objects.create(name='test category', image='test.jpg')

        discount = Discount.objects.create(
            value=30,
            is_active=True,
            start_date=timezone.now() - timezone.timedelta(days=1),
            expire_date=timezone.now() + timezone.timedelta(days=1),
        )

        Product.objects.create(
            name='test product',
            price=100,
            main_image='product.jpg',
            short_description='short description',
            description='description',
            category=self.parent_category,
            discount=discount,
        )

    def test_home_view_url(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_context_data_with_site_settings(self):
        site_setting = SiteSettings.objects.create(site_name='Test Shop name')

        SliderBanners.objects.create(site_setting=site_setting, title="slider", image="slider.jpg")
        SideBanners.objects.create(site_setting=site_setting, title="side", image="side.jpg")
        MiddleBanners.objects.create(site_setting=site_setting, title="middle", image="middle.jpg")

        response = self.client.get(reverse('home'))
        self.assertIn('slider_banners', response.context)
        self.assertIn('side_banners', response.context)
        self.assertIn('middleBanners', response.context)
        self.assertIn('discounted_products', response.context)
        self.assertIn('newest_products', response.context)
        self.assertIn('top_categories', response.context)

    def test_home_view_context_data_without_site_settings_obj(self):
        response = self.client.get(reverse('home'))
        self.assertNotIn('slider_banners', response.context)
        self.assertNotIn('side_banners', response.context)
        self.assertNotIn('middleBanners', response.context)
        self.assertIn('discounted_products', response.context)
        self.assertIn('newest_products', response.context)
        self.assertIn('top_categories', response.context)


class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='test category', image='category.jpg')
        discount = Discount.objects.create(
            value=30,
            is_active=True,
            start_date=timezone.now() - timezone.timedelta(days=1),
            expire_date=timezone.now() + timezone.timedelta(days=1),
        )
        discount_2 =Discount.objects.create(
            value=30,
            is_active=True,
            start_date=timezone.now() - timezone.timedelta(days=1),
            expire_date=timezone.now() + timezone.timedelta(days=1),
        )

        self.product = Product.objects.create(
            category=self.category,
            name='test product',
            main_image='product.jpg',
            short_description='test short dec',
            description='test long dec',
            price=100,
            discount=discount,
            stock=10,
        )

        self.comment = Comment.objects.create(
            product=self.product,
            display_name='test name',
            title='test title',
            text='test text',
            recommend=True,
            status=Comment.CommentStatus.APPROVED,
        )

        FeatureOption.objects.create(
            product=self.product,
            feature=FeatureOption.Feature.Color,
            color=FeatureOption.Color.BLUE,
        )

        FeatureOption.objects.create(
            product=self.product,
            feature=FeatureOption.Feature.Size,
            value=45,
        )
        self.related_product = Product.objects.create(
            category=self.category,
            name='test product2',
            main_image='product2.jpg',
            short_description='test short dec2',
            description='test long dec2',
            price=100,
            discount=discount_2,
            stock=10,
        )
    def test_view_url(self):
        response = self.client.get(reverse('product-detail', args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)

    def test_context_contains_product(self):
        response = self.client.get(reverse('product-detail', args=[self.product.slug]))
        self.assertEqual(response.context['object'], self.product)

    def test_context_contains_related_products(self):
        response = self.client.get(reverse('product-detail', args=[self.product.slug]))
        related_products = response.context['related_products']
        self.assertIn(self.related_product, related_products)
        self.assertNotIn(self.product, related_products)

    def test_context_contains_color_options(self):
        response = self.client.get(reverse('product-detail', args=[self.product.slug]))
        color_options = response.context['color_options']
        color =  [{'code': 'blue', 'name': 'blue'}]
        self.assertEqual(color_options, color)

    def test_context_contains_size_option(self):
        response = self.client.get(reverse('product-detail', args=[self.product.slug]))
        size_options = response.context['size_options']
        self.assertIn('45', size_options)

    def test_context_contains_comment(self):
        response = self.client.get(reverse('product-detail', args=[self.product.slug]))
        self.assertIn(self.comment, response.context['comments'])
