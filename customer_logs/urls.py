from django.urls import path
from . import views

app_name = "visitors_view"

urlpatterns = [
    path("product-view/<int:category_id>", views.ProductView, name="products-view"),
    path("product-detail/<int:product_id>", views.ProductDetail, name='product-detail-view'),

    path('cart-form/<product_name>', views.CustomerDetailForm, name='cart-form'),

    path('cart/<customer_name>', views.CartDetail, name='cart-detail'),

    path('remove-cart/<int:product_ID>', views.RemoveCart, name='remove-cart'),

    path('update-cart/', views.UpdateCart, name='cart-update'),

    # path('checkout/', views.Checkout, name='checkout'),

    path('success/', views.CheckoutSuccess, name='checkout-success'),
    path('canceled/', views.CheckoutCancel, name='checkout-cancel'),
]