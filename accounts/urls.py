from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import LoginForm

app_name = "accounts"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(authentication_form = LoginForm),
        name="login",
    ),
    path("logout/", auth_views.LoginView.as_view(), name="logout"),
]