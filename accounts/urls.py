from django.urls import path
from  . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.home , name = 'home'),
    path('register/', views.registerPage , name = 'register'),
    path('login/', views.loginPage , name = 'login'),
    path('logout/', views.logoutUser , name = 'logout'),
    path('user/', views.userPage , name = 'user_page'),

    path('account/' , views.accountSettings , name ='account'),


    path('products/', views.products , name='products'),
    path('cust/<str:pk_test>/', views.cust , name = 'cust'),
    path('create_order/<str:pk>/' , views.createOrder , name='create_order'),
    path('update_order/<str:pk>/' , views.UpdateOrder , name='update_order'),
    path('delete_order/<str:pk>/', views.DeleteOrder, name='delete_order'),



    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>//', auth_views.PasswordResetConfirmView.as_view(), name ='password_reset_confirm'),
    path('reset_password_completed/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
