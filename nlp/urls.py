from django.urls import path
from . import views
from django.contrib import admin
from django.urls import include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/new/', views.post_new, name='post_new'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('mytexts/', views.TextsByUserListView.as_view(), name='my-texts'),
    path('upload/', views.UploadTextView.as_view(), name='upload-text'),
    path('userworkspace/', views.WorkspaceView.as_view(), name='workspace-view'),
    path('fileuploadpractice/', views.model_form_upload, name='model-form-upload'),
    path('bupload/', views.UploadToBytesView.as_view(), name='byte-upload')
    # if I want to go the pattern-matching url route for working with a specific book, something like this?
    # path('workspace/<int:pk>', views.workspace, name='workspacetext')
]

