from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import PageView



def homepage(request):
    page_view, created = PageView.objects.get_or_create(pk=1)
    page_view.count += 1
    page_view.save()

    context = {'view_count': page_view.count}
    
    # Debugging
    print("PageView Count: ", page_view.count)
    
    return render(request, 'yrcorporation.html', context)

def products(request):
    return render(request,"products.html")
