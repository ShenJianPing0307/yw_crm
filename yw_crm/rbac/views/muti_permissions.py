from rbac.forms.muti_permissions import MultiPermissionForm
from django.shortcuts import render
from django.forms import formset_factory,modelform_factory
from rbac import models
from rbac.services.routes import *


def multi_permissions(request):
    """
    批量操作权限
    :param request:
    :return:
    """
    post_type = request.GET.get('type')

    MultiPermissionFormSet = formset_factory(MultiPermissionForm,extra=0)

    generate_formset = None
    update_formset = None

    if request.method == 'POST' and post_type == 'generate':
        print('request.post',request.POST)
        formset = MultiPermissionFormSet(request.POST)
        if formset.is_valid():
            for row_dict in formset.cleaned_data:
                models.Permission.objects.create(**row_dict)
        else:
            generate_formset = formset

    if request.method == 'POST' and post_type == 'update':
        formset = MultiPermissionFormSet(request.POST)
        if formset.is_valid():
            for row_dict in formset.cleaned_data:
                permission_id = row_dict.pop('id')
                models.Permission.objects.filter(id=permission_id).update(**row_dict)
        else:
            update_formset = formset

    # 1.1 去数据库中获取所有权限
    # [{},{}]
    permissions = models.Permission.objects.all().values('id', 'title', 'url', 'name', 'menu_id', 'parent_id')
    # {'rbac:menu_list':{},'rbac:menu_add':{..}}
    permisssion_dict = OrderedDict()
    for per in permissions:
        permisssion_dict[per['name']] = per

    # 1.2 数据库中有的所有权限name的集合
    permission_name_set = set(permisssion_dict.keys())


    # 2.1 获取路由系统中所有的URL
    # {'rbac:menu_list':{'url':.... },,,}
    router_dict = get_all_url_dict(ignore_namespace_list=['admin',])

    for row in permissions:
        name = row['name']
        if name in router_dict:
            router_dict[name].update(row)

    # 2.2 路由系统中的所有权限name的集合
    router_name_set = set(router_dict.keys())

    # 需要新建：数据库无、路由有
    if not generate_formset:
        generate_name_list=router_name_set-permission_name_set
        generate_formset = MultiPermissionFormSet(
            initial=[row for name, row in router_dict.items() if name in generate_name_list]
        )

    # 需要删除：数据库有、路由无
    destroy_name_list = permission_name_set - router_name_set
    destroy_formset = [row for name, row in permisssion_dict.items() if name in destroy_name_list]

    # 需要更新：数据库有、路由有
    if not update_formset:
        update_name_list = permission_name_set.intersection(router_name_set)
        update_formset = MultiPermissionFormSet(
            initial=[row for name, row in router_dict.items() if name in update_name_list]
        )

    return render(
        request,
        'rbac/multi_permissions.html',
        {
            'destroy_formset': destroy_formset,
            'update_formset': update_formset,
            'generate_formset': generate_formset,
        }
    )







