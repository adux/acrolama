from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext, gettext_lazy as _

from .models import User


class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = [
        'email', 'first_name', 'last_name', 'is_staff', 'is_teacher'
    ]
    list_filter = [
        'is_staff', 'is_teacher', 'is_active', 'email'
    ]
    ordering = ['email']
    fieldsets = (
       (None, {'fields': ('email', 'password')}),
       (_('Personal info'), {
           'fields': (
               'pronoun',
               'first_name',
               'last_name',
               'phone',
               'address',
               'birth_date',
           )
       }),
       (_('Teacher & Stuff info'), {
           'fields': (
               'avatar',
               'title',
               'short_description',
               'long_description',
           )
       }),
       (_('Permissions'), {
           'fields': ('is_active', 'is_staff', 'is_teacher',
                      'is_superuser', 'groups', 'user_permissions'),
          }),
       (_('Important dates'), {
           'fields': ('last_login', 'date_joined')
       }),
    )
    add_fieldsets = (
        (None, {
              'classes': ('wide',),
              'fields': ('email', 'password1', 'password2'),
           }),
    )


admin.site.register(User, UserAdmin)
