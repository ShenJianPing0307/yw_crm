from stark.service.base_stark import BaseStark,BaseModelForm
from django.forms import modelformset_factory
from crm import models
from django.urls import re_path
from django.shortcuts import render
from django import forms
import json
from crm.permissions.permissios import Permissions


class ProductAuditModelForm(BaseModelForm):
    class  Meta:
        model=models.ProductAudit
        exclude=['user']

class ProductProcedureModelForm(BaseModelForm):
    audit_date=forms.DateTimeField(required=False)
    class  Meta:
        model=models.Procedure
        fields="__all__"

class ProductAuditStark(Permissions,BaseStark):

    model_form_class = ProductAuditModelForm

    list_display = [BaseStark.display_checkbox,'procedure','user','status','reason','audit_date']

    action_list = [BaseStark.muti_editable_save]

    list_editable = ['user','status','reason','audit_date']

    def get_add_btn(self,request,*args,**kwargs):
        return None

    def get_urls(self):
        urlpatterns = [
            re_path('list/$', self.wrapper(self.changelist_view), name=self.get_list_url_name),
        ]
        extra_urls = self.extra_urls()

        if extra_urls:
            urlpatterns.extend(extra_urls)
        return urlpatterns







