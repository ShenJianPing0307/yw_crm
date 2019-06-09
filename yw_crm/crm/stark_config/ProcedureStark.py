from stark.service.base_stark import BaseStark,BaseModelForm
from django import forms
from crm import models
from stark.service.base_stark import Option
from django.urls import re_path
from django.forms import modelformset_factory
from django.shortcuts import render
from crm.permissions.permissios import Permissions


class ProcedureModelForm(BaseModelForm):
    class  Meta:
        model=models.Procedure
        exclude=['audit_status']


class ProcedureStark(Permissions,BaseStark):

    def display_audit_product(self, row=None, header_body=False,*args,**kwargs):
        if not header_body:
            return '产品审核状态'
        audit_obj=row.productaudit_set.first()
        if audit_obj:
            return getattr(audit_obj,'status')
        return '未审核'

    list_display = ['order','workshop','name','status','parent','reason','start','end','scedule','product_status',display_audit_product]

    model_form_class = ProcedureModelForm

    list_filter = [
        Option('order',),
        Option('name', value_func=lambda x:x.name)
    ]

    search_list = ['name']

    def get_list_display(self):
        val=super().get_list_display()
        # val.remove(BaseStark.display_del)
        return val

    def get_queryset(self,request,*args,**kwargs):
        queryset=self.model_class.objects.filter(order__check_date__isnull=False)
        return queryset

    def get_add_btn(self,request,*args,**kwargs):
        has_product_parameter=models.ProductParameter.objects.all()
        if not has_product_parameter:
            return None
        return super().get_add_btn(request,*args,**kwargs)







