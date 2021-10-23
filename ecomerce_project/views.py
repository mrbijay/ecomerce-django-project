from django.core.paginator import Paginator
from django.shortcuts import render
from store.models import *



def home(request):
    products =Product.objects.all().filter(is_available=True).order_by('-id')
    paginator=Paginator(products,8)
    page=request.GET.get('page')
    paged_products=paginator.get_page(page)

    context = {
        'products' : paged_products,
    }
    


    return render(request, 'home.html',context)

def signin(request):
    return render(request, 'signin.html')
    
def register(request):
    return render(request, 'register.html')

def cart(request):
    return render(request, 'cart.html')
    