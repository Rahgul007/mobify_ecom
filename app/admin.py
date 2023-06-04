from django.contrib import admin
from app import models

# Register your models here.


class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "img", "isMobile",)
    list_display_links = ("id", "name",)

class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "brand", "disc", "price", "discount", "isStacksAvailable", "isPopular","quantity", "get_final_price",)
    list_display_links = ("id", "name",)
    
    def disc(self, obj):
        return obj.discription[:100]
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)
    list_display_links = ("id", "name",)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "rate", "comment",)
    list_display_links = ("id", "user",)

class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "quantity", "get_total_price")
    list_display_links = ("id", "user",)

# class ShippingAddress(admin.ModelAdmin):
#     list_display = ("id", "user", "location", "state", "pincode",)
#     list_display_links = ("id", "user",)

class BannerAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "banner_img","isEnable", "createdAt", "updatedAt",)
    list_display_links = ("id", "user",)
    

admin.site.register(models.Brand, BrandAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Review, ReviewAdmin)
admin.site.register(models.Cart, CartAdmin)
# admin.site.register(models.ShippingAddress, ShippingAddress)
admin.site.register(models.Banner, BannerAdmin)