from django.conf import settings

from django.conf import settings


# def init_permission(request,user):
#     """
#     权限和菜单信息初始化，以后使用时，需要在登陆成功后调用该方法将权限和菜单信息放入session
#     :param request:
#     :param user:
#     :return:
#     """
#
#     # 3. 获取用户信息和权限信息写入session
#     permission_queryset = user.roles.filter(permissions__url__isnull=False).values('permissions__id',
#                                                                                    'permissions__url',
#                                                                                    'permissions__title',
#                                                                                    'permissions__name',
#                                                                                    'permissions__parent_id',
#                                                                                    'permissions__parent__name',
#                                                                                    'permissions__menu_id',
#                                                                                    'permissions__menu__title',
#                                                                                    'permissions__menu__icon',
#                                                                                   ).distinct()
#
#
#     menu_dict = {} # 菜单+能成为菜单的权限，用于做菜单显示
#     permission_dict = {} # 所有权限，用于做权限校验
#
#     for row in permission_queryset:
#         permission_dict[row['permissions__name']] = {
#             'id':row['permissions__id'],
#             'url': row['permissions__url'],
#             'title': row['permissions__title'],
#             'pid':row['permissions__parent_id'],
#             'pname':row['permissions__parent__name'],
#         }
#
#
#         menu_id = row.get('permissions__menu_id')
#         if not menu_id:
#             continue
#
#         if menu_id not in menu_dict:
#             menu_dict[menu_id] = {
#                 'title': row['permissions__menu__title'],
#                 'icon': row['permissions__menu__icon'],
#                 'children': [
#                     {'id':row['permissions__id'],'title': row['permissions__title'], 'url': row['permissions__url']}
#                 ]
#             }
#         else:
#             menu_dict[menu_id]['children'].append({'id':row['permissions__id'],'title': row['permissions__title'], 'url': row['permissions__url']})
#
#     print(permission_dict)
#
#     request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
#     request.session[settings.MENU_SESSION_KEY] = menu_dict

class InitPermission(object):

    def __init__(self,request,user):
        """
        :param request: 传入request对象
        :param user: 传入用户对象
        """

        self.request=request
        self.user=user
        self.menu_dict={}
        self.permissions_dict={}

    def init_data(self):
        """
        从数据库中获取权限信息以及用户信息
        :return:
        """
        self.permissions_queryset=self.user.roles.filter(permissions__url__isnull=False).values(
            'permissions__id',
            'permissions__url',
            'permissions__title',
            'permissions__name',
            'permissions__parent_id',
            'permissions__parent__name',
            'permissions__menu_id',
            'permissions__menu__title',
            'permissions__menu__icon',
        ).distinct()
        return self.permissions_queryset

    def init_permissions_dict(self):
        """
        构建权限列表,并且存入session
        self.permissions_dict={
            'customer_list':{'id':1,'url':'/customer/list/','title':'客户列表','pid':'父权限id'}
            ...
        }
        :return:
        """
        for row in self.init_data():
            self.permissions_dict[row['permissions__name']]={
            'id':row['permissions__id'],
            'url': row['permissions__url'],
            'title': row['permissions__title'],
            'pid':row['permissions__parent_id'],
            'pname':row['permissions__parent__name'],
            }
        self.request.session[settings.PERMISSION_SESSION_KEY]=self.permissions_dict

    def init_menu_dict(self):
        """
        构建菜单字典并且存入session,之所以构建字典，可以通过键值进行排序
        self.menu_dict={
        1:{
        title:'客户管理',icon:'fa fa-coffe',children:[
        {'id':1,'url':'/customer/list/','title':'客户列表'}
        ...
        ]
        }
        }
        :return:
        """
        for row in self.init_data():
            menu_id=row['permissions__menu_id']
            if not menu_id:
                continue
            if menu_id not in self.menu_dict:
                self.menu_dict[menu_id]={
                'title': row['permissions__menu__title'],
                'icon': row['permissions__menu__icon'],
                'children': [
                    {'id':row['permissions__id'],'title': row['permissions__title'], 'url': row['permissions__url']}
                ]
                }
            else:
                self.menu_dict[menu_id]['children'].append(
                    {'id': row['permissions__id'], 'title': row['permissions__title'], 'url': row['permissions__url']}
                )
        self.request.session[settings.MENU_SESSION_KEY] = self.menu_dict








