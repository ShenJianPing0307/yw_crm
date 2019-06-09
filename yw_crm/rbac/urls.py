"""luffy_permission URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import re_path
from rbac.views.roles import *
from rbac.views.menus import *
from rbac.views.permissions import *
from rbac.views.muti_permissions import *
from rbac.views.distribute_permissions import  *


app_name='[rbac]'
urlpatterns = [
    re_path(r'^roles/list/$', RoleView.as_view(),name='roles_list'),
    re_path(r'^roles/add/$', RoleAddView.as_view(), name='roles_add'),
    re_path(r'^roles/edit/(?P<rid>\d+)/$', RoleEditView.as_view(), name='roles_edit'),
    re_path(r'^roles/dell/(?P<rid>\d+)/$', RoleDelView.as_view(), name='roles_del'),

    re_path(r'^menus/list/$', MenuView.as_view(), name='menus_list'),
    re_path(r'^menus/add/$', MenuAddView.as_view(), name='menus_add'),
    re_path(r'^menus/edit/(?P<mid>\d+)/$', MenuEditView.as_view(), name='menus_edit'),
    re_path(r'^menus/dell/(?P<mid>\d+)/$', MenuDelView.as_view(), name='menus_del'),

    re_path(r'^permissions/add/$', PermissionAddView.as_view(), name='permissions_add'),
    re_path(r'^permissions/edit/(?P<pid>\d+)/$', PermissionEditView.as_view(), name='permissions_edit'),
    re_path(r'^permissions/dell/(?P<pid>\d+)/$', PermissionDelView.as_view(), name='permissions_del'),
    re_path(r'^multi/permissions/$', multi_permissions, name='multi_permissions'),

    re_path(r'^distribute/permissions/$', distribute_permissions, name='distribute_permissions'),

]
