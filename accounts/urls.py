from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path,include
from accounts.forms import UserLoginForm
from accounts.views import RegisterView,edite_profile

urlpatterns = [
    path('login/', LoginView.as_view(authentication_form=UserLoginForm),name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/',edite_profile, name='profile'),
    path('', include('django.contrib.auth.urls'))
]