from django.db import models
from django.contrib.auth.models import User
from django.db.models import CharField


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("id",)

    def __str__(self) -> CharField:
        return self.name


class Brand(models.Model):
    category = models.ManyToManyField(Category, related_name="brand_category")
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    img = models.ImageField(upload_to="Brands/", max_length=250, default="default_image.png", null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    isMobile = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("id",)

    def __str__(self) -> CharField:
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="product_category")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    img = models.ImageField(upload_to="mobiles/", max_length=250, default="default_image.png", null=True, blank=True)
    discription = models.TextField(max_length=300, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default="0", null=True, blank=True)
    discount = models.DecimalField(max_digits=3, decimal_places=1, default="0", null=True, blank=True)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, default="0", null=True, blank=True)
    isStacksAvailable = models.BooleanField(default=True)
    isPopular = models.BooleanField(default=False)
    quantity = models.PositiveSmallIntegerField(default="0", null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-id",)

    def __str__(self) -> CharField:
        return self.name

    def save(self, *args, **kwargs):
        if self.discount != 0.0 or self.discount != 0:
            self.selling_price = self.get_final_price
        else:
            self.selling_price = self.price
        super(Product, self).save(*args, **kwargs)

    @property
    def get_final_price(self):
        if self.discount != 0.0 or self.discount != 0:
            discount_price = (self.discount / 100) * self.price
            final_price = self.price - discount_price
            return round(final_price, 2)
        else:
            return round(self.price, 2)

    @property
    def get_mobile_full_name(self):
        return f"{self.brand__name} {self.name}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(default="0", null=True, blank=True)
    comment = models.TextField(max_length=250, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-id",)

    def __str__(self) -> str:
        return self.product.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default="1", null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-id",)

    def __str__(self) -> str:
        return self.product.name

    @property
    def get_total_price(self):
        final_price = self.product.get_final_price * self.quantity
        return final_price


class Shipping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=150, null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    state = models.CharField(max_length=150, null=False, blank=False)
    pincode = models.CharField(max_length=6, null=False, blank=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.username


class Banner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    banner_img = models.ImageField(upload_to="banner/", max_length=250, default="default_image.png", null=True, blank=True)
    isEnable = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.user.username
