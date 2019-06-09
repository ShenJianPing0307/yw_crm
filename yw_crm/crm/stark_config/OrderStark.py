from stark.service.base_stark import BaseStark,BaseModelForm
from crm import models
from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.conf import settings
from django.db.models.fields import DateField,DateTimeField
from django.urls import re_path
from django.shortcuts import render,HttpResponse
from django.forms import modelformset_factory
from crm.permissions.permissios import Permissions


class OrderModelForm(BaseModelForm):

    class Meta:
        model=models.Order
        exclude=['consultant','customer','check_date']

class OrderStark(Permissions,BaseStark):


    model_form_class = OrderModelForm

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

    list_display = [BaseStark.display_checkbox,'id','customer', 'product', 'consultant', 'quantity', 'delivery_date', 'note', display_edit_del]

    def get_list_display(self):
        val=super().get_list_display()
        val.remove(BaseStark.display_del)
        val.remove(BaseStark.display_edit)
        return val

    action_list = [BaseStark.muti_delete]


    def get_urls(self):
        urlpatterns = [
            re_path('customer/order/(?P<customer_id>\d+)/$', self.wrapper(self.changelist_view), name=self.get_list_url_name),
            re_path('add/(?P<customer_id>\d+)/$', self.wrapper(self.add_view), name=self.get_add_url_name),
            re_path('(?P<customer_id>\d+)/(?P<pk>\d+)/change/$', self.wrapper(self.change_view),name=self.get_edit_url_name),
            re_path('(?P<customer_id>\d+)/(?P<pk>\d+)/del/$', self.wrapper(self.del_view), name=self.get_del_url_name),
        ]

        extra_urls = self.extra_urls()

        if extra_urls:
            urlpatterns.extend(extra_urls)

        return urlpatterns

    def get_queryset(self,request,*args,**kwargs):
        customer_id = kwargs.get('customer_id')
        current_user_id = request.session['user_info']['id']
        return self.model_class.objects.filter(customer_id=customer_id, customer__consultant_id=current_user_id) or self.model_class.objects.none()

    def save(self,request,form,is_modify,*args,**kwargs):
        customer_id = kwargs.get('customer_id')
        current_user_id = request.session['user_info']['id']
        customer_obj= models.Customer.objects.filter(id=customer_id,
                                                       status=2).exists()
        if customer_obj:
            return HttpResponse('该客户未签合同，无法添加订单信息！')

        if not is_modify:
            form.instance.customer_id = customer_id
            form.instance.consultant_id = current_user_id
        form.save()


class CheckModelForm(BaseModelForm):

    class Meta:
        model=models.Order
        fields="__all__"

class CheckOrderStark(BaseStark):

    model_form_class = OrderModelForm

    def get_urls(self):
        urlpatterns = [
            re_path('check_list/$', self.wrapper(self.changelist_view), name=self.get_url_name('check_order')),
        ]
        extra_urls = self.extra_urls()

        if extra_urls:
            urlpatterns.extend(extra_urls)
        return urlpatterns

    def changelist_view(self, request,*args,**kwargs):
        queryset=models.Order.objects.filter(check_date__isnull=True).all()
        check_formset=modelformset_factory(model=models.Order,form=CheckModelForm,extra=0)
        if request.method == 'POST':
            formset=check_formset(data=request.POST)
            if formset.is_valid():
                formset.save()
        formset=check_formset(queryset=queryset)
        return render(request,'check_order.html',{'formset':formset})


class CustomerOrderStark(BaseStark):

    def display_payment(self, row=None, header_body=False, *args, **kwargs):
        if not header_body:
            return '付款记录'
        url = reverse("stark:crm_paymentrecord_changelist", kwargs={'order_id': row.pk})  # 注意小写表名
        return mark_safe("<a href='%s'>付款记录</a>" % url)

    def display_status(self, row=None, header_body=False, *args, **kwargs):
        if not header_body:
            return '产品审核状态'
        obj=models.ProductAudit.objects.filter(procedure__order_id=row.id).first()
        if obj:
            return "%s"%obj.status

    def get_list_display(self):
        val=super().get_list_display()
        val.remove(BaseStark.display_del)
        val.remove(BaseStark.display_edit)
        return val

    def get_urls(self):
        urlpatterns = [
            re_path('customer/order/list/$', self.wrapper(self.changelist_view),name=self.get_url_name('customer_order')),
        ]
        extra_urls = self.extra_urls()

        if extra_urls:
            urlpatterns.extend(extra_urls)
        return urlpatterns

    list_display = ['customer','product','quantity',display_status,display_payment]

    def get_add_btn(self,request,*args,**kwargs):
        return None

    def get_queryset(self,request,*args,**kwargs):
        current_user_id = self.request.session['user_info']['id']
        customer=models.Customer.objects.filter(name=models.UserInfo.objects.filter(id=current_user_id).first().username).first()
        return models.Order.objects.filter(customer=customer)
