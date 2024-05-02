from django.urls import path
from . import views
urlpatterns = [
    path('', views.homeView, name='home'),
    # admin panel url

    path('admin/create-category/', views.CreateCategory, name='category-create'),
    path('admin/<admin_name>/', views.Admin, name='admin-panel'),
    path('admin/products/<category_name>/', views.Products, name='admin-panel-products'),
    path('admin/products/<int:product_id>', views.ProductDetails, name='admin-panel-product-detail'),
    path('admin/products/add-product/<category_name>/', views.ProductAdd, name='admin-panel-product-add'),
    path('admin/product-category/product/<product_category>/<int:product_id>', views.ProductSpecs, name='admin-panel-product-specs'),
    # path('admin/product-category/product/<product_category>/<int:product_id>', views.ProductSpecsAdd, name='admin-panel-product-specs-add'),

    path('signup/', views.RegistrationView, name='signup'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
]
