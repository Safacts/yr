from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from .models import PageView , Product
from supabase import create_client, Client
import os

# new imports for file uploading
import re
import urllib.parse


# Initialize Supabase client
SUPABASE_URL = os.environ.get("SUPABASE_URL")
# SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE_SERVICE_KEY = os.environ.get('SUPABASE_SERVICE_KEY')  # Set this in your environment
supabase: Client = create_client(SUPABASE_URL,  SUPABASE_SERVICE_KEY)

PASSWORD = os.environ.get("PASSWORD")

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



def sanitize_filename(filename):
    """
    Replace spaces with underscores and remove any special characters
    except periods, underscores, and hyphens.
    """
    filename = re.sub(r'[^\w\.\-]', '_', filename)
    return filename

def submit_product(request):
    if request.method == "POST":
        # Retrieve form data
        name = request.POST.get("productName", "").strip()
        description = request.POST.get("productDescription", "").strip()
        price = float(request.POST.get("productPrice", "0").strip())  # Convert to float
        image = request.FILES.get("productImage")

        if image:
            # Sanitize the product name and original filename
            sanitized_product_name = sanitize_filename(name.lower())
            sanitized_file_name = sanitize_filename(image.name)

            # Combine product name with the original file name
            unique_file_name = f"{sanitized_product_name}_{sanitized_file_name}"

            # URL-encode the unique file name
            unique_file_name_encoded = urllib.parse.quote(unique_file_name)

            # Define the path in the Supabase bucket
            image_path = f"images/{unique_file_name_encoded}"

            try:
                # Read the content of the uploaded image
                file_content = image.read()
                content_type = image.content_type

                # Upload the image content to Supabase
                response = supabase.storage.from_("images").upload(
                    image_path, file_content, {
                        'content-type': content_type
                    }
                )

                # Check for errors in the response
                response_data = response.json()
                if response_data.get('error'):
                    print(f"Error uploading file: {response_data['error']}")
                    return JsonResponse({'success': False, 'error': response_data['error']})

                # Construct the public URL of the uploaded image
                image_url = f"{SUPABASE_URL}/storage/v1/object/public/images/{image_path}"

            except Exception as e:
                # Handle any exceptions during the upload process
                print(f"Exception during file upload: {e}")
                return JsonResponse({'success': False, 'error': str(e)})
        else:
            image_url = None

        # Create the product in the database using Supabase
        product_data = {
            'name': name,
            'description': description,
            'price': price,
            'image_url': image_url
        }

        # Insert the product into the Supabase table
        response = supabase.table('yr_app_product').insert(product_data).execute()

        # Check for errors in the response
        if isinstance(response.data, list) and len(response.data) > 0:
            # If the response is a list and contains data, the insert was successful
            return JsonResponse({"message": "Product submitted successfully!"})
        elif isinstance(response.data, dict) and response.data.get('error'):
            # If the response is a dictionary and contains an error
            print("Error inserting product:", response.data['error'])
            return JsonResponse({'success': False, 'error': response.data['error']})
        else:
            # Handle unexpected response structure
            print("Unexpected response structure:", response.data)
            return JsonResponse({'success': False, 'error': 'Unknown error occurred'})

    return render(request, "upload.html")


def product_list(request):
    try:
        # Fetch all products from Supabase
        response = supabase.table('yr_app_product').select("*").execute()

        print("Raw response from Supabase:", response)  # Debugging

        if hasattr(response, 'data') and isinstance(response.data, list):
            products = response.data  # Extract products
        else:
            print("Unexpected response structure:", response)
            products = []  # Default to empty list

    except Exception as e:
        print("Error fetching products:", e)
        products = []

    return render(request, "products.html", {"products": products})

def password(request):
    return render(request, "password.html")

