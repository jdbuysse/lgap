from django.urls import path
from . import views
from django.contrib import admin
# what does this do?
from django.urls import include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/new/', views.post_new, name='post_new'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('mytexts/', views.TextsByUserListView.as_view(), name='my-texts'),
    path('uploadtest/', views.upload, name='upload-tester'),
    path('workspace/', views.workspace, name='workspace'),
    path('upload', views.UploadTextView.as_view(), name='upload-text')
    # if I want to go the pattern-matching url route for working with a specific book, something like this?
    # path('workspace/<int:pk>', views.workspace, name='workspacetext')
]

