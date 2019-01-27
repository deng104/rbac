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
from django.conf.urls import url,include
from django.contrib import admin
from rbvc import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login, name='login'),
    url(r'logout/$', views.logout, name='logout'),
    url(r'^', include('web.urls', namespace='web')),
    # 角色管理
    url(r'^role_list/$', views.role_list, name='role_list'),
    url(r'^role_add/$', views.op_role, name='role_add'),
    url(r'^role_edit/(\d+)/$', views.op_role, name='role_edit'),
    url(r'^role_del/(\d+)/$', views.role_del, name='role_del'),
    # 菜单管理
    url(r'^menu_list/$', views.menu_list, name='menu_list'),
    url(r'^menu_add/$', views.op_menu, name='menu_add'),
    url(r'^menu_edit/(\d+)/$', views.op_menu, name='menu_edit'),
    url(r'^menu_del/(\d+)/$', views.menu_del, name='menu_del'),
    # 权限管理
    url(r'^permission_add/$', views.op_permission, name='permission_add'),
    url(r'^permission_edit/(\d+)/$', views.op_permission, name='permission_edit'),
    url(r'^permission_del/(\d+)/$', views.permission_del, name='permission_del'),
    # 权限批量录入
    url(r'^permission_entry/$', views.permission_entry, name='permission_entry'),
    # 批量权限更新
    url(r'^permission_update/$', views.permission_update, name='permission_update'),
]
