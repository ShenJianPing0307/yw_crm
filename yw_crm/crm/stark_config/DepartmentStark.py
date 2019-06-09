from stark.service.base_stark import BaseStark

class DepartmentStark(BaseStark):

    list_display = ['id','name',]

    search_list = ['name']