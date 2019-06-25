from django.urls import path
from . import views

urlpatterns = [
    # honestly I need to look up the pattern matching sometime I'm confused by it
    path('', views.index, name='index'),
    path('post/new/', views.post_new, name='post_new'),
]

