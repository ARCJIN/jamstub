"""arc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app1 import views
from django.urls import re_path as url
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse




urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.customer_login , name = "customer_login") ,
    url(r'home', views.home , name = "home") ,
    url(r'customer_signup', views.customer_signup , name = "customer_signup") ,
    url(r'register', views.register , name = "register") ,
    url(r'baseintro', views.baseintro , name = "baseintro") ,
    url(r'profile', views.profile , name = "profile") ,
    url(r'addpost', views.addpost , name = "addpost") ,
    url(r'getcode', views.getcode , name = "getcode") ,
    url(r'discover', views.discover , name = "discover") ,
    url(r'request', views.req , name = "request") ,
    url(r'reqdetail/(?P<pk>\d+)' , views.reqdetail , name = 'reqdetail'),
    url(r'customerdetail/(?P<pk>\d+)' , views.customerdetail , name = 'customerdetail'),
    url(r'postdetail/(?P<pk>\d+)' , views.postdetail , name = 'postdetail'),
    url(r'list/(?P<pk>\d+)' , views.list , name = 'list'),
    url(r'editpost/(?P<pk>\d+)' , views.editpost , name = 'editpost'),
    url(r'commentbox/(?P<pk>\d+)' , views.commentbox , name = 'commentbox'),
    url(r'update' , views.update , name = 'update'),
    url(r'addtag' , views.tagadd , name = 'tagadd'),
    url(r'^searchcode/' , views.searchcode , name = 'searchcode'),
    url(r'delete/(?P<pk>\d+)' , views.delete , name = 'delete'),
    url(r'logout', views.logout , name = "logout") ,
    url(r'safe', views.safe , name = "safe") ,
    url(r'forgotpassword', views.forgotpassword , name = "forgotpassword") ,
]



if settings.DEBUG :
    urlpatterns += static(settings.STATIC_URL , document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)
