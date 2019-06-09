from stark.service.base_stark import BaseStark,BaseModelForm
from crm import models
from django.urls import re_path
from crm.permissions.permissios import Permissions
from django.utils.safestring import mark_safe

class PaymentRecordModelForm(BaseModelForm):
       class Meta:
           model=models.PaymentRecord
           exclude=['confirm_date','confirm_user']

       def __init__(self,request,*args, **kwargs): #form中没有传入request对象
           super().__init__(request,*args, **kwargs)
           current_user_id = self.request.session['user_info']['id']
           customer=models.Customer.objects.filter(name=models.UserInfo.objects.filter(id=current_user_id).first().username).first()
           self.fields['order'].queryset = models.Order.objects.filter(customer=customer)

class PaymentRecordStark(Permissions,BaseStark):
    """
    客户费用提交申请
    """
    def display_edit_del(self, row=None, header_body=False, *args, **kwargs):
        """
        返回表格中不是数据库中的信息，自定制数据库之外的信息
        :param row:
        :param header_body:
        :return:
        """
        order_id = kwargs.get('order_id')
        if not header_body:
            return '操作'
        tpl = """
        <a href="%s"> <i class="fa fa-edit" aria-hidden="true"></i></a>|
        <a href="%s"> <i class="fa fa-trash-o" aria-hidden="true"></i></a>
        """ % ( self.reverse_edit_url(pk=row.pk, order_id=order_id),
            self.reverse_del_url(pk=row.pk, order_id=order_id))
        return mark_safe(tpl)

    list_display = ['order','payment','paid_fee','confirm_date','confirm_user','note',display_edit_del]

    search_list = []

    model_form_class = PaymentRecordModelForm

    def get_list_display(self):
        val=super().get_list_display()
        val.remove(BaseStark.display_del)
        val.remove(BaseStark.display_edit)
        return val


    def get_urls(self):
        urlpatterns = [
            re_path('list/(?P<order_id>\d+)/$', self.wrapper(self.changelist_view),name=self.get_list_url_name),
            re_path('add/(?P<order_id>\d+)/$', self.wrapper(self.add_view), name=self.get_add_url_name),
            re_path('(?P<order_id>\d+)/(?P<pk>\d+)/change/$', self.wrapper(self.change_view),
                    name=self.get_edit_url_name),
            re_path('(?P<order_id>\d+)/(?P<pk>\d+)/del/$', self.wrapper(self.del_view), name=self.get_del_url_name),
        ]
        extra_urls = self.extra_urls()

        if extra_urls:
            urlpatterns.extend(extra_urls)
        return urlpatterns


class AuditPaymentRecordModelForm(BaseModelForm):
    class Meta:
        model = models.PaymentRecord
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order'].queryset = models.Order.objects.filter(customer__name='南京金龙')


class AuditPaymentStark(BaseStark):
    """
    财务部进行审核
    """
    def get_add_btn(self,request,*args,**kwargs):
        return None

    def get_list_display(self):
        val=super().get_list_display()
        val.remove(BaseStark.display_del)
        val.remove(BaseStark.display_edit)
        return val

    def get_urls(self):
        urlpatterns = [
            re_path('audit/$', self.wrapper(self.changelist_view), name=self.get_url_name('audit_list') ),
        ]
        extra_urls = self.extra_urls()

        if extra_urls:
            urlpatterns.extend(extra_urls)

        return urlpatterns


    list_display = [BaseStark.display_checkbox,'order','payment','paid_fee','confirm_date','confirm_user','note']
    list_editable = ['confirm_date','confirm_user']
    action_list = [BaseStark.muti_editable_save]





