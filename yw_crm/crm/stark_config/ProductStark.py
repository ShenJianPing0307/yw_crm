from stark.service.base_stark import BaseStark
from crm import models
from crm.permissions.permissios import Permissions


class ProductStark(Permissions,BaseStark):
    """
    项目部根据客户的需求，记录产品的参数
    """
    list_display = ['id','name','price','paramters']

    search_list = ['name',]

    def get_add_btn(self,request,*args,**kwargs):
        has_order_date=models.Order.objects.filter(check_date__isnull=False)
        if not has_order_date:
            return None