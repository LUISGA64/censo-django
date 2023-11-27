from django.urls import path
from .views import home, association, LoginView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', home, name='home'),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page='accounts/log'), name="logout"),
    path("asociacion/", association, name="asociacion"),

]