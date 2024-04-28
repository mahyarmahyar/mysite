from django.urls import path
from .import views
app_name = 'accounts'

urlpatterns = [
    # تغییر از 'login' به 'login/'
    path('login/', views.login_view, name='login'),
    # تغییر از 'logout' به 'logout/'
    path('logout/', views.logout_view, name='logout'),
    # تغییر از 'singup' به 'signup/'
    path('signup/', views.signup_view, name='signup'),
]
