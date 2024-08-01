from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.views import View
from django.db.models import Q
from django.http import JsonResponse

from .models import Product,Category,Customer,Cart

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
                 pass
        

def plus_cart(request):
    if request.session.has_key('phone'):
        phone=request.session["phone"]
        product_id=request.GET['prod_id']
        cart=Cart.objects.get(Q(product=product_id) & Q(phone=phone))
        cart.quantity+=1
        cart.save()
        quanity=cart.quantity
        data={
            'quantity':quanity
        }
        return JsonResponse(data)

        
          
            

   
        


    



        

   

