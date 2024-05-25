from django.shortcuts import render,redirect
from django.http import JsonResponse
from .forms import registrationform,cprofile,ReviewFrom,CuponcodeFrom
from django.views import View
from django.contrib import messages
from .models import customers ,hero,Product,Products,Customer_Reivew,Cart,Customer_Contract_From,OrderPlaced,onlyOne_Special_Product,Reviews,Cupon
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# Create your views here.
class homeView(View):
  def get(self,request):
    total_item=0
    if request.user.is_authenticated:
       total_item=len(Cart.objects.filter(user=request.user))
        
    cetagory=request.GET.get('cetagory')
    print(cetagory)
    heros=hero.objects.all()
    vagitable=Product.objects.filter(item='vegetables')
    fru=Product.objects.filter(item='fruits')
    brad=Product.objects.filter(item='bread')
    meat=Product.objects.filter(item='meat')
    p=Product.objects.all()[:8]
    pa=Product.objects.all()
    s=Product.objects.all()[8:14]
    re=Customer_Reivew.objects.all()
    on=onlyOne_Special_Product.objects.all()
    if cetagory :
        p=Product.objects.filter(item=cetagory)
        print(p)


    return render(request, 'home.html',{"hero":heros,'vg':vagitable,'fr':fru,'br':brad,'me':meat,'p':p,'r':re,'s':s,'pa':pa,'on':on,'total_item':total_item})

def shop(request):
    total_item=0
    if request.user.is_authenticated:
        total_item=len(Cart.objects.filter(user=request.user))
    p=Product.objects.all()
    fe=Product.objects.all()[9:15]
    
    paginator=Paginator(p,9)
    page_number=request.GET.get('page')
    datafinal=paginator.get_page(page_number)
   
    return render(request,'shop.html',{'p':datafinal,'fe':fe,'total_item':total_item})
@method_decorator(login_required,name='dispatch')
class shop_detailView(View):
    def get(self, request, pk):
        total_item=0
        if request.user.is_authenticated:
            total_item=len(Cart.objects.filter(user=request.user))
            
            sd = Product.objects.get(pk=pk)
            reviews=Reviews.objects.filter(product=sd)
            comment_from=ReviewFrom()
            pa = Product.objects.filter(item=sd.item).exclude(pk=pk)
            fe = Product.objects.filter(item=sd.item)[:6]
            quantity = 1
            try:
                cart = Cart.objects.get(Q(product=sd) & Q(user=request.user))
                quantity = cart.quantity
            except Cart.DoesNotExist:
                quantity = 1
            return render(request, 'shop-detail.html', {'sd': sd, 'pa': pa, 'quantity': quantity, 'fe': fe,'r':reviews,'cf':comment_from,'total_item':total_item})
        else:
            return redirect("/login")

    def post(self, request, pk):
        if request.user.is_authenticated:
            product = Product.objects.get(pk=pk)
            comment_form = ReviewFrom(request.POST)
            
            if comment_form.is_valid():
                new_review = comment_form.save(commit=False)
                new_review.product = product
                new_review.user = request.user
                new_review.save()  # Save the review
                return redirect('shop-detail', pk=pk)
            else:
                
                print("Form is invalid:", comment_form.errors)
                return redirect('home')  
            
        else:
            return redirect('/login/')
         
def vegetable(request):
    vg=Product.objects.filter(item='vegetables')
    return render(request,'vegetable.html',{'vg':vg})

def meats(request):
    me=Product.objects.filter(item='meat')
    return render(request,'mets.html',{'m':me})

def Breads(request):
    br=Product.objects.filter(item='bread')
    return render(request,'bread.html',{'br':br})

def fruit(request):
    fru=Product.objects.filter(item='fruits')
    return render (request,'fruit.html',{"ft":fru})

