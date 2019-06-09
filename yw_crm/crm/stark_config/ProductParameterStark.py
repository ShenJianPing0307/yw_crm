from stark.service.base_stark import BaseStark
from django import forms
from crm import models
from crm.permissions.permissios import Permissions


class ProductParameterStark(Permissions,BaseStark):
    """
    工艺
    """
    def display_product_parameters(self, row=None, header_body=False, *args, **kwargs): #跨表取值
        if not header_body:
            return '产品参数'
        val=getattr(row.product,'paramters')
        return val

    list_display = ['id','workshop','product',display_product_parameters,'technology','quality']



    def get_add_btn(self,request,*args,**kwargs):
        has_product=models.Product.objects.all()
        if not has_product:
            return None
        return super().get_add_btn(request,*args,**kwargs)






