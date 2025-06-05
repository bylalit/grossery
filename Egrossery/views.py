from django.shortcuts import render, redirect, get_object_or_404
from .models import category, Product, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required 


# Create your views here.
def index(request):
    cart = request.session.get('cart', {})
    item_count = len(cart)
    product = Product.objects.all()[:5]
    # print(product)
    return render(request, 'index.html', {'products': product, 'item_count': item_count, 'user': request.user})

def singal_page(request, product_id):
    products = Product.objects.get(id=product_id)
    # print(products)
    releted_products = Product.objects.filter(category=products.category)[:5]
    # print(releted_products)
    cart = request.session.get('cart', {})
    item_count = len(cart)
    return render(request, 'singal_product.html', {'products': products, 'releted_products': releted_products, 'item_count': item_count, 'user': request.user})

def product(request, category_name):
    # products = Product.objects.all()
    if category_name == 'all products':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category__name=category_name)
    print(products)
    cart = request.session.get('cart', {})
    item_count = len(cart)
    return render(request, 'product.html', {'products': products, 'item_count': item_count, 'user': request.user, 'category_name': category_name})


def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart = request.session.get('cart', {})
    
    if str(product.id) in cart:
        cart[str(product.id)]['quantity'] += 1
    else:
        cart[str(product.id)] = {
            'name': product.name,
            'price': product.price,
            'quantity': 1,
            'image': product.image1.url if product.image1 else None
        }
    
    request.session['cart'] = cart
    request.session.modified = True
    
    # return redirect('home')
    referer = request.META.get('HTTP_REFERER', '/')
    return redirect(referer)


def cart_view(request):
    cart = request.session.get('cart', {})
    total_amount = 0
    
    item_count = len(cart)
    
    for i in cart.values():
        # print(i['price'])
        total_amount += (i['price'] * i['quantity'])
    # print(total_amount)
    
    address = request.session.get('address_details')
    return render(request, 'cart.html', {'cart':cart, 'total_amount': total_amount, 'item_count': item_count, 'user': request.user, 'address': address})
    
    
def update_cart(request, product_id, action):
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        if action == 'increase':
            cart[str(product_id)]['quantity'] += 1
        elif action == "decrease":
            if cart[str(product_id)]['quantity'] > 1:
                cart[str(product_id)]['quantity'] -= 1
            else:
                del cart[str(product_id)]      

    request.session['cart'] = cart
    request.session.modified = True
    
    return redirect("cart_view")

def delete_cart(request, product_id):
    cart = request.session.get("cart", {})
    
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        request.session.modified = True
        
    return redirect("cart_view")


def register(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username Already Exists")
            return redirect('home')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email Already Exists')
            return redirect('home')            
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        messages.success(request, "Account Created Successfully, Please Loged In.")
        
        
    return redirect('home')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request,user)
            messages.success(request, "User Login Succesfully!")
            return redirect(index)
        else:
            messages.error(request, "Invalid username or Password!")
            return redirect(index)    
    
    
    # return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "User LogOut Succesfully!")
    return redirect(index)


@login_required(login_url=('/cart_view'))
def add_address(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        code = request.POST.get('code')
        country = request.POST.get('country')
        phone = request.POST.get('phone')
        
        details = {
            'fname': fname,
            'lname': lname,
            'email': email,
            'street': street,
            'city': city,
            'state': state,
            'code': code,
            'country': country,
            'phone': phone
        }
        
        request.session['address_details'] = details
        
        return redirect('cart_view')
        
    return render(request, 'add_address.html')



@login_required 
def place_order(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        
        if not cart:
            return redirect('cart_view')
        
        total = sum(item['price'] * item['quantity'] for item in cart.values())

        order = Order.objects.create(
            user = request.user,
            address = address,
            phone = phone,
            total_amount = total
        )
        
        for pid, item in cart.items():
            try:
                product = Product.objects.get(id=pid)
                OrderItem.objects.create(
                    order = order,
                    product = product,
                    quantity = item['quantity'],
                    price = item['price']
                )
                
            except Product.DoesNotExist:
                continue

        request.session['cart'] = {}
        request.session.modified = True

        return redirect('my_orders')
    
    return redirect('cart_view')


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-date')
    return render(request, 'my_orders.html', {'orders': orders})








# Admin Section

@login_required(login_url=('/login_dash'))
@staff_member_required
def admin_dash(request):
    categories = category.objects.all()
    if request.method == 'POST':
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        name = request.POST.get('name')
        description = request.POST.get('description')
        categorie_id = request.POST.get('categorie')
        price = request.POST.get('price')
        
        print(image1, image2, image3, name, description, categorie_id, price)
        
        categorie = category.objects.get(id=categorie_id)
        product = Product(image1=image1, image2=image2, image3=image3, name=name, description=description, category=categorie, price=price)
        
        product.save()
        return redirect('admin_dash')
    
    return render(request, 'admin/index.html', {'categories': categories, 'active_page': 'add'})

@staff_member_required
def product_list(request):
    product = Product.objects.all()
    return render(request, 'admin/product_list.html', {'products': product, 'active_page': 'list'})


@staff_member_required
def order_list(request):
    orders = Order.objects.select_related('user').order_by('-date')
    return render(request, 'admin/order_list.html', {'orders': orders, 'active_page': 'odr'})


def login_dash(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_superuser:
                auth_login(request, user)
                messages.success(request, "Admin login successful!")
                return redirect('admin_dash') 
            else:
                messages.error(request, "Access denied. Admins only.")
        else:
            # messages.error(request, "Invalid username or password.")
            messages.add_message(request, messages.WARNING, "Invalid username or password")
        
    return render(request, 'admin/login.html')

def logout_dash(request):
    logout(request)
    messages.success(request, "Admin LogOut Succesfully!")
    return redirect('home')

