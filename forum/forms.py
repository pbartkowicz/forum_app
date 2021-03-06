from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Topic, Post, Comment


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('name', )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post_text', )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_text', )


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
