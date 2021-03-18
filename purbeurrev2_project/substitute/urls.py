from django.urls import path, re_path

from . import views

app_name = 'substitute'

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^signup/', views.signup, name='signup'),
    re_path(r'^logout_request/', views.logout_request, name='logout'),
]
