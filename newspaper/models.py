from django.db import models

# Create your models here.

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True # Don't create a table in DB
class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"] # category.objects.all()
        verbose_name = "category"
        verbose_name_plural = "Categories"


class Tag(TimeStampedModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Post(TimeStampedModel):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("in-active", "Inactive"),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="post_images/%Y/%m/%d/", blank=True)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    status = models.CharField(max_length = 20, choices = STATUS_CHOICES, default="active")
    views_count = models.PositiveIntegerField(default=0)
    is_breaking_news = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
    
class Advertisement(TimeStampedModel):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="advertisements/%Y/%m/%d", blank=False)

    def __str__(self):
        return self.title
    
class Contact(TimeStampedModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]


class OurTeam(TimeStampedModel):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    image = models.ImageField(upload_to="team_image/%Y/%m/%d", blank=False)
    description = models.TextField()

    def __str__(self):
        return self.name
    

class Comment(TimeStampedModel):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"{self.user} - {self.post}"
