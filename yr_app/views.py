from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from .models import PageView , Product
from supabase import create_client, Client
import os

# Initialize Supabase client
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


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

# def upload(request):
#     return render(request, "upload.html")


def upload(request):
    if request.method == "POST":
        name = request.POST.get("productName")
        description = request.POST.get("productDescription")
        price = request.POST.get("productPrice")
        image = request.FILES.get("productImage")

        if image:
            image_path = f"images/{image.name}"
            supabase.storage.from_("images").upload(image_path, image.file)

            # Get public URL of uploaded image
            image_url = supabase.storage.from_("images").get_public_url(image_path)
        else:
            image_url = None

        product = Product.objects.create(
            name=name, description=description, price=price, image_url=image_url
        )
        return JsonResponse({"message": "Product submitted successfully!"})

    return render(request, "upload.html")
