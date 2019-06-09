from django.shortcuts import render,HttpResponse
from rbac import models
from django.utils.module_loading import import_string
from django.conf import settings


def distribute_permissions(request):
    # uid=request.GET.get('uid')
    # rid=request.GET.get('rid')
    #
    # user_class=import_string(settings.USER_MODEL_PATH) #获取用户表
    #
    # user_list=user_class.objects.all() #获取所有的用户
    # role_list=models.Role.objects.all() #获取所有的角色
    #
    # #############################为用户分配角色#################
    # if request.method=='POST' and request.POST.get('postType') == 'role':
    #     user = user_class.objects.filter(id=uid).first()
    #     if not user:
    #         return HttpResponse('该用户不存在')
    #     role_id_list=request.POST.getlist('roles')
    #     print(role_id_list)
    #     user.roles.set(role_id_list)#为该用户分配角色
    #
    # if request.method=='POST' and request.POST.get('postType')=='permission' and rid:
    #     role=models.Role.objects.filter(id=rid).first()
    #     if not role:
    #         return HttpResponse('该角色不存在')
    #     print(request.POST.getlist('permissions'))
    #     role.permissions.set(request.POST.getlist('permissions'))
    #
    # # user_has_role_list=user_class.objects.filter(id=uid).first().roles.all()
    # # ############################## 角色信息 ##########################
    # # 当前用户拥有的角色
    # user_has_roles = user_class.objects.filter(id=uid).values('id', 'roles')
    # print('role_id',user_has_roles)
    # user_has_roles_dict = {item['roles']: None for item in user_has_roles}
    # print(user_has_roles_dict)
    # """
    # role_id <QuerySet [{'id': 1, 'roles': 2}]>
    # {2: None}
    # """
    # #################################权限信息###########################
    # #####判断角色拥有的所有的权限，前端需要判断
    # if rid:
    #     role_has_permission=models.Role.objects.filter(id=rid,permissions__isnull=False).values('id','permissions')
    # elif uid and not rid:
    #     user=user_class.objects.filter(id=uid).first()
    #     if not user:
    #         return HttpResponse('该用户不存在')
    #     role_has_permission=user.roles.filter(permissions__isnull=False).values('id','permissions')
    # else:
    #     role_has_permission=[]
    # role_has_permission_dict={item['permissions']:None for item in role_has_permission}#{'1':None} 以权限id为键，值为None
    #
    # ####菜单信息
    # menu_queryset= models.Menu.objects.values('id','title') #取出菜单id，title [{'id':1,'title':'客户管理'},]
    #
    # all_menu_list=[]
    # menu_dict={}
    # for per_menu in menu_queryset:
    #     per_menu['children']=[] #{'id':1,'title':'客户管理','children':[]} #children是为了放挂载菜单上的权限
    #     menu_dict[per_menu['id']]=per_menu#menu_dict={1:{'id':1,'title':'客户管理','children':[]}}
    #     all_menu_list.append(per_menu)#[{{'id':1,'title':'客户管理','children':[]}},]
    #
    # other={'id':None,'title':'其它','children':[]} #处理其他像登陆，注销这样的权限
    # menu_dict[None]=other
    # all_menu_list.append(other)
    #
    # #####挂载到菜单上的权限
    # permission_dict={}
    # root_permission=models.Permission.objects.filter(menu__isnull=False).values('id','title','menu_id')
    # for per_permission in root_permission:#[{'id':1,'title':'客户列表'，'menu_id':1}]
    #     per_permission['children']=[]#{'id':1,'title':'客户列表'，'menu_id':1,'children':[]}
    #     permission_dict[per_permission['id']]=per_permission#{1:{'id':1,'title':'客户列表'，'menu_id':1,'children':[]}}
    #     menu_dict[per_permission['menu_id']]['children'].append(per_permission)#menu_dict={1:{'id':1,'title':'客户管理','children':[{'id':1,'title':'客户列表'，'menu_id':1,'children':[]},]}}
    #
    # ######未挂载到菜单的权限 像增加客户这样的权限 菜单为空
    # node_permission=models.Permission.objects.filter(menu__isnull=True).values('id','title','parent_id')
    # for per_permission in node_permission:#[{'id':2,'title':增加客户,'parent_id':1},]
    #     permission_dict[per_permission['parent_id']]['children'].append(per_permission)
    #
    #     if not per_permission['parent_id']: #如果是其它菜单中的权限直接加入，其它是菜单
    #         menu_dict[None]['children'].append(per_permission)
    #         continue

    user_id = request.GET.get('uid')
    # 业务中的用户表 "app01.models.UserInfo""
    user_model_class = import_string(settings.USER_MODEL_PATH)

    user_object = user_model_class.objects.filter(id=user_id).first()
    if not user_object:
        user_id = None

    role_id = request.GET.get('rid')
    role_object = models.Role.objects.filter(id=role_id).first()
    if not role_object:
        role_id = None

    if request.method == 'POST' and request.POST.get('postType') == 'role':
        role_id_list = request.POST.getlist('roles')
        # 用户和角色关系添加到第三张表（关系表）
        if not user_object:
            return HttpResponse('请选择用户，然后再分配角色！')
        user_object.roles.set(role_id_list)

    if request.method == 'POST' and request.POST.get('postType') == 'permission':
        permission_id_list = request.POST.getlist('permissions')
        if not role_object:
            return HttpResponse('请选择角色，然后再分配权限！')
        role_object.permissions.set(permission_id_list)

    # 获取当前用户拥有的所有角色
    if user_id:
        user_has_roles = user_object.roles.all()
    else:
        user_has_roles = []

    user_has_roles_dict = {item.id: None for item in user_has_roles}

    # 获取当前用户用户用户的所有权限

    # 如果选中的角色，优先显示选中角色所拥有的权限
    # 如果没有选择角色，才显示用户所拥有的权限
    if role_object:  # 选择了角色
        user_has_permissions = role_object.permissions.all()
        user_has_permissions_dict = {item.id: None for item in user_has_permissions}

    elif user_object:  # 未选择角色，但选择了用户
        user_has_permissions = user_object.roles.filter(permissions__id__isnull=False).values('id',
                                                                                              'permissions').distinct()
        user_has_permissions_dict = {item['permissions']: None for item in user_has_permissions}
    else:
        user_has_permissions_dict = {}

    all_user_list = user_model_class.objects.all()

    all_role_list = models.Role.objects.all()

    menu_permission_list = []

    # 所有的菜单（一级菜单）
    all_menu_list = models.Menu.objects.values('id', 'title')
    """
    [
        {id:1,title:菜单1,children:[{id:1,title:x1, menu_id:1,'children':[{id:11,title:x2,pid:1},] },{id:2,title:x1, menu_id:1 },]},
        {id:2,title:菜单2,children:[{id:3,title:x1, menu_id:2 },{id:5,title:x1, menu_id:2 },]},
        {id:3,title:菜单3,children:[{id:4,title:x1, menu_id:3 },]},
    ]
    """
    all_menu_dict = {}
    """
       {
           1:{id:1,title:菜单1,children:[{id:1,title:x1, menu_id:1,children:[{id:11,title:x2,pid:1},] },{id:2,title:x1, menu_id:1,children:[] },]},
           2:{id:2,title:菜单2,children:[{id:3,title:x1, menu_id:2,children:[] },{id:5,title:x1, menu_id:2,children:[] },]},
           3:{id:3,title:菜单3,children:[{id:4,title:x1, menu_id:3,children:[] },]},
       }
       """
    for item in all_menu_list:
        item['children'] = []
        all_menu_dict[item['id']] = item

    # 所有二级菜单
    all_second_menu_list = models.Permission.objects.filter(menu__isnull=False).values('id', 'title', 'menu_id')

    """
    [
        {id:1,title:x1, menu_id:1,children:[{id:11,title:x2,pid:1},] },   
        {id:2,title:x1, menu_id:1,children:[] },
        {id:3,title:x1, menu_id:2,children:[] },
        {id:4,title:x1, menu_id:3,children:[] },
        {id:5,title:x1, menu_id:2,children:[] },
    ]
    """
    all_second_menu_dict = {}
    """
        {
            1:{id:1,title:x1, menu_id:1,children:[{id:11,title:x2,pid:1},] },   
            2:{id:2,title:x1, menu_id:1,children:[] },
            3:{id:3,title:x1, menu_id:2,children:[] },
            4:{id:4,title:x1, menu_id:3,children:[] },
            5:{id:5,title:x1, menu_id:2,children:[] },
        }
        """
    for row in all_second_menu_list:
        row['children'] = []
        all_second_menu_dict[row['id']] = row

        menu_id = row['menu_id']
        all_menu_dict[menu_id]['children'].append(row)

    # 所有三级菜单（不能做菜单的权限）
    all_permission_list = models.Permission.objects.filter(menu__isnull=True).values('id', 'title', 'parent_id')
    """
    [
        {id:11,title:x2,pid:1},
        {id:12,title:x2,pid:1},
        {id:13,title:x2,pid:2},
        {id:14,title:x2,pid:3},
        {id:15,title:x2,pid:4},
        {id:16,title:x2,pid:5},
    ]
    """
    for row in all_permission_list:
        pid = row['parent_id']
        if not pid:
            continue
        all_second_menu_dict[pid]['children'].append(row)

    """
    [
        {
            id:1,
            title:'业务管理'
            children:[
                {
                    'id':11, 
                    title:'账单列表',
                    children:[
                        {'id':12,title:'添加账单'}
                    ]
                },
                {'id':11, title:'客户列表'},
            ]
        },

    ]
    """

    return render(
        request,
        'rbac/distribute_permission.html',
        {
            'user_list': all_user_list,
            'role_list': all_role_list,
            'all_menu_list': all_menu_list,
            'uid': user_id,
            'rid': role_id,
            'user_has_roles_dict': user_has_roles_dict,
            'role_has_permission_dict': user_has_permissions_dict,
        }
    )




    # return render(request,'rbac/distribute_permission.html',{
    #     'user_list':user_list,
    #     'role_list':role_list,
    #     'uid':uid,
    #     'rid':rid,
    #     'user_has_roles_dict':user_has_roles_dict,
    #     'role_has_permission_dict':role_has_permission_dict,
    #     'all_menu_list':all_menu_list
    # })