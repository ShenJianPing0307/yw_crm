from django import forms
from rbac import models

class PermissionModelForm(forms.ModelForm):

    class Meta:
        model=models.Permission
        fields='__all__'

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '请输入权限名称', 'class': 'form-control'}),
            'url': forms.TextInput(attrs={'placeholder': '请输入url', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'placeholder': '请输入url名称', 'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'menu':forms.Select(attrs={'class': 'form-control'}),
        }
        help_texts={
            'parent':'父级权限，无法作为菜单的权限才需要选择。',
            'menu':'选中，表示该权限可以作为菜单；否则，不可做菜单。'
        }
        error_messages ={
            'title':{
                    'required':'该字段不能为空'
            }
        }

    def clean(self):
        menu=self.cleaned_data['menu']
        parent=self.cleaned_data['parent']
        if menu and parent:
            self.add_error('menu','菜单和根权限同时只能选择一个')#错误标注在menu字段旁边


