from django import forms
from rbac import models
from django.utils.safestring import mark_safe

ICON_LIST = [
    ['fa fa-address-book', '<i aria-hidden="true" class="fa fa-address-book"></i>'],
    ['fa fa-address-book-o', '<i aria-hidden="true" class="fa fa-address-book-o"></i>'],
    ['fa fa-address-card', '<i aria-hidden="true" class="fa fa-address-card"></i>'],
    ['fa fa-address-card-o', '<i aria-hidden="true" class="fa fa-address-card-o"></i>'],
    ['fa fa-adjust', '<i aria-hidden="true" class="fa fa-adjust"></i>'],
    ['fa fa-american-sign-language-interpreting','<i aria-hidden="true" class="fa fa-american-sign-language-interpreting"></i>'],
    ['fa fa-stack-overflow', '<i class="fa fa-stack-overflow" aria-hidden="true"></i>'],
    ['fa fa-clipboard', '<i class="fa fa-clipboard"></i>'],

]

for item in ICON_LIST:
    item[1]=mark_safe(item[1])

class MenuModelForm(forms.ModelForm):

    class Meta:
        model=models.Menu

        fields=['title','icon']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '请输入菜单名称', 'class': 'form-control'}),
            'icon':forms.RadioSelect(choices=ICON_LIST)
        }

