from django.shortcuts import render,HttpResponseRedirect,redirect,HttpResponse
from  .models import Customer,Product,cart,OrderPlaced,Category
from django.views import View
from django.contrib import messages
from .forms import CustomerRegistrationForm,UserLoginForm,CustomerProfileForm
from django.contrib.auth import login,logout,authenticate
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.conf import settings
import stripe

stripe.api_key=settings.STRIPE_SECRET_KEY

class ProductView(View):
 def get(self,request):
  totalitem=0
  topwares=Product.objects.all()
  bottomwares=Product.objects.all()
  mobiles=Product.objects.all()
  laptops=Product.objects.all()
  
  parentsCategory=Category.objects.filter(parent__isnull=True).get_descendants()
  categories_without_children = Category.objects.filter(children__isnull=True)
 


  electronics_P=Category.objects.get(pk=4)
  electronics=Category.objects.filter(parent=electronics_P)

  allproducts=Product.objects.all()
  paginator = Paginator(allproducts, 100)  
  page = request.GET.get('page')
  products = paginator.get_page(page)


  if request.user.is_authenticated:
   totalitem=len(cart.objects.filter(user=request.user))
  return render(request,'app/home.html',{'topwares':topwares,
            "bottomwares":bottomwares,"mobiles":mobiles,"laptops":laptops,
            "totalitem":totalitem,"products":products,"categories":categories_without_children})
  


class ProductDetailsView(View):
 def get(self,request,id):
  totalitem=0
  product=Product.objects.get(id=id)

  item_already_in_cart=False
  
  if request.user.is_authenticated:
  #  print(cart.objects.filter(product=product.id,user=request.user.id))
   #item_already_in_cart=cart.objects.filter(Q(product=product.id),Q(user=request.user.username))
   item_already_in_cart=cart.objects.filter(product=product.id,user=request.user.id)
 
   return render(request,'app/productdetail.html',{"product":product,"item_already_in_cart":item_already_in_cart,"totalitem":totalitem})
  else:
    return render(request,'app/productdetail.html',{"product":product,"totalitem":totalitem})
   


class CustomerRegistrationView(View):
 def get(self,request):
  form=CustomerRegistrationForm()
  return render(request,"app/customerregistration.html",{"form":form})
 
 def post(self,request):
  form=CustomerRegistrationForm(request.POST)
  if form.is_valid():
   form.save()
   messages.success(request,"registration has been completed successfully...")
  return render(request,"app/customerregistration.html",{"form":form})


#we can use this as a login class.also we can use inbuild login class which has been shown in urls.py
class UserLoginView(View):
 def get(self,request):
  form=UserLoginForm()
  return render(request,"app/login.html",{"form":form})
 def post(self,request):
  form=UserLoginForm(request=request,data=request.POST)
  if form.is_valid():
   uname=form.cleaned_data["username"]
   upass=form.cleaned_data["password"]
   user=authenticate(username=uname,password=upass)
   if user is not None:
    login(request,user)
    messages.success(request,"login successfully...")
    return HttpResponseRedirect("/")
  return render(request,"app/login.html",{"form":form})


@method_decorator(login_required,name='dispatch')
class ProfileView(View):
 def get(self,request):
  fm=CustomerProfileForm()
  return render(request,"app/profile.html",{"form":fm,"active":"btn-primary"})
 def post(self,request):
  fm=CustomerProfileForm(request.POST)
  if fm.is_valid():
   user=request.user
   name=fm.cleaned_data["name"]
   locality=fm.cleaned_data["locality"]
   city=fm.cleaned_data["city"]
   zipcode=fm.cleaned_data["zipcode"]
   state=fm.cleaned_data["state"]
   reg=Customer(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
   reg.save()
   messages.success(request,"Congratulations.profile added...!!! ")
  return render(request,"app/profile.html",{"form":fm,'active':"btn-primary"})

def address(request):
 user_address=Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{"address":user_address,"status":"btn-primary"})

@login_required
def add_to_cart(request):
 user=request.user
 product_id=request.GET.get("prod_id")
 product=Product.objects.get(id=product_id)
 if not cart.objects.filter(user=user,product=product).exists():
  cart(user=user,product=product).save()
 #return render(request,'app/addtocart.html')
 return redirect("/show-cart/")

@login_required
def show_cart(request):
 if request.user.is_authenticated:
  user=request.user
  Cart=cart.objects.filter(user=user)
  amount=0.0
  shiping_amount=70
  total_amount=0.0
  cart_product=[p for p in cart.objects.all() if p.user==user]
  if cart_product:
   for p in cart_product:
    if p.product.discounted_price:
     tempamount= p.quantity * p.product.discounted_price
    else:
     tempamount= p.quantity * p.product.selling_price
     
     
    amount += tempamount
    total_amount = shiping_amount + amount
   return render(request,'app/addtocart.html',{'cart': Cart,"amount":amount,"total_amount":total_amount,"shiping_amount":shiping_amount})
  else:
   empty=None
   return render(request,'app/addtocart.html',{"cart":empty})


def pluscart(request):
 if request.method=="GET":
  prod_id=request.GET["prod_id"]
  user=request.user
  Cart=cart.objects.get(Q(user=user),Q(product=prod_id))
  Cart.quantity += 1
  Cart.save()

  amount=0.0
  shiping_amount=70
  total_amount=0.0

  cart_product=[p for p in cart.objects.all() if p.user==user]
 
  for p in cart_product:
   if p.product.discounted_price:
    tempamount= p.quantity * p.product.discounted_price
   else:
    tempamount= p.quantity * p.product.selling_price
   amount += tempamount
   total_amount = shiping_amount + amount
  data={
   'amount':amount,
   'totalamount':total_amount,
   'quantity':Cart.quantity,
   #'total_cost':Cart.total_cost
  }
  return JsonResponse(data)


