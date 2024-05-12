import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import EmailMessage
import weasyprint
from io import BytesIO
from django.template.loader import render_to_string
from .models import Cart, CartProducts
from ecommerce_platform.models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_payment_webhook(request):
    event = None
    try:
        event = stripe.Webhook.construct_event(
            request.body,
            request.META['HTTP_STRIPE_SIGNATURE'],
            settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event.type == 'checkout.session.completed':
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order = Cart.objects.get(pk=session.client_reference_id)
            except Cart.DoesNotExist:
                return HttpResponse(status=404)
            # mark order as paid
            order.payment_status = "paid"
            order.shipment_status = "In progress"
            order.save()

            # send email to user
            subject = f'Your cart invoice. {order.customer_id}'
            message = 'Invoice of your recent purchase'
            email = EmailMessage(subject, message, 'ecommerceShop@gmail.com', [order.email])

            # generate PDF
            products_cart = []
            products = []
            if order:
                products_cart = order.customer_cart.all().order_by('product')
                product_ids = [product.product for product in products_cart]
                products = Product.objects.filter(pk__in=product_ids)

            html = render_to_string('customer_logs/cart/pdf/cart_detail_pdf.html', {'cart': order, 'products_cart': products_cart, 'products': products,})
            out = BytesIO()
            # stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
            weasyprint.HTML(string=html).write_pdf(out)
            # stylesheets=stylesheets)
            # attach PDF file
            email.attach(f'order_{order.customer_id}.pdf',
            out.getvalue(),
            'application/pdf')
            # send e-mail
            email.send()


    return HttpResponse(status=200)