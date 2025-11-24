from django.urls import path
from .views import HomeView
from . import views
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("post-list/", views.PostListView.as_view(), name="post-list"),
    path("post-detail/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("contact/", views.ContactCreateView.as_view(), name="contact"),
]
