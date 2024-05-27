from django.urls import path

from .views import homepage,products, search

urlpatterns = [
    path("", homepage, name="home"),
    path('products/', products, name='products'),
    path('search/', search, name='search'),
        
]