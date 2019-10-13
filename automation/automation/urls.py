"""automation URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from web import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 登陆 退出
    url(r'^login/', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),

    # 默认页面
    url(r'^index/', views.index, name='index'),

    # 用户
    url(r'^user/', views.user, name='user'),
    url(r'^useradd/', views.useradd, name='useradd'),
    url(r'^useredit/(\d+)', views.edit, name='useredit'),
    url(r'^userdel/(\d+)', views.userdel, name='userdel'),

    # 主机
    url(r'^host/', views.host, name='host'),
    url(r'^hostadd/', views.hostadd, name='hostadd'),
    url(r'^hostedit/(\d+)', views.hostedit, name='hostedit'),
    url(r'^hostdel/(\d+)', views.hostdel, name='hostdel'),

    # 初始化任务
    url(r'^init/', views.init, name='init'),
    url(r'^initadd/', views.initadd, name='initadd'),
    url(r'^initedit/(\d+)', views.initedit, name='initedit'),
    url(r'^initdel/(\d+)', views.initdel, name='initdel'),

    # 初始化主机
    url(r'^inithost/', views.inithost, name='inithost'),
    url(r'^initlog/(.*)', views.initlog, name='initlog'),

    # 项目
    url(r'^showproject/', views.project, name='showproject'),
    url(r'^projectadd/', views.projectadd, name='projectadd'),
    url(r'^projectedit/(\d+)', views.projectedit, name='projectedit'),
    url(r'^projectdel/(\d+)', views.projectdel, name='projectdel'),
    url(r'^projectinfo/(.*)', views.projectinfo, name='projectinfo'),

    # 命令下发
    url(r'^showissuance/', views.showissuance, name='showissuance'),
    url(r'^codeissuance/', views.codeissuance, name='codeissuance'),

    # 定时任务
    url(r'^showcron/', views.showcron, name='showcron'),
    url(r'^cronadd/',views.cronadd,name='cronadd'),
    url(r'^cronedit/(\d+)',views.cronedit,name='cronedit'),

    # 发布
    url(r'^showpublish/',views.showpublish,name='showpublish'),
    # 文件上传
    url(r'^createfile/',views.createfile,name='createfile'),
    # git添加
    url(r'^creategit/',views.creategit,name='creategit'),
    # TODO 发布的ansible动作未完成，showpublish的js动作未完成
]

