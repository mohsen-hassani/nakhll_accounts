from django.urls import path
from accounts import views

urlpatterns = [
    path('get-phone/', views.get_phone, name='accounts_get_phone'),
    path('register/', views.register, name='accounts_register'),
    path('login/', views.login_by_code, name='accounts_login_by_code'),
    path('forget-password/', views.forget_password, name='accounts_forget_password'),
    path('set-password/', views.set_password, name='accounts_set_password'),
    path('change-password/', views.change_password, name='accounts_change_password'),
    path('password/', views.password, name='accounts_password'),

    path('dashboard/', views.dashboard, name='accounts_dashboard'),
    path('logout/', views.logout_user, name='accounts_logout'),
]