from django.template import Library
from django.conf import settings
from collections import OrderedDict

register=Library()

@register.inclusion_tag('rbac/menu.html')
def menu(request):
    #获取session中的菜单列表
    menu_dict=request.session.get(settings.MENU_SESSION_KEY)
    order_dict=OrderedDict()
    if menu_dict:
        for key in sorted(menu_dict): #按照菜单id升序对菜单进行排序
            order_dict[key]=menu_dict[key]
            menu_dict[key]['class']='hide'
            for child in menu_dict[key]['children']:
                if request.current_menu_id==child['id']:  #非菜单权限以及菜单权限默认展开
                    child['class']='active'
                    menu_dict[key]['class'] = ''
        return {"menu_dict":menu_dict}

@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    return {'breadcrumb_list':request.breadcrumb_list}

@register.filter()
def has_permission(request,url_name):
    permissions_dict=request.session.get(settings.PERMISSION_SESSION_KEY)
    if url_name in permissions_dict:
        return True
    else:
        return False
