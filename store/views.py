from django.shortcuts import render, get_object_or_404
from .models import Product
from django.db.models import Q
from categery.models import Catagory
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


# Create your views here.
def store(request, catagory_slug=None):

    catagories = None
    products = None

    if catagory_slug != None:
        catagories = get_object_or_404(Catagory, slug=catagory_slug)
        products = Product.objects.filter(catagory=catagories, is_available=True)
        peginator = Paginator(products, 12)
        page = request.GET.get('page')
        paged_products = peginator.get_page(page)
        pr_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        peginator = Paginator(products, 12)
        page = request.GET.get('page')
        paged_products = peginator.get_page(page)
        pr_count = Product.objects.filter(is_available=True).count()
    dict = {
        'products': paged_products,
        'pr_count': pr_count,
    }
    return render(request, 'store.html', dict)



def pr_detail(request, catagory_slug, pr_slug):
    try:
        single_pr = Product.objects.get(catagory__slug=catagory_slug, slug=pr_slug)
    except Exception as e:
        raise e
    
    dict = {
        'single_pr': single_pr,
    }
    return render(request, 'pr_details.html', dict)



def search(request):
    product = None
    if 'keyword' in request.GET:
        k_word = request.GET['keyword']
        if k_word:
            product = Product.objects.filter(Q (description__icontains=k_word) | Q (pr_name__icontains=k_word))
            pr_count = product.count()
    dict = {
        'products': product,
        'pr_count': pr_count,
    }
    return render(request, 'store.html', dict)