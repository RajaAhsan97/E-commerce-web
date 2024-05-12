
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import request, JsonResponse, HttpResponse
from django.db.models import Q
from .models import Customer, Cart, CartProducts
from ecommerce_platform.models import Category, Product, ProductSpecifications
from .forms import CartForm
import uuid
from django.conf import settings
import stripe
from decimal import Decimal

# Create your views here.

def Search(request):
    search_category = request.GET.get('search')
    category = Category.objects.filter(Q(category_name__icontains=search_category)).first()
    if category == None:
        # search_error = "No result for your search"
        return redirect('home')
    else:
        return redirect('visitors_view:products-view', category.id)

def ProductView(request, category_id):
    category = Category.objects.get(pk=category_id)
    products = category.category_product.all()

    admin_name = request.user.username

    return render(request, "customer_logs/product_view.html", {'admin': admin_name,
                                                 'products': products,
                                                 'category': category.category_name})

def ProductDetail(request, product_id):
    product = Product.objects.get(pk=product_id)
    product_specs = product.specifications.all()
    print(product_specs)

    admin_name = request.user.username

    return render(request, 'customer_logs/product_detail.html', {'admin': admin_name,
                                                   'product': product,
                                                   'specs': product_specs})

def CustomerDetailForm(request, product_name):
    customer_name = request.user.username
    customer_exist_in_cart = Cart.objects.filter(name=customer_name)

    if customer_exist_in_cart:
        product = Product.objects.get(product_name=product_name)
        cart_product = CartProducts.objects.create(cart=customer_exist_in_cart.first(), product=product.id, unit_price=product.price, total_price=product.price)
        cart_product.save()
        return redirect('visitors_view:cart-detail', customer_name)
    else:
        if request.method == 'POST':
            cartForm = CartForm(request.POST)
            if cartForm.is_valid():
                cd = cartForm.cleaned_data
                print("form data valid")

                customer_cart_id = str(uuid.uuid4())
                cart = Cart.objects.create(name=cd['name'], email=cd['email'], address=cd['address'], phone_no=cd['contact'], customer_id=customer_cart_id)
                cart.save()

                #
                product = Product.objects.get(product_name=product_name)
                cart = Cart.objects.get(name=cd['name'])
                cart_product = CartProducts.objects.create(cart=cart, product=product.id, unit_price=product.price, total_price=product.price)
                cart_product.save()
                #

                return redirect('visitors_view:cart-detail', cd['name'])
        else:
            customer = Customer.objects.filter(customer_name=customer_name).first()

            if customer:
                data = {
                    'name': customer.customer_name,
                    'email': customer.email,
                }
                cartForm = CartForm(initial=data)
            else:
                customer_regstr_msg = "please sign-up to purchase products..."
                return render(request, 'customer_logs/cart/cart_form.html', {'msg': customer_regstr_msg})

        return render(request, 'customer_logs/cart/cart_form.html', {'form': cartForm})


def CartDetail(request, customer_name):
    print(customer_name)

    cart = Cart.objects.filter(name=customer_name).first()

    products_cart = []
    products = []
    if cart:
        products_cart = cart.customer_cart.all().order_by('product')
        product_ids = [product.product for product in products_cart]
        products = Product.objects.filter(pk__in=product_ids)

    return render(request, "customer_logs/cart/cart_detail.html", {'cart': cart,
                                                     'products_cart': products_cart,
                                                     'products': products,
                                                     'admin': customer_name})

def RemoveCart(request, product_ID):
    customer_name = request.user.username
    print(customer_name)
    customer_id = Cart.objects.get(name=customer_name)
    CartProducts.objects.filter(cart_id=customer_id, product=product_ID).first().delete()
    # CartProducts.objects.all().delete()
    return redirect('visitors_view:cart-detail', customer_name)

def UpdateCart(request):
    customer_name = request.user.username
    if request.method == "POST":
        prod = request.POST.get("product")
        qty = request.POST.get("quantity")
        total_price = request.POST.get("total_price")
        print("product: ", prod, "QTY: ", qty, "------", "totol Price: ", total_price)

        customer = Cart.objects.get(name=customer_name)

        product_id = Product.objects.get(product_name=prod).id
        print("product id: ", product_id)

        update_cart_obj = CartProducts.objects.get(product=product_id, cart_id=customer)
        update_cart_obj.quantity = qty
        update_cart_obj.total_price = total_price
        update_cart_obj.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


stripe.api_key = settings.STRIPE_SECRET_KEY

def Checkout(request):
    customer = request.user.username

    customer_id = Cart.objects.get(name=customer).id

    cart_items = CartProducts.objects.filter(cart_id=customer_id)
    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse("visitors_view:checkout-success"))
        cancel_url = request.build_absolute_uri(reverse("visitors_view:checkout-cancel"))
        session = {
            'mode': 'payment',
            'success_url': success_url,
            'cancel_url': cancel_url,
            'client_reference_id': str(customer_id),
            'line_items': []
        }

        for item in cart_items:
            product_name = Product.objects.get(id=item.product).product_name
            session['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.unit_price * Decimal('100')),
                    'currency': 'usd',
                    'product_data': {
                        'name': product_name
                    },
                },
                'quantity': item.quantity,
            })
        session = stripe.checkout.Session.create(**session)
        return redirect(session.url, code=303)
    return render(request, 'customer_logs/payment/payment_process.html', {'items': cart_items})

def CheckoutSuccess(request):
    customer_name = request.user.username

    # cart_obj = Cart.objects.get(name=customer_name)
    # cart_obj.payment_status = "paid"
    # cart_obj.shipment_status = "In progress"
    # cart_obj.save()
    return render(request, 'customer_logs/payment/payment_completed.html', {'customer': customer_name})

def CheckoutCancel(request):

    return render(request, 'customer_logs/payment/payment_canceled.html')