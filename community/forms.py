from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Comment


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-posta")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("avatar", "bio", "favorite_coffee")
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {
            "text": forms.Textarea(attrs={"rows": 3, "placeholder": "Yorumunu yaz..."}),
        }
        labels = {"text": ""}
