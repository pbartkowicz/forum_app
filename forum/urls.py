from . import views
from django.conf.urls import url

app_name = 'forum'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^topic/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    url(r'^add_topic/', views.add_topic, name='add_topic'),
    url(r'^add_post/(?P<topic_id>\d+)/$', views.add_post, name='add_post'),
    url(r'^add_comment/(?P<topic_id>\d+)/(?P<post_id>\d+)/$', views.add_comment, name='add_comment'),
    url(r'^edit_topic/(?P<topic_id>\d+)/$', views.edit_topic, name='edit_topic'),
    url(r'^edit_post/(?P<topic_id>\d+)/(?P<post_id>\d+)/$', views.edit_post, name='edit_post'),
    url(r'^edit_comment/(?P<topic_id>\d+)/(?P<post_id>\d+)/(?P<comment_id>\d+)/$',
        views.edit_comment, name='edit_comment'),
    url(r'^delete_topic/(?P<topic_id>\d+)/$', views.delete_topic, name='delete_topic'),
    url(r'^delete_post/(?P<topic_id>\d+)/(?P<post_id>\d+)/$', views.delete_post, name='delete_post'),
    url(r'^delete_comment/(?P<topic_id>\d+)/(?P<post_id>\d+)/(?P<comment_id>\d+)/$',
        views.delete_comment, name='delete_comment'),
    url(r'^user_profile/(?P<user_id>\d+)/$', views.user_profile, name='user_profile'),
    url(r'^edit_profile/(?P<user_id>\d+)/$', views.edit_profile, name='edit_profile'),
    url(r'^change_password/$', views.change_password, name='change_password'),
]
