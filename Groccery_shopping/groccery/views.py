from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.views import View
from django.db.models import Q
from django.http import JsonResponse

from .models import Product,Category,Customer,Cart, Order, OrderItem

def home(request):
    products = None
    total_item=0
    if request.session.has_key('phone'):
        phone=request.session['phone']
        category = Category.get_all_categories()
        customer = Customer.objects.filter(phone=phone)
        total_item= len(Cart.objects.filter(phone=phone))
        for c in customer:
            name = c.name
            categoryID = request.GET.get('category')
            if categoryID:
                products= Product.get_all_products_by_category_id(categoryID)
            else:
                products= Product.objects.all()
            pro ={
                'products':products,
                'category':category,
                'name':name,
                'total_item':total_item
            }
            return render(request, 'home.html',pro)
    else:
        return redirect('login')

        
class signup(View):
    def get(self,request):
        return render(request,'signup.html')
    def post(self, request):
        postData = request.POST
        name = postData.get('name')
        phone = postData.get('phone')
        error_message= None
        value ={
            'name':name,
            'phone':phone
        }
        customer = Customer(name = name, phone= phone)

        if(not name):
            error_message="Name is required"
        elif not phone:
            error_message="Phone number is required"
        elif customer.doesExist():
            error_message="This number has already been taken"
        elif len(phone)<10:
            error_message="Please enter a valid number"
        
        if not error_message:
            messages.success(request,'Congratulations! you have successfully signed up')
            customer.register()
            return redirect('signup')
        else:
            data={
                'error':error_message,
                'value':value
            }
            return render(request,'signup.html',data)

class login(View):
    def get(self,request):
        return render(request,'login.html')
    
    def post(self, request):
        phone = request.POST.get('phone')
        error_message = None
        value ={
            'phone':phone
        }
        customer =  Customer.objects.filter(phone=request.POST['phone'])
        if customer:
            request.session['phone']=phone
            return redirect('home')
        else:
            error_message="The number is invalid"
            data={
                'error':error_message,
                'value':value
            }
        
        return render(request,'login.html',data)
    
def productdetail(request, pk):
    total_item = 0
    product = Product.objects.get(pk=pk)
    item_already_exist = False
    if request.session.has_key('phone'):
        phone = request.session['phone']
        total_item= len(Cart.objects.filter(phone=phone))
        item_already_exist= Cart.objects.filter(Q(product=product.id) & Q(phone=phone)).exists()
        data={
            'product':product,
            'item_already_exist':item_already_exist,
            'total_item':total_item
        }
        return render(request,'productdetail.html',data)


def logout(request):
    if request.session.has_key('phone'):
        del request.session['phone']
        return redirect('login')
    else:
        return redirect('login')
    

def add_to_cart(request):
    phone = request.session.get('phone')
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)

    Cart.objects.create(
        phone=phone,
        product=product,
        image=product.image,
        price=product.price
    )
    return redirect(f"/productdetail/{product_id}")


def showcart(request):
    total_item = 0
    if request.session.has_key('phone'):
         phone = request.session['phone']
         total_item = len(Cart.objects.filter(phone=phone))
         customer= Customer.objects.filter(phone=phone)
         for c in customer:
             name= c.name
             cart= Cart.objects.filter(phone= phone)
             data={
                 'name':name,
                 'total_item':total_item,
                 'cart':cart
             }
             if cart:
                  return render(request,'showcart.html',data)
             else:
                 return render(request,'empty_cart.html',data)
        

def plus_cart(request):
    if request.session.has_key('phone'):
        phone = request.session["phone"]
        product_id = request.GET.get('prod_id')  # use get() to handle missing prod_id gracefully

        try:
            cart = Cart.objects.get(Q(product_id=product_id) & Q(phone=phone))
            cart.quantity += 1
            cart.save()
            quantity = cart.quantity
            data = {
                'quantity': quantity,
                'price': cart.price,  # include price if needed
            }
        except Cart.DoesNotExist:
            # Handle the case where the cart does not exist
            data = {
                'error': 'Cart item does not exist'
            }

        return JsonResponse(data)

    else:
        # Handle the case where the phone is not in the session
        data = {
            'error': 'User is not authenticated'
        }
        return JsonResponse(data)
