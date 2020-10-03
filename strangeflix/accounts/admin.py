from django.contrib import admin
from .models import CustomUser, UserDetails
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserModelAdmin(UserAdmin):

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = (
        # This defines fields which is to displayed
        'id', 'username', 'user_type', 'email',
    )
    fieldsets = (
        # Can add only original fields of User
        ('Account info', {'fields': ('username', 'email', 'password',)}),
        ('Permission', {'fields': ('user_type', 'is_superuser', 'is_staff', 'is_active')}),
        ('Extra info', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        # This defines fields displayed in Django Admin when ADD USER button
        # is clicked.
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'user_type', 'password1', 'password2'),
        }),
    )

admin.site.register(CustomUser, CustomUserModelAdmin)
admin.site.register(UserDetails)