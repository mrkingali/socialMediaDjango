from django.contrib import admin
from .models import Post
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ('user','slug','updated',)
    list_filter = ('updated',)
    search_fields = ('slug','body',)
    raw_id_fields = ('user',)
    prepopulated_fields = {'slug':('body',)}
