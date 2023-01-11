from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _

from users.models import User

# Register your models here.

class UserAdmin(UserAdmin):
    """User Admin Panel Configuration"""

    model = User
    readonly_fields = ('date_joined',)
    filter_horizontal = ('groups', 'user_permissions')
    list_display = ('email', 'first_name', 'last_name', 'date_joined')
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name', 'name', 'date_joined', 'is_acitve', 'is_staff', 'is_superuser',)


    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'),{'fields': ('first_name', 'last_name', 'avatar')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

admin.site.register(User, UserAdmin)    
