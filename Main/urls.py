from django.contrib import admin
from django.urls import path
from . import views
from.forms import loginform,passwordchangeform
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls. static import static

urlpatterns = [
    path('', views.homeView.as_view(), name = 'home'),
    path('shop/',views.shop,name='shop'),
    path('shop-detail/<int:pk>',views.shop_detailView.as_view(),name='shop-detail'),
    path('cart/',views.show_cart,name='cart'),
    path('add-to-card/',views.cart,name='add-to-card'),
    path('chackout/',views.chackout,name='chackout'),
    path('testimonial',views.testimonial,name='testimonial'),
    path('error/',views.error,name='error'),
    path('contract/',views.contract,name='contract'),
    
    path('plus_cart',views.plus_cart,name="plus_cart"),
    path('minas_cart',views.minas_cart,name="minas_cart"),
    path('delete_cart/<int:id>',views.delete_cart,name="delete_cart"),
    

    path('accounts/login/',auth_view.LoginView.as_view(template_name='login.html',authentication_form=loginform),name='login'),

    path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout'),

    path('registration/',views.registrationView.as_view(),name='registration'),
    path('profile/',views.cprofileView.as_view(),name='profile'),
    path('address/',views.address,name='address'),
    path('users/',views.users,name='users'),
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='passwordchange.html',form_class=passwordchangeform),name='passwordchange'),

    path('password_change/done//',auth_view.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'),name='password_change_done'),
    
    path('vegetable/',views.vegetable,name='vegetable'),
    path('meat/',views.meats,name='meat'),
    path('fruit/',views.fruit,name='fruit'),
    path('bread/',views.Breads,name='bread'),
    path('paymeny/',views.payment,name='payment'),
    path('search/',views.search,name='search'),
    
    path('order/',views.order,name='order')
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)