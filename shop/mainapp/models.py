from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
User = get_user_model()


class MaxResolutionErrorException(Exception):
    pass


class MinResolutionErrorException(Exception):
    pass


class MaxSizeErrorException(Exception):
    pass


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        products = []
        with_respect_to = kwargs.get("with_respect_to")
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return products


class LatestProducts:

    objects = LatestProductsManager()


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name="Имя категории")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (800, 800)
    MAX_SIZE = 3145728

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="Наиминование")
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name="Изображение")
    description = models.TextField(verbose_name="Описание", null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # image = self.image
        # img = Image.open(image)
        # min_width, min_height = Product.MIN_RESOLUTION
        # max_width, max_height = Product.MAX_RESOLUTION
        # if image.size > Product.MAX_SIZE:
        #     raise MaxSizeErrorException("Размер файла больше 3МБ!")
        # if img.width < min_width or img.height < min_height:
        #     raise MinResolutionErrorException("Разшерение изображение меньше минимального!")
        # if img.width > max_width or img.height > max_height:
        #     raise MaxResolutionErrorException("Разшерение изображение больше максимального!")
        image = self.image
        img = Image.open(image)
        max_width, max_height = Product.MAX_RESOLUTION
        if img.width > max_width or img.height > max_height:
            new_img = img.convert("RGB")
            resized_new_img = new_img.resize((800, 800), Image.ANTIALIAS)
            name = "{}.{}".format(*self.image.name.split("."))
            filestream = BytesIO()
            resized_new_img.save(filestream, "JPEG", quality=90)
            filestream.seek(0)
            self.image = InMemoryUploadedFile(filestream, 'ImageField', name, "jpeg/image", sys.getsizeof(filestream), None)
        super().save(*args, **kwargs)


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name="Покупатель", on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name="Корзина", on_delete=models.CASCADE, related_name="related_products")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Общая стоимость")

    def __str__(self):
        return "Продукт {} для корзины".format(self.product.title)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', verbose_name="Владелец", on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name="related_cart")
    total_products = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Общая стоимость")

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    address = models.CharField(max_length=255, verbose_name="Адрес")

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)


class Notebook(Product):

    diagonal = models.CharField(max_length=255, verbose_name="Диагональ")
    display_type = models.CharField(max_length=255, verbose_name="Тип дисплея")
    processor_freq = models.CharField(max_length=255, verbose_name="Частота процесора")
    ram = models.CharField(max_length=255, verbose_name="Оперативная память")
    video = models.CharField(max_length=255, verbose_name="Видеокарта")
    time_without_charge = models.CharField(max_length=255, verbose_name="Время работи акамулятора")

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)


class Smartphone(Product):

    diagonal = models.CharField(max_length=255, verbose_name="Диагональ")
    display_type = models.CharField(max_length=255, verbose_name="Тип дисплея")
    resolution = models.CharField(max_length=255, verbose_name="Разшерение екрана")
    accum_value = models.CharField(max_length=255, verbose_name="Обьем батареи")
    ram = models.CharField(max_length=255, verbose_name="Оперативная память")
    sd = models.BooleanField(default=True)
    sd_volume_max = models.CharField(max_length=255, verbose_name="Максимальный обьем встраимавой памяти")
    main_cam_mp = models.CharField(max_length=255, verbose_name="Главная камера")
    frontal_cam_mp = models.CharField(max_length=255, verbose_name="Фронтальная камера")

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)
