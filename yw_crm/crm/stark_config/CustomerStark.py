from stark.service.base_stark import BaseStark,BaseModelForm,Option
from django.utils.safestring import mark_safe
from django.urls import reverse
from crm import models
from crm.permissions.permissios import Permissions

class PersonalCustomerModelForm(BaseModelForm):
    class Meta:
        model = models.Customer
        exclude = ['consultant', ]

class PersonalCustomerStark(Permissions,BaseStark):

    def display_follow(self, row=None, header_body=False,*args,**kwargs):
        if not header_body:
            return '跟进记录'
        url = reverse("stark:crm_consultantrecord_per_changelist",kwargs={'customer_id':row.pk}) #注意小写表名
        return mark_safe('<a href="%s">跟进记录</a>'%url)

    model_form_class = PersonalCustomerModelForm

    def display_order(self, row=None, header_body=False,*args,**kwargs):
        if not header_body:
            return '订单记录'
        url = reverse("stark:crm_order_changelist",kwargs={'customer_id':row.pk}) #注意小写表名
        return mark_safe("<a href='%s'>订单记录</a>"%url)

    list_display = [BaseStark.display_checkbox,'id','name','contact','status','source','referral_from','product','consultant','consultant_date',display_follow,display_order]
    list_editable = ['contact','status']
    action_list = [BaseStark.muti_editable_save]
    list_filter = [
        Option('name',),
        Option('status',text_func=lambda x:x[1],is_choice=True)
    ]


    search_list = ['name']

    def get_queryset(self,request,*args,**kwargs):
        current_user_id = self.request.session['user_info']['id']
        return self.model_class.objects.filter(consultant_id=current_user_id)

    def save(self,request,form,is_modify,*args,**kwargs):
        if not is_modify:
            current_user_id = self.request.session['user_info']['id']
            form.instance.consultant_id = current_user_id
        form.save()



