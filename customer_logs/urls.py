from django.urls import path
from . import views
from . import webhooks

app_name = "visitors_view"

urlpatterns = [
    path("search/", views.Search, name="search-product"),
    path("product-view/<int:category_id>", views.ProductView, name="products-view"),
    path("product-detail/<int:product_id>", views.ProductDetail, name='product-detail-view'),

    path('cart-form/<product_name>', views.CustomerDetailForm, name='cart-form'),

    path('cart/<customer_name>', views.CartDetail, name='cart-detail'),

    path('remove-cart/<int:product_ID>', views.RemoveCart, name='remove-cart'),

    path('update-cart/', views.UpdateCart, name='cart-update'),

    path('process/', views.Checkout, name='checkout-process'),

    path('webhook/', webhooks.stripe_payment_webhook, name='stripe-webhook'),

    path('completed/', views.CheckoutSuccess, name='checkout-success'),
    path('canceled/', views.CheckoutCancel, name='checkout-cancel'),


]