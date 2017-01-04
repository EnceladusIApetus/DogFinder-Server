from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    fb_id = forms.CharField(label='fb_id', widget=forms.Textarea)
    fb_name = forms.CharField(label='fb_name')
    fb_token = forms.CharField(label='fb_token', widget=forms.Textarea)
    fb_token_exp = forms.DateTimeField(label='fb_token_exp')
    email = forms.EmailField(label='email')
    birth_date = forms.DateField(label='birth_date')
    telephone = forms.CharField(label='tel')


    class Meta:
        model = User
        fields = ('fb_id', 'fb_name', 'fb_token', 'fb_token_exp', 'telephone', 'email', 'birth_date')


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    class Meta:
        model = User
        fields = ('fb_id', 'fb_name', 'fb_token', 'fb_token_exp', 'telephone', 'email', 'birth_date')


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('fb_id', 'fb_name', 'fb_token', 'fb_token_exp', 'telephone', 'email', 'birth_date', 'role')
    list_filter = ('role',)
    fieldsets = (
        (None, {'fields': ('email', 'fb_id', 'fb_name', 'fb_token', 'fb_token_exp', 'telephone',)}),
        ('Personal info', {'fields': ('birth_date',)}),
        ('Permissions', {'fields': ('role',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('fb_id', 'fb_name', 'fb_token', 'fb_token_exp', 'telephone', 'email', 'birth_date', 'role')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)