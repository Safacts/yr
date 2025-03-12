from django.urls import path
from .views import homepage, products, search, upload, submit_product, product_list, password, search_products, all_products, order_button_click

urlpatterns = [
    path("", homepage, name="home"),
    path('products/', product_list, name='products'),
    path('search/', search, name='search'),
    path('submit_product/', submit_product, name='submit_product'),  # Ensure this pattern is correct and not duplicated
    path('upload/',upload, name='upload'),
    path('password/',password, name='password'),
    path('search-products/',search_products, name='search_products'),
    path('all-products/', all_products, name='all_products'),
    path('order-button-click/<int:product_id>/', order_button_click, name='order_button_click'),

    # path('product_list/', product_list, name='product_list')
]
