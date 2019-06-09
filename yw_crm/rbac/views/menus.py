from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from rbac.models import *
from rbac.forms.menus import MenuModelForm
from django.urls import reverse

class MenuView(View):
    def get(self,request):
        menu_queryset=Menu.objects.all()

        pid=request.GET.get('pid')

        if pid:
            root_permission_queryset = Permission.objects.filter(menu_id=pid).values('id', 'title', 'url', 'name', 'parent_id','menu__title')
        else:
            root_permission_queryset = Permission.objects.filter(menu_id__isnull=False).values('id', 'title', 'url', 'name', 'parent_id','menu__title')
        # print('permission_queryset',root_permission_queryset)

        all_root_permission_queryset=Permission.objects.all().values('id', 'title', 'url', 'name', 'parent_id')
        root_permission_dict={}
        for row in root_permission_queryset:
            if not row['parent_id']:
                root_permission_dict[row['id']]={
                    'id':row['id'],
                    'title':row['title'],
                    'name':row['name'],
                    'url':row['url'],
                    'menu_title':row['menu__title'],
                    'children':[]
                }
        for row in all_root_permission_queryset:
            parent_id=row['parent_id']
            if parent_id in root_permission_dict:
                root_permission_dict[parent_id]['children'].append(
                    {
                        'id':row['id'],
                        'title':row['title'],
                        'name':row['name'],
                        'url':row['url']
                    }
                )
        print(root_permission_dict)

        return render(request,'rbac/menu_list.html',{'menu_queryset':menu_queryset,
                                                     'root_permission_dict':root_permission_dict,
                                                     'pid':pid

                                                     })

class MenuAddView(View):
    def get(self,request):
        form = MenuModelForm()
        return render(request,'rbac/menu_add.html',{'form':form})

    def post(self,request):
        form=MenuModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:menus_list'))
        return render(request,'rbac/menu_add.html',{'form':form})

class MenuEditView(View):

    def get(self,request,mid):
        menu_obj=Menu.objects.filter(id=mid).first()
        if not menu_obj:
            return HttpResponse('该菜单不存在')
        form=MenuModelForm(instance=menu_obj)
        return render(request,'rbac/menu_edit.html',{'form':form})

    def post(self,request,mid):
        menu_obj=Menu.objects.filter(id=mid).first()
        form=MenuModelForm(data=request.POST,instance=menu_obj)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:menus_list'))
        return render(request, 'rbac/menu_edit.html', {'form': form})

class MenuDelView(View):

    def  get(self,request,mid):
        Menu.objects.filter(id=mid).first().delete()
        return redirect(reverse('rbac:menus_list'))