from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from rbac.models import *
from rbac.forms.permissions import PermissionModelForm
from django.urls import reverse


class PermissionAddView(View):
    def get(self,request):
        form = PermissionModelForm()
        return render(request,'rbac/permission_add.html',{'form':form})

    def post(self,request):
        form=PermissionModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:menus_list'))
        return render(request,'rbac/permission_add.html',{'form':form})

class PermissionEditView(View):

    def get(self,request,pid):
        permission_obj=Permission.objects.filter(id=pid).first()
        if not permission_obj:
            return HttpResponse('该权限不存在')
        form=PermissionModelForm(instance=permission_obj)
        return render(request,'rbac/permission_edit.html',{'form':form})

    def post(self,request,pid):
        permission_obj=Permission.objects.filter(id=pid).first()
        form=PermissionModelForm(data=request.POST,instance=permission_obj)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:menus_list'))
        return render(request, 'rbac/permission_edit.html', {'form': form})

class PermissionDelView(View):

    def  get(self,request,pid):
        Permission.objects.filter(id=pid).first().delete()
        return redirect(reverse('rbac:menus_list'))