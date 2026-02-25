from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('feed/', views.feed, name='feed'),
    path('search/', views.search_users, name='search_users'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('my-profile/', views.my_profile, name='my_profile'),
    path('create-post/', views.create_post, name='create_post'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
]
