from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Category, Brand


class TestCategoryModel(TestCase):
    def setUp(self):
        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake-image-content',
            content_type='image/jpg',
        )

    def test_create_category(self):
        category = Category.objects.create(
            name="category test",
            image=self.image
        )
        self.assertEqual(category.name, 'category test')
        self.assertTrue(category.slug)
        self.assertEqual(category.slug, 'category-test')

    def test_persian_slug(self):
        category = Category.objects.create(name="لپتاپ ایسوس", image=self.image)
        self.assertTrue(category.slug)
        self.assertEqual(category.slug, 'لپتاپ-ایسوس')

    def test_parent_category(self):
        parent = Category.objects.create(name="الکترونیک", image=self.image)
        child = Category.objects.create(name="لپ‌تاپ", parent=parent, image=self.image)
        self.assertEqual(child.parent, parent)

    def test_ordering_by_created_at(self):
        category1 = Category.objects.create(name='category1')
        category2 = Category.objects.create(name='category2')
        self.assertGreater(category2.created_at, category1.created_at)


class TestBrandModel(TestCase):
    def test_create_brand(self):
        brand = Brand.objects.create(name='brand name')
        self.assertEqual(brand.slug, 'brand-name')

    def test_ordering_by_created_at(self):
        brand1 = Brand.objects.create(name='brand1')
        brand2 = Brand.objects.create(name='brand2')
        self.assertGreater(brand2.created_at, brand1.created_at)