from django.urls import path
from app import views

urlpatterns = [
    # auth
    path('', views.login, name = 'login'),
    path('register', views.register, name = 'register'),
    path('logout', views.logout, name = 'logout'),
    # home page
    path('mobify/', views.index, name = 'index'),
    # product, product detail, cart
    path('mobify/product/<int:cid>/', views.product, name = 'product'),
    path('mobify/product/<int:pid>/detail', views.productDetail, name = 'product_detail'),
    path('mobify/cart', views.cart, name = 'cart'),
    path('mobify/profile/<int:id>', views.profile, name = 'profile'),
    # add cart, remove cart
    path('mobify/add-cart', views.addCart, name = 'add_cart'),
    path('mobify/remove-cart', views.removeCart, name = 'remove_cart'),
    path('mobify/remove-review', views.removeReivew, name = 'remove_review'),
]
