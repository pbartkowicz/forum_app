from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Topic, Post, Comment


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('name', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'char-field'}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post_text', )
        widgets = {
            'post_text': forms.TextInput(attrs={'class': 'text-field'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_text', )
        widgets = {
            'comment_text': forms.TextInput(attrs={'class': 'text-field'}),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=256)
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
