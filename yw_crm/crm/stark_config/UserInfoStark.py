from stark.service.base_stark import BaseStark,BaseModelForm,Option,BaseForm
from django import forms
from crm import models
from django.forms import ValidationError
from django.shortcuts import HttpResponse,render,redirect
from django.urls import re_path
from django.utils.safestring import mark_safe


class UserInfoAddModelForm(BaseModelForm):
    confirm_password = forms.CharField(label='确认密码')

    class Meta:
        model = models.UserInfo
        fields='__all__'

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('密码输入不一致')
        return confirm_password

class UserInfoChangeModelForm(BaseModelForm):
    class Meta:
        model = models.UserInfo
        fields = '__all__'

    def clean(self):
        password = self.cleaned_data['password']
        self.cleaned_data['password'] = password
        return self.cleaned_data

class ResetPasswordForm(BaseForm):
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('密码输入不一致')
        return confirm_password

    def clean(self):
        password = self.cleaned_data['password']
        self.cleaned_data['password'] = password
        return self.cleaned_data


class UserInfoStark(BaseStark):

    def display_reset_pwd(self, row=None, header_body=False,*args,**kwargs):
        if not header_body:
            return '重置密码'
        reset_url = self.reverse_common_url\
            (self.get_url_name('reset_pwd'), pk=row.pk)
        return mark_safe("<a href='%s'>重置密码</a>" % reset_url)

    list_display = ['username', 'gender', 'phone', 'email', 'department', display_reset_pwd]

    search_list = ['username', 'name']

    list_filter = [
        Option(field='department'),
    ]

    def get_model_form_class(self, is_add, pk, request, *args,**kwargs):
        if is_add:
            return UserInfoAddModelForm
        return UserInfoChangeModelForm

    def reset_password(self, request, pk):
        """
        重置密码的视图函数
        :param request:
        :param pk:
        :return:
        """
        userinfo_object = models.UserInfo.objects.filter(id=pk).first()
        if not userinfo_object:
            return HttpResponse('用户不存在，无法进行密码重置！')
        if request.method == 'GET':
            form = ResetPasswordForm(request)
            return render(request, 'stark/change.html', {'form': form})
        form = ResetPasswordForm(data=request.POST,request=request)
        if form.is_valid():
            userinfo_object.password = form.cleaned_data['password']
            userinfo_object.save() #赋值后再进行保存
            return redirect(self.reverse_changelist_url())
        return render(request, 'stark/change.html', {'form': form})

    def extra_urls(self):
        patterns = [
            re_path('reset/password/(?P<pk>\d+)/$', self.wrapper(self.reset_password),
                name=self.get_url_name('reset_pwd')),
        ]
        return patterns