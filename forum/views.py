from django.http import HttpResponse
from django.template import loader
from .models import Topic, Post, Comment
from .forms import PostForm, RegisterForm, TopicForm, CommentForm, UpdateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.forms import PasswordChangeForm


# user managing


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/forum/')
    else:
        form = RegisterForm()

    template = loader.get_template('registration/register.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))


@login_required
def user_profile(request, user_id):
    user = request.user
    template = loader.get_template('forum/user_profile.html')
    context = {'user': user}
    return HttpResponse(template.render(context, request))


@login_required
def edit_profile(request, user_id):
    user = request.user
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('/forum/user_profile/' + user_id)
    else:
        form = UpdateUserForm(initial={'username': user.username, 'first_name': user.first_name,
                                       'last_name': user.last_name, 'email': user.email, })

    template = loader.get_template('forum/edit_profile.html')
    context = {'form': form, 'user': user}
    return HttpResponse(template.render(context, request))


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('/forum/')
    else:
        form = PasswordChangeForm(request.user)

    template = loader.get_template('registration/change_password.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))


# main views in forum


@login_required
def index(request):
    topics_list = Topic.objects.order_by('-published_date')
    template = loader.get_template('forum/index.html')
    context = {'topics_list': topics_list}
    return HttpResponse(template.render(context, request))


@login_required
def topic(request, topic_id):
    posts_list = Post.objects.filter(topic=topic_id).order_by('-published_date')
    comments_list = Comment.objects.order_by('-published_date')
    template = loader.get_template('forum/topic.html')
    context = {'posts_list': posts_list, 'topic': Topic.objects.get(id=topic_id),
               'comments_list': comments_list}
    return HttpResponse(template.render(context, request))


# topics managing


@login_required
def add_topic(request):
    if request.method == 'POST':
        new_topic = Topic()
        form = TopicForm(request.POST, instance=new_topic)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.user = request.user
            new_topic.save()
            return redirect('/forum/')
    else:
        form = TopicForm()

    template = loader.get_template('forum/add_topic.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))


@login_required
def delete_topic(request, topic_id):
    if request.method == 'POST':
        Topic.objects.filter(id=topic_id).delete()
        return redirect('/forum/')

    this_topic = get_object_or_404(Topic, id=topic_id)
    template = loader.get_template('forum/delete_topic.html')
    context = {'topic': this_topic}
    return HttpResponse(template.render(context, request))


@login_required
def edit_topic(request, topic_id):
    this_topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        form = TopicForm(request.POST, instance=this_topic)
        if form.is_valid():
            this_topic = form.save(commit=False)
            this_topic.save()
            return redirect('/forum/')
    else:
        form = TopicForm(initial={'name': this_topic.name, })

    template = loader.get_template('forum/edit_topic.html')
    context = {'form': form, 'topic': this_topic}
    return HttpResponse(template.render(context, request))


# posts managing

@login_required
def add_post(request, topic_id):
    this_topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        new_post = Post(topic=this_topic)
        form = PostForm(request.POST, instance=new_post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect('/forum/topic/' + topic_id)
        else:
            print(form.errors)
    else:
        form = PostForm()

    template = loader.get_template('forum/add_post.html')
    context = {'form': form, 'topic': this_topic}
    return HttpResponse(template.render(context, request))


@login_required
def delete_post(request, topic_id, post_id):
    if request.method == 'POST':
        Post.objects.filter(id=post_id).delete()
        return redirect('/forum/topic/' + topic_id)

    this_topic = get_object_or_404(Topic, id=topic_id)
    this_post = get_object_or_404(Post, id=post_id)

    template = loader.get_template('forum/delete_post.html')
    context = {'topic': this_topic, 'post': this_post}
    return HttpResponse(template.render(context, request))


@login_required
def edit_post(request, topic_id, post_id):
    this_topic = get_object_or_404(Topic, id=topic_id)
    this_post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=this_post)
        if form.is_valid():
            this_post = form.save(commit=False)
            this_post.save()
            return redirect('/forum/topic/' + topic_id)
    else:
        form = PostForm(initial={'post_text': this_post.post_text, })

    template = loader.get_template('forum/edit_post.html')
    context = {'form': form, 'topic': this_topic, 'post': this_post}
    return HttpResponse(template.render(context, request))


# comments managing


@login_required
def add_comment(request, topic_id, post_id):
    this_post = get_object_or_404(Post, id=post_id)
    this_topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        new_comment = Comment(post=this_post)
        form = CommentForm(request.POST, instance=new_comment)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.save()
            return redirect('/forum/topic/' + topic_id)
        else:
            print(form.errors)
    else:
        form = CommentForm()

    template = loader.get_template('forum/add_comment.html')
    context = {'form': form, 'post': this_post, 'topic': this_topic}
    return HttpResponse(template.render(context, request))


@login_required
def delete_comment(request, topic_id, post_id, comment_id):
    if request.method == 'POST':
        Comment.objects.filter(id=comment_id).delete()
        return redirect('/forum/topic/' + topic_id)

    this_topic = get_object_or_404(Topic, id=topic_id)
    this_post = get_object_or_404(Post, id=post_id)
    this_comment = get_object_or_404(Comment, id=comment_id)

    template = loader.get_template('forum/delete_comment.html')
    context = {'topic': this_topic, 'post': this_post, 'comment': this_comment}
    return HttpResponse(template.render(context, request))


@login_required
def edit_comment(request, topic_id, post_id, comment_id):
    this_topic = get_object_or_404(Topic, id=topic_id)
    this_post = get_object_or_404(Post, id=post_id)
    this_comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=this_comment)
        if form.is_valid():
            this_comment = form.save(commit=False)
            this_comment.save()
            return redirect('/forum/topic/' + topic_id)
    else:
        form = CommentForm(initial={'comment_text': this_comment.comment_text, })

    template = loader.get_template('forum/edit_comment.html')
    context = {'form': form, 'topic': this_topic, 'post': this_post, 'comment': this_comment}
    return HttpResponse(template.render(context, request))
