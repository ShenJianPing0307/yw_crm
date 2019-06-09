from stark.service.base_stark import BaseStark
from crm import models
from django import forms
from django.urls import re_path
from django.shortcuts import HttpResponse
from django.utils.safestring import mark_safe
from crm.permissions.permissios import Permissions

class PersonaleConsultantRecordModelForm(forms.ModelForm):

    class Meta:
        model=models.ConsultantRecord
        exclude=['consultant','customer']

class AllConsultantRecordModelForm(forms.ModelForm):

    class Meta:
        model=models.ConsultantRecord
        fields='__all__'

class PersonalConsultantRecordStark(Permissions,BaseStark):

    model_form_class = PersonaleConsultantRecordModelForm

    def display_edit_del(self, row=None, header_body=False, *args, **kwargs):
        """
        返回表格中不是数据库中的信息，自定制数据库之外的信息
        :param row:
        :param header_body:
        :return:
        """
        customer_id = kwargs.get('customer_id')
        if not header_body:
            return '操作'
        tpl = """
        <a href="%s"> <i class="fa fa-edit" aria-hidden="true"></i></a>|
        <a href="%s"> <i class="fa fa-trash-o" aria-hidden="true"></i></a>
        """ % ( self.reverse_edit_url(pk=row.pk, customer_id=customer_id),
            self.reverse_del_url(pk=row.pk, customer_id=customer_id))
        return mark_safe(tpl)

    list_display = ['customer', 'consultant', 'date', 'content',display_edit_del ]

    def get_list_display(self):
        val=super().get_list_display()
        val.remove(BaseStark.display_del)
        val.remove(BaseStark.display_edit)
        return val

    def get_urls(self):
        urlpatterns = [
            re_path('constant/list/(?P<customer_id>\d+)/$', self.wrapper(self.changelist_view), name=self.get_list_url_name ),
            re_path('add/(?P<customer_id>\d+)/$', self.wrapper(self.add_view), name=self.get_add_url_name),
            re_path('(?P<customer_id>\d+)/(?P<pk>\d+)/change/$', self.wrapper(self.change_view), name=self.get_edit_url_name),
            re_path('(?P<customer_id>\d+)/(?P<pk>\d+)/del/$', self.wrapper(self.del_view), name=self.get_del_url_name),
        ]
        extra_urls = self.extra_urls()

        if extra_urls:
            urlpatterns.extend(extra_urls)

        return urlpatterns

    def get_queryset(self,request,*args,**kwargs):

        return self.model_class.objects.all()




    def save(self,request,form,is_modify,*args,**kwargs):
        customer_id = kwargs.get('customer_id')
        current_user_id=5
        object_exists = models.Customer.objects.filter(id=customer_id,
                                                       consultant_id=current_user_id).exists()
        if not object_exists:
            return HttpResponse('非法操作')

        if not is_modify:
            form.instance.customer_id = customer_id
            form.instance.consultant_id = current_user_id

        form.save()