def minus_cart(request):
    if request.session.has_key('phone'):
        phone = request.session["phone"]
        product_id = request.GET.get('prod_id')

        try:
            cart = Cart.objects.get(Q(product=product_id) & Q(phone=phone))
            if cart.quantity > 1:
                cart.quantity -= 1
                cart.save()
            else:
                # If quantity is 1, you may want to delete the item from the cart
                # cart.delete() 
                cart.quantity = 0  # Optionally, set it to 0 instead of deleting

            data = {
                'quantity': cart.quantity,
            }
        except Cart.DoesNotExist:
            data = {
                'error': 'Item not found in the cart.'
            }

        return JsonResponse(data)
def remove_cart(request):
    if request.session.has_key('phone'):
        phone = request.session["phone"]
        product_id = request.GET.get('prod_id')  # use get() to handle missing prod_id gracefully

        try:
            cart = Cart.objects.get(Q(product_id=product_id) & Q(phone=phone))
            cart.delete()
            data = {
                'success': 'Cart item removed successfully'
            }
        except Cart.DoesNotExist:
            # Handle the case where the cart item does not exist
            data = {
                'error': 'Cart item does not exist'
            }

        return JsonResponse(data)

    else:
        # Handle the case where the phone is not in the session
        data = {
            'error': 'User is not authenticated'
        }
        return JsonResponse(data)


def checkout(request):
    if request.session.has_key('phone'):
        phone = request.session['phone']
        cart_items = Cart.objects.filter(phone=phone)
        
        if cart_items.exists():
            total_amount = 0
            cart_details = []

            for item in cart_items:
                item_total_price = item.price * item.quantity
                total_amount += item_total_price
                cart_details.append({
                    'product_name': item.product.name,
                    'quantity': item.quantity,
                    'price': item.price,
                    'total_price': item_total_price
                })

            data = {
                'cart_items': cart_details,
                'total_amount': total_amount
            }
            
            return render(request, 'checkout.html', data)
        
        messages.info(request, "Your cart is empty. Please add items to your cart before checking out.")
        return redirect('showcart')
    
    return redirect('login')




def process_checkout(request):
    if request.method == 'POST':
        if request.session.has_key('phone'):
            phone = request.session['phone']
            customer = Customer.objects.get(phone=phone)
            cart_items = Cart.objects.filter(phone=phone)

            if cart_items.exists():
                address = request.POST.get('address')
                payment_method = request.POST.get('payment')

                # Create Order
                order = Order.objects.create(
                    customer=customer,
                    total_amount=0,  # This will be updated later
                    payment_method=payment_method,
                    address=address
                )

                total_amount = 0

                # Create Order Items
                for item in cart_items:
                    item_total_price = item.price * item.quantity
                    total_amount += item_total_price
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.price,
                        total_price=item_total_price
                    )

                # Update total amount in the order
                order.total_amount = total_amount
                order.save()

                # Clear the cart after the order is placed
                cart_items.delete()

                # Redirect to the invoice page
                return redirect('invoice', order_id=order.id)
            
            messages.info(request, "Your cart is empty. Please add items to your cart before checking out.")
            return redirect('showcart')

    return redirect('checkout')
def invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'invoice.html', {'order': order})


def search(request):
    total_item = 0
    name = ''
    
    if request.session.has_key('phone'):
        phone = request.session["phone"]
        query = request.GET.get('query', '').strip()

        if query:
            search_results = Product.objects.filter(name__icontains=query)
        else:
            search_results = Product.objects.none()  

        categories = Category.get_all_categories()
        total_item = Cart.objects.filter(phone=phone).count()

        customer = Customer.objects.filter(phone=phone).first()
        if customer:
            name = customer.name

        data = {
            'name': name,
            'totalitem': total_item,
            'query': query,
            'search': search_results,
            'category': categories,
        }

        return render(request, 'search.html', data)
    else:
        return redirect('login')




        
          
            

   
        


    



        

   

