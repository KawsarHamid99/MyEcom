from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from .forms import UserLoginForm,MyPasswordChangeForm,MyPasswordResetForm,MyPasswordSetForm
from django.contrib.auth import views as auth_view
urlpatterns = [
    path('', views.ProductView.as_view(),name="home"),
    path('product-detail/<int:id>/', views.ProductDetailsView.as_view(), name='product-detail'),
    
    path('cart/', views.add_to_cart, name='add-to-cart'),
    path('show-cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.pluscart, name='pluscart'),
    path('minuscart/', views.minuscart, name='minuscart'),
    path('removecart/', views.removecart, name='removecart'),
    
    path('buy/', views.buy_now, name='buy-now'),
    path('orders/', views.orders, name='orders'),

    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>/', views.mobile, name='mobiledata'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),



    path('login/', auth_view.LoginView.as_view(template_name="app/login.html",
        authentication_form=UserLoginForm), name='login'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name="app/login.html",
        authentication_form=UserLoginForm), name='login-account'),
    #path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/',auth_view.LogoutView.as_view(next_page='login'),name="logout"),

    path('changepassword/', auth_view.PasswordChangeView.as_view(template_name="app/changepassword.html",
    form_class=MyPasswordChangeForm,success_url="/passwordchangedone/"),name='changepassword'),
    path("passwordchangedone/",auth_view.PasswordChangeView.as_view(template_name="app/passwordchangedone.html")
    ,name="passwordchangedone"),

    path("password-reset/",auth_view.PasswordResetView.as_view(template_name="app/password_reset.html",
    form_class=MyPasswordResetForm),name="password_reset"),
    path("password-reset/done/",auth_view.PasswordResetDoneView.as_view(template_name="app/password_reset_done.html"),
    name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/",auth_view.PasswordResetConfirmView.as_view(
    template_name="app/password_reset_confirm.html",form_class=MyPasswordSetForm
    ),name="password_reset_confirm"),
    path("password-reset-complete/",auth_view.PasswordResetCompleteView.as_view(
    template_name="app/password_reset_complete.html"),name="password_reset_complete"),

    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),

    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
