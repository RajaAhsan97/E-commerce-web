import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Cart

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

    return HttpResponse(status=200)