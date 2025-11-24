from django.contrib import admin
from newspaper.models import Advertisement, Category, Post, Tag, Contact

# Register your models here.

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Advertisement)
admin.site.register(Contact)
