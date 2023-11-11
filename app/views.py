from django.shortcuts import render,HttpResponseRedirect,redirect,HttpResponse
from  .models import Customer,Product,cart,OrderPlaced,Category,Productcolor,ProductSize
from django.views import View
from django.contrib import messages
from .forms import CustomerRegistrationForm,UserLoginForm,CustomerProfileForm,EditUserProfileForm
from .forms import CustomerAddresUpdateForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.conf import settings
import stripe,json,time,uuid,string,random
from django.core.mail import EmailMessage

stripe.api_key=settings.STRIPE_SECRET_KEY


def email_sending(subject,message,recieveb_by):

  mail=EmailMessage(subject,message,settings.EMAIL_HOST_USER,recieveb_by)
  mail.send()
  

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
  

