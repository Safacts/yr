from django.urls import path
from .views import homepage, products, search, upload, submit_product, product_list, password

urlpatterns = [
    path("", homepage, name="home"),
    path('products/', product_list, name='products'),
    path('search/', search, name='search'),
    path('submit_product/', submit_product, name='submit_product'),  # Ensure this pattern is correct and not duplicated
    path('upload/',upload, name='upload'),
    path('password/',password, name='password'),

    # path('product_list/', product_list, name='product_list')
]
