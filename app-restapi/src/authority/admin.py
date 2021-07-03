from django.contrib import admin
from django.contrib.auth import get_user_model

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from authority.forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
    'email', 'username', 'first_name', 'last_name', 'is_active', 'is_superuser', 'is_admin', 'is_staff',)
    list_filter = ('is_active', 'is_superuser', 'is_admin', 'is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'about_me')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_admin', 'is_staff',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')}
         ),
    )
    search_fields = ('email', 'username', 'first_name', 'last_name',)
    ordering = ('email', 'username', 'first_name', 'last_name',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)

admin.site.unregister(Group)