def plus_cart(request):
    if request.method == 'GET':
        cart_id = request.GET['cart_id']
        cart = Cart.objects.get(Q(id=cart_id) & Q(user=request.user))
        cart.quantity += 1
        cart.save()
        line_total = cart.quantity * cart.product.price
        carts = Cart.objects.filter(user=request.user)
        cart_total = 0
        for i in carts:
            cart_total = cart_total + i.line_total()

        print(cart_total)
        return JsonResponse({"status":"success", "quantity": cart.quantity,"line_total":line_total,"cart_total":cart_total})

def minas_cart(request):
    if request.method == 'GET':
        cart_id = request.GET['cart_id']
        cart = Cart.objects.get(Q(id=cart_id) & Q(user=request.user))
        if cart.quantity <= 1:
            cart.quantity = 1
        else:
            cart.quantity -= 1
        cart.save()
        line_total = cart.quantity * cart.product.price
        carts = Cart.objects.filter(user=request.user)
        cart_total = 0
        for i in carts:
            cart_total = cart_total + i.line_total()
      
        return JsonResponse({"status":"success", "quantity": cart.quantity,"line_total":line_total,"cart_total":cart_total})



@login_required
def cart(request):
    
    user = request.user
    product_id = request.GET.get('prod_id')
    product_quantity = request.GET.get('product_quantity')
    product = Product.objects.get(id=product_id)
    try:
        cart_item = Cart.objects.get(user=user, product=product)
        quantity = cart_item.quantity
        cart_item.quantity = product_quantity
        cart_item.save()
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user,product=product,quantity=product_quantity)
        cart.save()
    return redirect('/cart')

def delete_cart(request,id):
    cart = Cart.objects.get(id=id)
    cart.delete()
    return redirect('/cart')


def chackout(request):
    if request.user.is_authenticated:
        user=request.user
        cart_item=Cart.objects.filter(user=user)
        amount=0.0
        shiping_amount=0.50
        total_amount=0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for p in cart_product:
                temamount=(p.quantity*p.product.price)
                amount=temamount+amount
                totalammount=amount+shiping_amount
            
            cuponform=CuponcodeFrom(request.POST)
            if cuponform.is_valid():
                current_time=timezone.now()
                code=cuponform.cleaned_data.get('code')
                cupon_obj=Cupon.objects.get(code=code)
                if cupon_obj.valid_to >= current_time and cupon_obj.active :
                   get_discaunt=(cupon_obj.discaunt/100)*totalammount
                   total_price_dis=totalammount-get_discaunt
                   request.session['discaount_total']=total_price_dis
                   request.session['copon_code']=code
                   
                   return redirect('cart')
                
                
            
            total_price_dis=request.session.get('discaount_total')
            cupon_code=request.session.get('cupon_code')
            print(Cart.line_total)   
            return render(request,'chackout.html',{'temamount':temamount,
                 'amount':amount,
                 'totalammount':totalammount,
                 'cart':cart_item,
                 'shiping_amount':shiping_amount,
                 'total_price_dis':total_price_dis,
                 'copon_code':cupon_code
                 })
        else:
            
            return render(request,'404.html')
    

def testimonial(request):
    re=Customer_Reivew.objects.all()
    return render(request,'testimonial.html',{'r':re})

def error(request):
    return render(request,'404.html')

