from django.urls import path, re_path

from . import views

app_name = 'substitute'

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^signup/$', views.signup, name='signup'),
    re_path(r'^logout_request/$', views.logout_request, name='logout'),
    re_path(r'^myaccount/$', views.my_account, name='myaccount'),
    re_path(r'^results/(?P<query>[\w\d+]*)/$', views.results, name='results'),
    re_path(r'^detail/(?P<product_id>\d+)/$', views.detail, name='detail'),
    re_path(r'^togglefav/$', views.togglefav, name='togglefav'),
    re_path(r'^favorites/$', views.favorites, name='favorites'),
    re_path(r'^legal_notice/$', views.legal_notice, name='legal_notice'),
]
