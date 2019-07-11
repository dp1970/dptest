import re
from django.shortcuts import HttpResponse,render,redirect
from django.utils.deprecation import MiddlewareMixin

class PermissionMiddleWare(MiddlewareMixin):

    def process_request(self,request):
        #白名单放行
        for i in ['/regiest/','/login/','/admin/.*','/code/']:
            ret = re.search(i,request.path)
            if ret:
                return None

        #登录认证
        print(request.session)
        user = request.session.get('user')
        if not user:
            return redirect('login')

        request.menu_breadcrumb = [
            {'name':'首页','url':'javascript:void(0);'}
        ]

        #权限认证
        print(request.path)
        for item in request.session['permission_list']:
            reg = '^%s$'%item['url']
            ret = re.search(reg,request.path)
            if ret:
                request.show_id = item['pid']
                return None
        else:
            return HttpResponse('不好意思,权限不够!!无权访问!')





