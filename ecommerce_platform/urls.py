from django.urls import path
from . import views
urlpatterns = [
    path('', views.homeView, name='home'),
    # admin panel url

    #
    path('admin/show-models/', views.ShowModels, name="show-models"),
    path('admin/Category/', views.CategoryModel, name="category"),
    path('admin/Cart/', views.CartModel, name="cart"),
    path('admin/DeleteCart/<int:cart_id>', views.DeleteCart, name='delete-cart'),
    path('admin/DeleteCart/', views.DeleteCart, name='delete-cart'),
    #

    path('admin/customers-carts/', views.CustomersCart, name="customers-cart"),
    path('admin/customers-carts/deliver-status/', views.DeliveryStatus, name="customer-cart-delivery-status"),
    path('admin/print/customers-cart/.pdf', views.CustomersCartPDFPrint, name="customer-cart-pdf-print"),

    path('admin/create-category/', views.CreateCategory, name='category-create'),
    path('admin/<admin_name>/', views.Admin, name='admin-panel'),
    path('admin/products/<category_name>/', views.Products, name='admin-panel-products'),
    path('admin/products/<int:product_id>', views.ProductDetails, name='admin-panel-product-detail'),
    path('admin/products/add-product/<category_name>/', views.ProductAdd, name='admin-panel-product-add'),
    path('admin/product-category/product/<product_category>/<int:product_id>', views.ProductSpecs, name='admin-panel-product-specs'),
    path('admin/delete-category/<int:category_id>/', views.DeleteCategory, name="delete-category"),
    path('admin/delete-product/<int:product_id>', views.DeleteProduct, name='delete-product'),

    path('signup/', views.RegistrationView, name='signup'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('accounts/profile/', views.GoogleAuthUser, name="google-auth"),
]
