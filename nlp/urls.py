from django.urls import path
from . import views
from django.contrib import admin
# what does this do?
from django.urls import include

urlpatterns = [
    # honestly I need to look up the pattern matching sometime, I'm confused by it
    path('', views.index, name='index'),
    # path('admin', admin.site.urls),
    path('post/new/', views.post_new, name='post_new'),
    path('upload', views.upload, name='upload'),
    path('accounts/', include('django.contrib.auth.urls'))
]

