"""managerment_system URL Configuration

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
from app01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 注册
    url(r'^regiest/',views.regiest,name='regiest'),
    # 登录
    url(r'^login/',views.login,name='login'),
    # 验证码图片
    url(r'^code/',views.code,name='code'),
    # 默认页面
    url(r'^index/',views.index,name='index'),
    # 退出
    url(r'^logout',views.logout,name='logout'),
    # 展示所有客户信息
    url(r'^customers/list/', views.customers, name='customers'),
    # 添加
    url(r'^add$', views.add, name='add'),
    # 删除跟进记录
    url(r'delfollow/(\d+)',views.delfollow,name='delfollow'),
    # 删除
    url(r'^delete/(\d+)', views.delete, name='delete'),
    # 编辑跟进记录
    url(r'editfollow/(\d+)',views.editfollow,name='editfollow'),
    # 编辑
    url(r'^edit/(\d+)', views.edit, name='edit'),
    # 私户信息展示
    url(r'^mycustomers/', views.mycustomers, name='mycustomers'),
    # 跟进记录
    url(r'^followrecord/$',views.followrecord,name='followrecord'),
    # 公共页面的查看记录详情
    url(r'^followrecord/(\d+)',views.followrecord,name='singlerecord'),
    # 添加跟进记录
    url(r'^addfollow/',views.addfollow,name='addfollow'),
    # 展示班级信息
    url(r'^showclass/',views.showclass,name='showclass'),
]
