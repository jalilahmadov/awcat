from django.contrib import admin
from .models import News
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)} 

    class Meta:
        model = News
admin.site.register(News, PostAdmin)
