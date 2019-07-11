from app01 import models

def privileges(request, user_obj):
    permissions = models.Permission.objects.filter(role__userinfo__username=user_obj.username).values('pk','name','url','menu_id','menu__name','menu__id','pid').distinct()

    #修改数据结构
    permission_list = []
    # permission_menu_list = []
    permission_menu_dict = {}
    for item in permissions:
        # 获取全部权限数据
        permission_list.append({'pk':item['pk'],'url':item['url'],'pid':item['pid'],'name':item['name']})
        if item['menu_id']:
            # 获取菜单数据(包含1，2级)
            if item['menu_id'] in permission_menu_dict:
                permission_menu_dict[item['menu__id']]['children'].append({
                        'pk':item['pk'],
                        'name':item['name'],
                        'url':item['url'],
                    })
            else:
                permission_menu_dict[item['menu__id']] = {
                    'name':item['menu__name'],
                    'children':[{
                        'pk':item['pk'],
                        'name':item['name'],
                        'url':item['url'],
                    }],
                }
            # permission_menu_list.append({
            #     'name':item.name,
            #     'url':item.url,
            # })

    print(permission_menu_dict)
    print(permission_list)
    # 往session中注入全部的权限数据
    request.session['permission_list'] = permission_list
    # 往session中注入菜单数据
    request.session['permission_menu_dict'] = permission_menu_dict

