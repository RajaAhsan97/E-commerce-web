from datetime import datetime
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import request, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.forms import formset_factory
from .forms import RegisterationForm, LoginForm, ProductAddForm, CategoryCreateForm, ProductSpecsAddForm
from .models import Category, Product, ProductSpecifications
from customer_logs.models import Customer, Cart, CartProducts
import weasyprint
from django.template.loader import render_to_string

def homeView(request):
    categories = Category.objects.all()
    print("session: ", request.user)
    admin_name = request.user.username

    customer = Cart.objects.filter(name=admin_name).first()
    customer_cart = []
    if customer:
        customer_cart = customer.customer_cart.all()

    return render(request, 'ecommerce_platform/home.html', {'admin': admin_name,
                                         'categories': categories, "customer_cart": customer_cart})

def RegistrationView(request):
    msg = None
    if request.method == 'POST':
        registerForm = RegisterationForm(request.POST)

        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.set_password(registerForm.cleaned_data['password'])
            user.save()

            # save registered customer to customer model
            Customer.objects.create(customer_name=registerForm.cleaned_data['username'],
                                    email=registerForm.cleaned_data['email'])

            return redirect('home')
        else:
            msg = "User already exist or you have provided invalid data to sign-up"
    else:
        registerForm = RegisterationForm()
    return render(request, 'ecommerce_platform/authentication/signup.html', {'form': registerForm, 'error_msg': msg})

def LoginView(request):
    msg = None

    if request.method == 'POST':
        logForm = LoginForm(request.POST)
        if logForm.is_valid():
            cd = logForm.cleaned_data

            user = authenticate(request, username=cd['username'], password=cd['password'])

            if user:
                login(request, user)
                # if admin is signed in then redirect to admin panel and if not admin then redirect to the home page
                if user.is_staff:
                    return redirect('admin-panel', user.username)
                else:
                    return redirect('home')
            else:
                msg = "Please sign-up first, to login"
    else:
        logForm = LoginForm()
    return render(request, 'ecommerce_platform/authentication/login.html', {'form': logForm, 'error_msg': msg})

def LogoutView(request):
    logout(request)

    return redirect('home')

def Admin(request, admin_name):
    categories = Category.objects.all()

    recent_category = None
    if categories:
        last_category_time = categories.last().created
        current_time = datetime.now()
        time_diff = current_time - last_category_time
        recent_category = None
        if time_diff.seconds < 7:
            recent_category = categories.last().category_name

    return render(request, 'ecommerce_platform/admin/admin_panel.html', {'admin': admin_name,
                                                      'recent_category': recent_category,
                                                      'categories': categories})

def CreateCategory(request):
    print("Category create function executed...")
    admin_name = request.user.username
    print(admin_name)
    if request.method == 'POST':
        CategoryForm = CategoryCreateForm(request.POST, request.FILES)
        if CategoryForm.is_valid():
            cd = CategoryForm.cleaned_data

            category_obj = Category.objects.create(category_name=cd['category_name'], image=cd['image'])
            category_obj.save()

            return redirect('admin-panel', admin_name)
    else:
        CategoryForm = CategoryCreateForm()

    return render(request, 'ecommerce_platform/admin/actions/category_create.html', {'admin': admin_name,
                                                                  'form': CategoryForm})

def DeleteCategory(request, category_id):
    Category.objects.get(pk=category_id).delete()
    admin_name = request.user.username

    return redirect('admin-panel', admin_name)

def Products(request, category_name):
    category = Category.objects.get(category_name=category_name)
    category_products = category.category_product.all()

    recent_product = None
    if category_products:
        last_added_product_time = category_products.last().created
        current_time = datetime.now()
        time_diff = current_time - last_added_product_time

        if time_diff.seconds < 7:
            recent_product = category_products.last()

    admin_name = request.user.username
    return render(request, 'ecommerce_platform/admin/products.html', {'admin': admin_name,
                                                   'category': category,
                                                   'recent_product': recent_product,
                                                   'products': category_products})

def DeleteProduct(request, product_id):
    product = Product.objects.get(pk=product_id)
    category = Category.objects.get(pk=product.category_id).category_name
    product.delete()

    return redirect('admin-panel-products', category)

def ProductDetails(request, product_id):
    admin_name = request.user.username
    product = Product.objects.get(pk=product_id)
    category = Category.objects.get(pk=product.category_id)
    specs = product.specifications.all()

    print("Product:", product.product_name)
    print("Category:", category.category_name)
    print("Specs:", specs)

    return render(request, 'ecommerce_platform/admin/product_detail.html', {'category': category.category_name,
                                                         'product': product,
                                                         'specs': specs,
                                                         'admin': admin_name})

def ProductAdd(request, category_name):
    admin_name = request.user.username
    if request.method == 'POST':
        productForm = ProductAddForm(request.POST, request.FILES)
        if productForm.is_valid():
            cd = productForm.cleaned_data

            category = Category.objects.get(category_name=category_name)
            product_obj = Product.objects.create(category=category, product_name=cd['product_nm'], description=cd['description'], price=cd['price'], image=cd['image'])
            product_obj.save()

            return redirect('admin-panel-products', category_name)
    else:
        data = {
            'category': category_name
        }
        productForm = ProductAddForm(initial=data)
    return render(request, 'ecommerce_platform/admin/actions/product_add.html', {'admin': admin_name,
                                                              'form': productForm})

def ProductSpecs(request, product_category, product_id):
    admin_name = request.user.username
    product = Product.objects.get(pk=product_id)
    SpecForm = formset_factory(ProductSpecsAddForm, extra=1)
    if request.method == "POST":
        productSpecForm = SpecForm(request.POST)

        if productSpecForm.is_valid():
            cnt = 0
            for prodSpec in productSpecForm:
                if cnt >= 1:
                    cd = prodSpec.cleaned_data

                    specs = ProductSpecifications.objects.create(product=product, spec_type=cd['spec_type'], spec_value=cd['spec_value'])
                    specs.save()
                cnt = cnt+1

            return redirect('admin-panel-product-detail', product.id)
    else:
        data = {
            'form-INITIAL_FORMS': '1',
            'form-TOTAL_FORMS': '1',
            'form-0-spec_type': 'spec',
            'form-0-spec_value': 'value',
        }
        productSpecForm = SpecForm(data)
    return render(request, 'ecommerce_platform/admin/actions/product_specs_add.html', {'formset': productSpecForm,
                                                                    'product': product,
                                                                    'admin': admin_name})

def CustomersCart(request):
    admin = request.user.username
    customers = Cart.objects.all()

    products = Product.objects.all()

    return render(request, 'ecommerce_platform/admin/customers_cart.html', {'customers': customers, 'products': products, 'admin': admin})

def DeliveryStatus(request):
    customer_id = request.POST.getlist("customer")
    customer_id = int(customer_id[0])

    cart_obj = Cart.objects.filter(pk=customer_id).first()
    cart_obj.shipment_status = "Delivered"
    cart_obj.save()

    return redirect('customers-cart')

def CustomersCartPDFPrint(request):
    # print_url = request.build_absolute_uri(reverse('customers-cart'))

    customers = Cart.objects.all()
    html = render_to_string('ecommerce_platform/pdf/customers_cart_pdf.html', {'customers': customers})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=customers_carts.pdf'
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/customers_cart_pdf.css')])
    return response