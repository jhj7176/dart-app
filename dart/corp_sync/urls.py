from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve
from corp_sync import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
