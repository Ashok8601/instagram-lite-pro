from django.urls import path
from . import views
urlpatterns = [
    path('create_post/', views.create_post, name='create_post'),
    path('get_posts/', views.get_posts, name='get_posts'),
    path('post-reel/',views.reel_post,name='reel_post'),
    path('explore/', views.explore, name='explore'),
]