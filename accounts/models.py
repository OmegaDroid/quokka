from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy


class UserProfile(models.Model):
    user = models.ForeignKey(User)

    @property
    def name(self):
        return self.firstName + " " + self.lastName

    def __str__(self):
        return self.name


class NewUserForm(UserCreationForm):
    first_name = forms.CharField(label=ugettext_lazy("First Name"), required=True)
    last_name = forms.CharField(label=ugettext_lazy("Last Name"), required=True)

    email = forms.CharField(
        label=ugettext_lazy("Email Address"),
        required=True,
        widget=forms.EmailInput
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
