from email import message
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.utils import timezone
from datetime import timedelta
from .models import Post, OurTeam
from newspaper.models import Advertisement, Contact, Tag 
from django.urls import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from newspaper.forms import CommentForm, ContactForm
from django.views.generic.edit import FormMixin

class SidebarMixin:
     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_posts"] = Post.objects.filter(
            published_at__isnull=False,
            status="active"
        ).order_by("-published_at")[:5]

        context["advertisements"] = (
            Advertisement.objects.all().order_by("-created_at").first()
        )

        return context
# Create your views here.
class HomeView(SidebarMixin,TemplateView):
    template_name = "newsportal/home.html"
    
    # If we want to add extra context data to our template we use get_context_data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breaking_news"] = Post.objects.filter(
            is_breaking_news=True,
            published_at__isnull=False,
            status="active"
        ).order_by("-published_at")[:3]

        context["featured_post"] = (
            Post.objects.filter(published_at__isnull=False, status="active")
            .order_by("-published_at", "views_count")
            .first()
        )
        context["trending_news"] = Post.objects.filter(
            published_at__isnull=False,
            status="active"
        ).order_by("-published_at")[:4]

        one_week_ago = timezone.now() - timedelta(days=7)
        context["weekly_top_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active", published_at__gte=one_week_ago
        ).order_by("-published_at", "-views_count")[:5]
        context["popular_posts"] = Post.objects.filter(
            published_at__isnull=False,
            status="active"
        ).order_by("-published_at")[:5]
        return context
class PostListView(SidebarMixin,ListView):
    model = Post
    template_name = "newsportal/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        return Post.objects.filter(
            published_at__isnull=False,
            status="active"
        ).order_by("-published_at")
    


class PostDetailView(SidebarMixin, FormMixin, DetailView):
    model = Post
    template_name = "newsportal/detail/detail.html"
    context_object_name = "post"
    form_class = CommentForm

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.pk}) # stay on the same post

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.post = self.object
        comment.save()
        messages.success(self.request, "Your comment has been added successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error submitting your comment.")
        return super().form_invalid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_post = self.object
        current_post.views_count += 1
        current_post.save()

        context["related_articles"] = (
            Post.objects.filter(
                published_at__isnull=False,
                status="active",
                category=self.object.category
            )
            .exclude(id=self.object.id)
            .order_by("-published_at", "-views_count")[:2]
        )
        return context
    
class ContactCreateView(SuccessMessageMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "newsportal/contact.html"
    success_url = reverse_lazy("contact")
    success_message = "Your message has been sent successfully!"

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error sending your message. Please check the form.",
        )
        return super().form_invalid(form)
    
    
from django.views.generic import TemplateView


from django.views.generic import ListView
from .models import Tag, Category   # adjust if your model is named differently

class AllTagsView(ListView):
    model = Tag
    template_name = "all_tags.html"
    context_object_name = "tags"

class AllCategoriesView(ListView):
    model = Category
    template_name = "all_categories.html"  # create this template
    context_object_name = "categories"

class AboutView(TemplateView):
    template_name = "about.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["our_teams"] = OurTeam.objects.all()
        return context