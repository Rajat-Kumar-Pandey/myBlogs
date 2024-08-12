from django.contrib import admin
from .models import Blog, Category ,Comment

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

# Register the Blog model with BlogAdmin
admin.site.register(Blog, BlogAdmin)

# Register the Category model with the default ModelAdmin
admin.site.register(Category)
admin.site.register(Comment)

