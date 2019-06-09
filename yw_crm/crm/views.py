from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from django.contrib.auth import login,authenticate
from crm import models
from utils.code import get_verify_code
from django.conf import settings
import os
from crm.forms.login import LoginForm
from crm.forms.reset import EmailForm
from django.urls import reverse
from rbac.services.init_permission_menu import InitPermission
import random,string
from django.core.mail import send_mail
import json


# Create your views here.

def verify_code(request):

    return get_verify_code(request)

class LoginView(View):

    def get(self,request):
        form = LoginForm()

        # with open(os.path.join(settings.BASE_DIR,'static/images/verifycode.png'),'wb') as f:
        #     f.write(verifycode_response.content)
        return render(request,'login.html',{'form':form})

    def post(self,request):
        check_code=request.POST.get('check_code')
        is_checked=request.POST.get('is_checked')

        if check_code:
            check_code=check_code.upper()
            if not check_code==request.session.get('verifycode').upper() :
                return redirect('/login/',)
        if is_checked:
            request.session.set_expiry(60*60*24*30)
        form=LoginForm(data=request.POST)
        form.request=request
        if form.is_valid():
            InitPermission(request, form.user).init_permissions_dict()
            InitPermission(request, form.user).init_menu_dict()
            return redirect('/index/')
        return render(request,'login.html',{'form':form})

class LogoutView(View):

    def get(self,request):
        request.session.delete()
        return redirect('/login/')

class IndexView(View):

    def get(self,request):

        return render(request,'index.html')

class ResetView(View):

    def get(self,request):
        form=EmailForm()
        return render(request,'reset.html',{'form':form})

    def post(self,request):
        print(request.POST)
        result = {'status':None,'message':None,'data':None}
        form=EmailForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data.get('email')
            obj=models.UserInfo.objects.filter(email=email).first()
            if not obj:
                result['status']=False
                result['message']='邮箱不存在'
            else:
                str = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
                rand_str = ''
                for i in range(0, 6):
                    rand_str += str[random.randrange(0, len(str))]
                send_mail(
                    '重置密码',
                    '亲爱的用户，您的密码已经重置，新的密码为%s' % rand_str,
                    settings.EMAIL_HOST_USER,
                    [email, ],
                    fail_silently=False
                )
                models.UserInfo.objects.filter(id=obj.id).update(password=rand_str)
                result['status'] = True
                result['message'] = '邮件发送成功'

        return HttpResponse(json.dumps(result))


def test(request):
    from django.db.models import ForeignKey, ManyToManyField, OneToOneField
    from django.db.models.fields import DateField

    # obj=models.Customer.objects.filter(id=1).first()
    # # queryset=obj.product.all()
    # val=getattr(obj,'consultant')
    # m2m=getattr(obj,'product').all()
    # print(val)
    # print(m2m)


    # field_obj=models.Customer._meta.get_field('consultant_date')
    # print(type(field_obj))
    # if isinstance(field_obj,ManyToManyField):
    #     queryset=field_obj.remote_field.model.objects.all()
    #     print(queryset)

    # queryset=models.WorkShop.objects.values_list('name').distinct()
    # print(queryset)
    # print(type(queryset))
    # from django.db.models.query import QuerySet
    # for item in queryset:
    #     print(item[0])
    from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
    # val=getattr(models.Procedure,'product').get_queryset()
    # print(val)

    obj=models.PaymentRecord.objects.filter(id=2).first()
    field_obj=models.PaymentRecord._meta.get_field('confirm_user')
    print(field_obj.get_choices())#[('', '---------'), (7, '李杰'), (15, '李材')]
    # field_obj=models.Customer._meta.get_field('status')  #[('', '---------'), (1, '已签合同'), (2, '未签合同')]
    # print(field_obj.get_choices())
    # print(type(field_obj))
    # print(field_obj.remote_field.model)
    # print(getattr(obj,'confirm_user_id'
    #               ))
    # val=getattr(obj,'confirm_date')
    # m=getattr(obj,'confirm_user')
    # print(obj.confirm_user_id)
    # print(obj.confirm_user.id)
    return HttpResponse('...')

from django.db.models.fields.related import ForeignKey
from django.db.models.fields.reverse_related import ManyToOneRel