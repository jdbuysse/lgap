from django.urls import path
from . import views
from django.contrib import admin
# what does this do?
from django.urls import include
from . import views

urlpatterns = [
    # honestly I need to look up the pattern matching sometime, I'm confused by it
    path('', views.index, name='index'),
    path('post/new/', views.post_new, name='post_new'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('mytexts/', views.TextsByUserListView.as_view(), name='my-texts'),
    path('uploadtest/', views.uploadtest, name='upload-tester'),
]

