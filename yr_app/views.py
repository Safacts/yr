from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.conf import settings
from .models import PageView



def homepage(request):
    if settings.COUNT_PAGE_VIEWS:
        page_view, created = PageView.objects.get_or_create(pk=1)
        page_view.count += 1
        page_view.save()
        view_count = page_view.count
    else:
        view_count = "Development mode: View count not tracked."

    context = {'view_count': view_count}
    
    return render(request, 'yrcorporation.html', context)

def products(request):
    return render(request,"products.html")
