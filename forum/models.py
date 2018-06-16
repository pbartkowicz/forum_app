from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField(max_length=128)
    published_date = models.DateTimeField('published date', default=datetime.now())
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Post(models.Model):
    post_text = models.TextField(max_length=800)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    published_date = models.DateTimeField('published date', default=datetime.now())

    def __str__(self):
        return self.post_text


class Comment(models.Model):
    comment_text = models.TextField(max_length=800)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    published_date = models.DateTimeField('published date', default=datetime.now())

    def __str__(self):
        return self.comment_text

    def __get__(self, instance, owner):
        return self.comment_text