def contract(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        data = {
            'name': name,
            'email': email,
            'message': message
        }
        email_message = '''
        From: {}
        Name:{}
        About: {}
        
        

        
        '''.format( data['email'],data['name'],data['message'],)

        send_mail('New message received by Bangla Bazar', email_message, '', ['harun708280@gmail.com'])
        
        en=Customer_Contract_From(name=name,email=email,message=message)
        
        
        en.save()
        messages.success(request,'Sucessfully Your SMS Sent')
        
    return render(request, 'contact.html')
def payment(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        company_name=request.POST.get('company_name')
        address=request.POST.get('address')
        town=request.POST.get('town')
        upozila=request.POST.get('upozila')
        postcode=request.POST.get('postcode')
        mobile=request.POST.get('mobile')
        email=request.POST.get('email')
        
    user=request.user
    cart=Cart.objects.filter(user=user)
    data = {
        'user':user,
        'name':name,
        'c_n':company_name,
        'add':address,
        'town':town,
        'cart':cart
    }
    email_message='''
    user:{}
    name:{}
    company name:{}
    address:{}
    town:{}
    product:{}
    '''.format(data['user'],data['name'],data['c_n'],data['add'],data['town'],data['cart'])
    send_mail('BanglaBazar Order Now',email_message,'',['harun708280@gmail.com'])
    for c in cart:
        OrderPlaced(user=user,name=name,company_name=company_name,address=address,town=town,upozila=upozila,postcode=postcode,mobile=mobile,email=email,product=c.product,quantity=c.quantity,).save()
        c.delete()
    
    return redirect('home')

def login(request):
    return render(request,'login.html')

class registrationView(View):
 def get(self,request):
   form=registrationform()
   return render(request,'registration.html',{'form':form})
 def post(self,request):
     form=registrationform(request.POST)
     if form.is_valid():
      form.save()
      messages.success(request,'Succesfully Registration Done')
     return render(request,'registration.html',{'form':form})

class cprofileView(View):
 def get(self,request):
  form=cprofile()
  return render(request,'profile.html',{'form':form})
 
 def post(self,request):
    form=cprofile(request.POST)
    if form.is_valid():
       user=request.user
       f_name=form.cleaned_data['first_name']
       l_name=form.cleaned_data['last_name']
       em=form.cleaned_data['email']
       con=form.cleaned_data['Contract_Number']
       div=form.cleaned_data['division']
       dis=form.cleaned_data['district']
       thana=form.cleaned_data['thana']
       un=form.cleaned_data['Union']

       pro=customers(user=user,first_name=f_name,last_name=l_name,Contract_Number=con,email=em,division=div,district=dis, thana=thana,Union=un)

       pro.save()
       return HttpResponseRedirect('/address/')
    return render(request,'profile.html',{'form':form})
    

def address(request):
    add=customers.objects.filter(user=request.user)
    return render(request,'address.html',{'add':add})

def users(request):
   return render(request,'users.html')



def show_cart(request):
    total_item=0
    if request.user.is_authenticated:
        total_item=len(Cart.objects.filter(user=request.user))
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shiping_amount=0.50
        total_amount=0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for p in cart_product:
                temamount=(p.quantity*p.product.price)
                amount=temamount+amount
                totalammount=amount+shiping_amount
            print(Cart.line_total)  
            
            cuponform=CuponcodeFrom(request.POST)
            if cuponform.is_valid():
                current_time=timezone.now()
                code=cuponform.cleaned_data.get('code')
                cupon_obj=Cupon.objects.get(code=code)
                if cupon_obj.valid_to >= current_time and cupon_obj.active :
                   get_discaunt=(cupon_obj.discaunt/100)*totalammount
                   total_price_dis=totalammount-get_discaunt
                   request.session['discaount_total']=total_price_dis
                   request.session['copon_code']=code
                   
                   return redirect('cart')
                
                else:
                   return redirect('home')
            
            total_price_dis=request.session.get('discaount_total')
            cupon_code=request.session.get('cupon_code')
            return render(request,'cart.html',{'temamount':temamount,
                 'amount':amount,
                 'totalammount':totalammount,
                 'cart':cart,
                 'shiping_amount':shiping_amount,
                 'line_total':Cart.line_total,
                 'cuponform':cuponform,
                 'total_price_dis':total_price_dis,
                 'copon_code':cupon_code,'total_item':total_item})
        else:
            
            return render(request,'404.html')
        
def search(request):
    if request.method=='GET':
        query=request.GET.get('quary')
        if query:
            product=Product.objects.filter(name__icontains=query)
            return render(request,'search.html',{'product':product})
        
        else:
            return render(request,'search.html')
        
        
def order(request):
    orders=OrderPlaced.objects.filter(user=request.user)
    return render(request,'order.html',{'oreder':orders})