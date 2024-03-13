from django.urls import path

from .views import homepage,products

urlpatterns = [
    path("", homepage, name="home"),
    path('products/', products, name='products'),
        
]