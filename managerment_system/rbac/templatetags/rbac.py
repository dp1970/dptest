from django import template

register = template.Library()


import re


@register.inclusion_tag('menu.html')
def menu(request):
    # menu_list = request.session.get('permission_menu_list')
    # for i in menu_list:
    #     if re.match('^{}$'.format(i['url']),request.path):
    #         i['class'] = 'active'
    #         break

    # return {'menu_list':menu_list}

    menu_dict = request.session.get('permission_menu_dict')

    for item in menu_dict.values():
        item['class'] = ''

        for child in item['children']:
            # if re.match('^{}$'.format(child['url']),request.path):
            if request.show_id == child['pk']:
                item['class'] = 'active'
                # child['class'] = 'active'
                break

    return {'menu_dict': menu_dict}
