from django.urls import path
from .views import HomeView
from . import views
from .views import AllTagsView, AllCategoriesView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("post-list/", views.PostListView.as_view(), name="post-list"),
    path("post-detail/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("contact/", views.ContactCreateView.as_view(), name="contact"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("tags/", AllTagsView.as_view(), name="all-tags"),
    path("categories/", AllCategoriesView.as_view(), name="all-categories"),


]
