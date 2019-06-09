from stark.service.base_stark import BaseStark
from crm.permissions.permissios import Permissions

class WorkShopStark(Permissions,BaseStark):

    list_display = ['id','name']

    search_list = ['name']




