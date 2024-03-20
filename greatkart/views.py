from django.shortcuts import render
from store.models import Product, ReviewRating
from category.models import Banner

def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('created_date')
    banners = Banner.objects.all()
    # Get the reviews
    reviews = None
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'products': products,
        'reviews': reviews,
        'banners': banners,
    }
    return render(request, 'home.html', context)

def faqs(request):
    return render(request, 'faqs.html')

def aboutus(request):
    return render(request, 'about-us.html')

def contactus(request):
    return render(request, 'contact-us.html')