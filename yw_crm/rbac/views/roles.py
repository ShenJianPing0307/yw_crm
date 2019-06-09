from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from rbac.models import *
from rbac.forms.roles import RoleModelForm
from django.urls import reverse

# Create your views here.

class RoleView(View):
    def get(self,request):
        role_queryset=Role.objects.all()
        return render(request,'rbac/role_list.html',{'role_queryset':role_queryset})

class RoleAddView(View):
    def get(self,request):
        form = RoleModelForm()
        return render(request,'rbac/role_add.html',{'form':form})

    def post(self,request):
        form=RoleModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:roles_list'))
        return render(request,'rbac/role_add.html',{'form':form})

class RoleEditView(View):

    def get(self,request,rid):
        role_obj=Role.objects.filter(id=rid).first()
        if not role_obj:
            return HttpResponse('该角色不存在')
        form=RoleModelForm(instance=role_obj)
        return render(request,'rbac/role_edit.html',{'form':form})

    def post(self,request,rid):
        role_obj=Role.objects.filter(id=rid).first()
        form=RoleModelForm(data=request.POST,instance=role_obj)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:roles_list'))
        return render(request, 'rbac/role_edit.html', {'form': form})

class RoleDelView(View):

    def  get(self,request,rid):
        Role.objects.filter(id=rid).first().delete()
        return redirect(reverse('rbac:roles_list'))


