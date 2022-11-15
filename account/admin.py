from django.contrib import admin
from .models import  Relation,Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False

class ExtendedUserAdmin(BaseUserAdmin):
    inlines = (ProfileInLine,)

admin.site.unregister(User)
admin.site.register(User,ExtendedUserAdmin)


admin.site.register(Relation)

