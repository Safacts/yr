from django.urls import path
from .views import homepage, products, search, upload, submit_product

urlpatterns = [
    path("", homepage, name="home"),
    path('products/', products, name='products'),
    path('search/', search, name='search'),
    path('submit_product/', submit_product, name='submit_product'),  # Ensure this pattern is correct and not duplicated
    path('upload/',upload, name='upload'),
]
