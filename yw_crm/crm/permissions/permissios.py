from django.conf import settings
from stark.service.base_stark import BaseStark


class Permissions(object):

    def get_add_btn(self,request,*args,**kwargs):
        permission_dict = self.request.session[settings.PERMISSION_SESSION_KEY]
        name="%s:%s"%(self.site.namespace,self.get_add_url_name)
        if name in permission_dict:
            return super().get_add_btn(request,*args,**kwargs)

    def get_list_display(self):
        permission_dict = self.request.session[settings.PERMISSION_SESSION_KEY]
        val=super().get_list_display()
        edit_name="%s:%s"%(self.site.namespace,self.get_edit_url_name)
        del_name="%s:%s"%(self.site.namespace,self.get_del_url_name)
        if edit_name not in permission_dict:
            val.remove(BaseStark.display_edit)
        if del_name not in permission_dict:
            val.remove(BaseStark.display_del)
        return val

    # def display_has_permission(self,field):
    #     if hasattr(field, 'url_name'):
    #         url_name = field.url_name
    #         if url_name and url_name not in self.permission_dict:
    #             return False

