from django.shortcuts import get_object_or_404, redirect, render
from carts.models import Cart, CartItem
from django.http import HttpResponse, request
from store.models import Product, Variation

# Create your views here.

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

# add cart item
def add_cart(request, product_id):
    product=Product.objects.get(id=product_id)  # get the product
    product_variation=[]
    if request.method == 'POST':
        for item in request.POST:
            key=item
            value=request.POST[key]
            
            try:
                variation=Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass

    
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))   #get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id= _cart_id(request)

        )
    cart.save()

    is_cart_item_exists = CartItem.objects.filter(product=product,cart=cart)

    if is_cart_item_exists:
        cart_item=CartItem.objects.filter(product=product,cart=cart)
        #existing_variation  from data base
        #current_variation   product_variation
        #item id             from data base
        ex_var_list=[]
        id=[]
        for item in cart_item:
            existing_variation=item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
        print(ex_var_list)

        if product_variation in ex_var_list:
            # increase the cart item quantity
            index=ex_var_list.index(product_variation)
            item_id=id[index]
            item=CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()

        else:
            item=CartItem.objects.create(product=product,quantity=1,cart=cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
                item.save()
    else:
        cart_item=CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart, 
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
            cart_item.save()
    return redirect('cart')

# decrease cart item
def remove_cart(request, product_id,cart_item_id):
    cart= Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product, id=product_id)
    try:
        cart_item=CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    
    return redirect('cart')
    
# for remove cart item
def remove_cart_item(request , product_id,cart_item_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product, id= product_id)
    cart_item=CartItem.objects.get(product=product, cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')



def cart(request, total=0, quantity=0, cart_item=None):
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except Cart.DoesNotExist:
        pass #just ignore

    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total': grand_total,
    }
    return render(request, 'cart.html', context)
    