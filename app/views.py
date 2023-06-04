import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from app.models import Category, Brand, Product, Banner, Cart, Review
from decimal import Decimal as D
from django.db.models import Q
from django.contrib.auth.decorators import login_required


# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            cart_count = Cart.objects.filter(user=request.user).count()
            request.session['cart_count'] = cart_count
            messages.success(request, f'Welcome to Mobify {request.user.username}...')
            return redirect('index')
        else:
            messages.error(request, f'Invalid username or password...')
            return redirect('login')
    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged...')
            return redirect("index")
        context = {}
        return render(request, "app/login.html", context)


def register(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")

        if password != cpassword:
            messages.warning(request, 'confirm password did not match!!!')
            return redirect("register")
        elif username == '' and password == '' and email == '':
            messages.info(request, 'Do not leave empty filed...')
            return redirect("register")
        elif User.objects.filter(Q(username=username) | Q(email=email)):
            messages.warning(request, 'Username or Email has been already taken!!!')
            return redirect("register")
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            messages.success(request, 'New Account created now login...')
            return redirect("login")
    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.warning(request, 'You are alresdy loggedin...')
            return redirect("index")
        return render(request, 'app/register.html')


def logout(request):
    if not request.user.is_authenticated:
        messages.info(request, 'you already logout!!!')
    else:
        auth_logout(request)
        messages.success(request, 'Logout success')
        return redirect("login")


@login_required(login_url="login")
def index(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please Login...')
        return redirect("login")
    category_list = Category.objects.all()
    banner_list = Banner.objects.filter(isEnable=True)
    product_list = Product.objects.filter(category__name__icontains="Mobiles", isPopular=True)
    accessories_list = Product.objects.exclude(category__name__icontains="Mobiles")

    context = {
        "category_list": category_list,
        "banner_list": banner_list,
        "product_list": product_list,
        "accessories_list": accessories_list,
    }
    return render(request, "app/index.html", context)


price_filter_option = [
    {"price_id": 1, "price_range": "0-500"}, {"price_id": 2, "price_range": "500-1000"}, {"price_id": 3, "price_range": "1000-5000"},
    {"price_id": 4, "price_range": "5000-10000"}, {"price_id": 5, "price_range": "10000-20000"}, {"price_id": 6, "price_range": "20000-30000"},
    {"price_id": 7, "price_range": "30000-40000"}, {"price_id": 8, "price_range": "40000-50000"}, {"price_id": 9, "price_range": "50000-60000"},
    {"price_id": 7, "price_range": "60000-70000"}
]


@login_required(login_url="login")
def productDetail(request, pid):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please Login...')
        return redirect("login")
    product_detail = Product.objects.get(id=pid)
    review_list = Review.objects.filter(product__id=product_detail.id)
    if request.method == 'POST':
        comment = request.POST.get("comment")
        rate = request.POST.get("rate")
        if comment == '' or rate == '' or comment is None or rate is None:
            messages.warning(request, "don't submit empty fields")
        else:
            review = Review.objects.create(comment=comment, rate=rate, product=product_detail, user=request.user)
            review.save()
            return redirect("product_detail", pid)
    context = {
        "product_detail": product_detail, "review_list": review_list, "review_count": review_list.count()
    }
    return render(request, "app/product_detail.html", context)


@login_required(login_url="login")
def cart(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please Login...')
        return redirect("login")
    cart_list = Cart.objects.filter(user=request.user)
    final_amount = 0
    for price in cart_list:
        final_amount = price.get_total_price + final_amount
    context = {"cart_list": cart_list, "final_amount": final_amount}
    return render(request, "app/cart.html", context)


@login_required(login_url="login")
def addCart(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please Login...')
        return redirect("login")
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.load(request)
        if data.get("pid"):
            product_detail = Product.objects.get(id=data.get("pid"))
            cart = Cart.objects.filter(user=request.user.id, product__id=product_detail.id)
            if cart:
                # print(request.session['cart_count'])
                messages.warning(request, "Product Already in Cart")
                return JsonResponse({'status': 'Product Already in Cart'}, status=200)
            else:
                add_cart = Cart.objects.create(user=request.user, product=product_detail)
                add_cart.save()
                request.session['cart_count'] = request.session['cart_count'] + 1
                # print(request.session['cart_count'])
                messages.success(request, "New item added in cart...")
                return JsonResponse({"data": "cart added succcess"}, status=200)
        else:
            return JsonResponse({'status': 'Product id is missing'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)


@login_required(login_url="login")
def removeCart(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please Login...')
        return redirect("login")
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.load(request)
        if data.get("cid"):
            cart_detail = Cart.objects.get(id=data.get("cid"))
            cart_detail.delete()
            request.session['cart_count'] = request.session['cart_count'] - 1
            messages.success(request, "cart remove succcess")
            return JsonResponse({"data": "cart item removeed succcess"}, status=200)
        else:
            return JsonResponse({'status': 'cart id is missing'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)


@login_required(login_url="login")
def removeReivew(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please Login...')
        return redirect("login")
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.load(request)
        if data.get("rid"):
            review_detail = Review.objects.get(id=data.get("rid"))
            review_detail.delete()
            messages.success(request, "review remove succcess")
            return JsonResponse({"data": "review remove succcess"}, status=200)
        else:
            return JsonResponse({'status': 'review id is missing'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)


@login_required(login_url="login")
def product(request, cid):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please Login...')
        return redirect("login")
    
    search_product = request.GET.get("search", 0)
    brand_id = request.GET.get("brand", 0)
    price_limit = request.GET.get("price", 0)
    product_list = None
    brand_list = None
    price_filter_list = price_filter_option

    try:
        category = Category.objects.get(id=cid)
    except:
        category = None

    if search_product != 0:
        category = Category.objects.filter(name__icontains=search_product).first()
        brand = Brand.objects.filter(name__icontains=search_product).first()
        if category:
            brand_list = Brand.objects.filter(category__id=category.id)
            product_list = Product.objects.filter(category__id=category.id)
        elif brand:
            product_list = Product.objects.filter(brand__id=brand.id)
            brand_list = Brand.objects.all()
            bdata = Brand.objects.get(id=brand.id)
            brand_id = bdata.id
        else:
            product_list = Product.objects.filter(name__icontains=search_product)
            brand_list = Brand.objects.all()

    elif (brand_id == 0 and price_limit == 0) or (brand_id == '0' and price_limit == '0'):
        product_list = Product.objects.filter(category__id=cid)
        brand_list = Brand.objects.filter(category__id=cid)
    else:
        brand_list = Brand.objects.filter(category__id=cid)
        if price_limit != '0':
            start_price, end_price = price_limit.split("-")
            if brand_id != '0':
                product_list = Product.objects.filter(category__id=cid, brand__id=int(brand_id)).filter(Q(Q(price__range=(D(start_price), D(end_price))) | Q(selling_price__range=(D(start_price), D(end_price)))))
            else:
                product_list = Product.objects.filter(category__id=cid).filter(Q(Q(price__range=(D(start_price), D(end_price))) | Q(selling_price__range=(D(start_price), D(end_price)))))
        else:
            product_list = Product.objects.filter(brand__id=int(brand_id), category__id=cid)

    context = {
        "product_list": product_list,
        "brand_list": brand_list,
        "price_ranges": price_filter_list,
        "brand_id": int(brand_id),
        "price_limit": price_limit,
        "category": category
    }
    return render(request, "app/product.html", context)


@login_required(login_url='login')
def profile(request, id):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please Login...')
        return redirect("login")
    profile_data = User.objects.get(id=id)
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        
        if username == '' and email == '':
            messages.info(request, 'Do not leave empty filed...')
            return redirect("profile", request.user.id)
        else:
            if profile_data.username == username or profile_data.email:
                profile_data.username = username
                profile_data.email = email
                profile_data.save()
                messages.success(request, 'Success')
                return redirect("profile", request.user.id)
            else:
                messages.warning(request, 'Username or Email has been already taken!!!')
                return redirect("profile", request.user.id)
        
    context = {"profile" : profile_data}
    return render(request, "app/profile.html", context)
