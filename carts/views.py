from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .models import Product, Variation, Cart, CartItem

# Create your views here.
from django.http import HttpResponse

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) # Get the product

    if current_user.is_authenticated:
        product_variation = []
        if 'size' in request.POST:  # Check if size is submitted in the form
            size_value = request.POST['size']
            try:
                # Retrieve the variation based on size
                variation = Variation.objects.get(variation_category__iexact='size', variation_value__iexact=size_value)
                product_variation.append(variation)
            except Variation.DoesNotExist:
                # Handle case where variation doesn't exist
                print("Variation does not exist for size:", size_value)
                pass

        print("Variations from form:", product_variation)

        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id_list = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id_list.append(item.id)

            if product_variation in ex_var_list:
                # Increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id_list[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

        return redirect('cart')

    else:  # If the user is not authenticated
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except Variation.DoesNotExist:
                    pass

        # Remaining part of the code for unauthenticated users

        return redirect('cart') 



def remove_cart(request, product_id, cart_item_id):

    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        sub_total = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            quantity += cart_item.quantity

            # Calculate the price based on variations
            price = cart_item.product.price
            for variation in cart_item.variations.all():
                if variation.variation_category == 'size':
                    if variation.variation_value == '30 ml':
                        price = cart_item.product.price_small
                    elif variation.variation_value == '50 ml':
                        price = cart_item.product.price_medium
                    elif variation.variation_value == '100 ml':
                        price = cart_item.product.price_large
            
            sub_total = cart_item.quantity * price
            cart_item.sub_total = sub_total  # Assign sub_total to cart_item.sub_total

        # Add this subtotal to the grand total
            grand_total += sub_total  
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'sub_total' : sub_total,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        sub_total = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            quantity += cart_item.quantity

            # Calculate the price based on variations
            price = cart_item.product.price
            for variation in cart_item.variations.all():
                if variation.variation_category == 'size':
                    if variation.variation_value == '30 ml':
                        price = cart_item.product.price_small
                    elif variation.variation_value == '50 ml':
                        price = cart_item.product.price_medium
                    elif variation.variation_value == '100 ml':
                        price = cart_item.product.price_large
            
            sub_total = cart_item.quantity * price
            cart_item.sub_total = sub_total  # Assign sub_total to cart_item.sub_total

        # Add this subtotal to the grand total
            grand_total += sub_total  
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'sub_total' : sub_total,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)
