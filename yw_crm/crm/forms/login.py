from django import forms
from django.forms import widgets
from crm import models


class LoginForm(forms.Form):
    username=forms.CharField(max_length=32,
                             required=True,
                             error_messages={
                                 'required':'用户名不能为空'
                                },
                             widget=widgets.TextInput(attrs={'class': 'form-control','placeholder':'用户名'})
                             )
    password=forms.CharField(max_length=32,
                            required = True,
                                       error_messages = {
                                'required': '用户名不能为空'
                            },
                            widget = widgets.TextInput(attrs={'class': 'form-control','placeholder':'用户名'})
                             )

    def clean(self):
        username=self.cleaned_data.get('username')
        password=self.cleaned_data.get('password')
        user=models.UserInfo.objects.filter(username=username,password=password).first()
        if not user:
            raise forms.ValidationError('用户名或密码错误|')
        self.request.session['user_info'] = {'id': user.id, 'username': user.username}  # 存入的数据能够序列化
        self.request.user=user
        self.user=user



