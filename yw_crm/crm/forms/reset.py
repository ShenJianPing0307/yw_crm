from django import forms
from django.forms import widgets
from crm import models

class EmailForm(forms.Form):

    email=forms.EmailField(
        max_length=32,
        required=True,
        error_messages={
            'required':'邮箱不能为空',
            'max_length':'长度超过32位'
        },
        widget=widgets.EmailInput(attrs={'class':'form-control','placeholder':'Email'})
    )

    # def clean(self):
    #     email=self.cleaned_data['email']
    #     obj=models.UserInfo.objects.filter(email=email).first()
    #     if not obj:
    #         raise forms.ValidationError('邮箱不存在')#如果raise 错误就会context must be a dict rather than set.