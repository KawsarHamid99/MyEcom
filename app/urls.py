from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from .forms import UserLoginForm,MyPasswordChangeForm,MyPasswordResetForm,MyPasswordSetForm
from django.contrib.auth import views as auth_view


from django.urls import re_path

from django.views.static import serve
# client did not paid yet for this website
# if you are a developer get your payment first.otherwise there is a chance to not get paid.
# please contact to to developer: kawsahamid7225@gmail.com
# https://www.linkedin.com/in/kawsar-hamid-6b6a86241/

urlpatterns = [

    re_path(r'^media/(?P<path>.*)$',serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$',serve,{'document_root': settings.STATIC_ROOT}),

    path('', views.ProductView.as_view(),name="home"),

    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
