"""testolwidget URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin

from .views import (
    show_alienactivity, edit_alienactivity, show_tree, edit_tree,
    edit_tree_custom, edit_capitals, show_countries, index
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^alienactivity/(?P<pk>\d+)/show$', show_alienactivity, name='show_alienactivity'),
    url(r'^alienactivity/(?P<pk>\d+)/edit$', edit_alienactivity, name='edit_alienactivity'),
    url(r'^tree/(?P<pk>\d+)/show$', show_tree, name='show_tree'),
    url(r'^tree/(?P<pk>\d+)/edit$', edit_tree, name='edit_tree'),
    url(r'^tree_custom/(?P<pk>\d+)/edit$', edit_tree_custom, name='edit_tree_custom'),
    url('^capitals/edit$', edit_capitals, name='edit_capitals'),
    url('^countries$', show_countries, name='show_countries'),
    url('^$', index, name='index'),
]
