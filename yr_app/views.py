from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from .models import PageView , Product



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



def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query).values('name', 'description', 'price', 'image_url')
    return JsonResponse(list(products), safe=False)



def products(request):
    return render(request,"products.html")

def upload(request):
    return render(request, "upload.html")