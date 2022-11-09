from django.contrib import admin
from .models import Post,Comment
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ('user','slug','updated',)
    list_filter = ('updated',)
    search_fields = ('slug','body',)
    raw_id_fields = ('user',)
    prepopulated_fields = {'slug':('body',)}
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user','body','post','is_reply','reply','created')
    raw_id_fields = ('user','post','reply')