def minuscart(request):
 if request.method=="GET":
  prod_id=request.GET["prod_id"]
  user=request.user
  Cart=cart.objects.get(Q(user=user),Q(product=prod_id))
  if Cart.quantity > 1:
   Cart.quantity -= 1
  else:
   Cart.quantity = 1
   
  Cart.save()

  amount=0.0
  shiping_amount=70
  total_amount=0.0

  cart_product=[p for p in cart.objects.all() if p.user==user]
 
  for p in cart_product:
   if p.product.discounted_price:
    tempamount= p.quantity * p.product.discounted_price
   else:
    tempamount= p.quantity * p.product.selling_price
   amount += tempamount
   total_amount = shiping_amount + amount
  data={
   'amount':amount,
   'totalamount':total_amount,
   'quantity':Cart.quantity,
   #'total_cost':Cart.total_cost
  }
  return JsonResponse(data)


def removecart(request):
 if request.method=="GET":
  prod_id=request.GET["prod_id"]
  user=request.user
  Cart=cart.objects.get(Q(user=user),Q(product=prod_id))

  Cart.delete()

  amount=0.0
  shiping_amount=70
  total_amount=0.0

  cart_product=[p for p in cart.objects.all() if p.user==user]
 
  for p in cart_product:
   if p.product.discounted_price:
    tempamount= p.quantity * p.product.discounted_price
   else:
    tempamount= p.quantity * p.product.selling_price
   amount += tempamount
   total_amount = shiping_amount + amount
  data={
   'amount':amount,
   'totalamount':total_amount,
   'quantity':Cart.quantity
  }
  return JsonResponse(data)




def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request,data=None,pk=None):
 if data==None:
  #mobile=Product.objects.filter(category=8)
  mobile=Product.objects.all()
 elif(data=="Xiaomi" or data=="Apple"):
  mobile=Product.objects.filter(category=8).filter(brand=data)
 elif(data=="Below"):
  mobile=Product.objects.filter(category=8).filter(discounted_price__lte=20000)
 else:
  mobile=Product.objects.filter(category=8).filter(discounted_price__gt=20000)
 return render(request, 'app/category_based.html',{"mobiles":mobile})

def category_based(request,pk=None):
 print("-----------------------------------------------")
 category=Category.objects.filter(parent__isnull=True)
 category=Category.objects.filter(parent__parent__isnull=True,parent__isnull=False)
 categories_without_children = Category.objects.filter(children__isnull=True)
 last_level_child = Category.objects.get(pk=pk) 
 root_parent = last_level_child.get_root_parent()
 all_level_children = root_parent.get_all_children()
 path_to_last_child = last_level_child.get_path_to_last_child()

 children_of_parent = Category.find_children_by_parent_pk(pk)
 search_category=Product.objects.filter(category__parent=pk)
 if not children_of_parent:
  children=Category.objects.get(pk=pk)
  print(children.parent.id)
  children_of_parent=Category.find_children_by_parent_pk(children.parent.id)
  print(children_of_parent)
  search_category=Product.objects.filter(category=pk)

 return render(request, 'app/category_based.html',{"mobiles":search_category,"catragorylist":children_of_parent,"root_parent":root_parent})

@login_required
def checkout(request):
 user=request.user
 add=Customer.objects.filter(user=user)
 cart_items=cart.objects.filter(user=user)

 amount=0.0
 shipping_amount=70.0
 totalamount= 0.0
 cart_product=[p for p in cart.objects.all() if p.user==user ]
 if cart_product:
  for p in cart_product:
   if p.product.discounted_price:
    tempamount= p.quantity*p.product.discounted_price
    amount += tempamount
   else:
    tempamount= p.quantity*p.product.selling_price
    amount += tempamount
  totalamount=amount+shipping_amount
 return render(request, 'app/checkout.html',{"add":add,"totalamount":totalamount,
 "amount":amount,"shipping":shipping_amount,"cart_items":cart_items,'key':settings.STRIPE_PUBLIC_KEY})

@login_required
def payment(request):
 custid = request.POST.get('custid')
 user=request.user
 customer=Customer.objects.get(id=custid)
 Cart=cart.objects.filter(user=user)
 print("------------------------------------------------------")
 print(Cart)
 totalprice=0
 productlist=[]
 for c in Cart:
  if c.product.discounted_price:
    totalprice=totalprice+int(c.quantity)*c.product.discounted_price
    productlist.append(["PN:"+ str(c.product) +"; PQ:" + str(c.quantity)  +"; Price/unit:"+ str(c.product.discounted_price)])
  else:
   totalprice=totalprice+int(c.quantity)*c.product.selling_price
   productlist.append(["PN:"+ str(c.product) +"; PQ:" + str(c.quantity)  +"; Price/unit:"+ str(c.product.selling_price)])
   
  OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,status="Accepted").save()
  c.delete()
 charge=stripe.Charge.create(amount=int(totalprice*100),currency='usd',description=str(productlist),source=request.POST['stripeToken'])
 return redirect("orders")
 
def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def orders(request):
 op=OrderPlaced.objects.filter(user=request.user).order_by("orderd_date").reverse()
 return render(request, 'app/orders.html',{'op':op})


def aboutus(request):
 return render(request,"app/aboutus.html")

def customersupport(request):
 return render(request,"app/customersupport.html")


def test(request):
 order=OrderPlaced.objects.filter(user=request.user)

 print("-----------------------------------")
 print(request.user)
 print(order)
#  print(order[0].customer.id)
 return HttpResponse("Under testing")