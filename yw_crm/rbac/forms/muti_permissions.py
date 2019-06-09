from django import forms
from rbac import models

##在视图中使用formset批量操作

# class MutiAddPermissionForm(forms.ModelForm):
#     class Meta:
#         model=models.Permission
#         fields=['title','url','name','parent','menu']
#         widgets={
#             'title':forms.TextInput( attrs={'class': 'form-control'}),
#             'url':forms.TextInput(attrs={'class': 'form-control'}),
#             'name':forms.TextInput(attrs={'class': 'form-control'}),
#             'parent':forms.Select(attrs={'class': "form-control"}),
#             'menu':forms.Select(attrs={'class': "form-control"}),
#         }
#     def clean(self):
#         menu=self.cleaned_data['menu']
#         parent=self.cleaned_data['parent']
#         if menu and parent:
#             self.add_error('menu','菜单和根权限同时只能选择一个')#错误标注在menu字段傍边


# class MutiAddPermissionForm(forms.Form):
#     title = forms.CharField(
#         max_length=32,
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         required=True
#     )
#     url = forms.CharField(
#         max_length=128,
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         required=True
#     )
#     name = forms.CharField(
#         max_length=64,
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         required=True
#     )
#     menu_id = forms.ChoiceField(
#         choices=[(None, '-----')],
#         widget=forms.Select(attrs={'class': "form-control"}),
#         required=False,
#
#     )
#     parent_id = forms.ChoiceField(
#         widget=forms.Select(attrs={'class': 'form-control'}),
#         choices=[(None, '-----')],  # 二选一
#         required=False
#     )
#
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['menu_id'].choices += models.Menu.objects.values_list('id', 'title')
#         self.fields['parent_id'].choices += models.Permission.objects.filter(parent__isnull=True).exclude(
#             menu__isnull=True).values_list('id', 'title')
#
#     def clean(self):
#         menu_id = self.cleaned_data.get('menu_id')
#         parent_id = self.cleaned_data.get('parent_id')
#         if menu_id and parent_id:
#             raise forms.ValidationError('菜单和根权限同时只能选择一个')
#
# class MultiEditPermissionForm(forms.Form):
#
#     id=forms.IntegerField(
#         widget=forms.HiddenInput(),
#     )
#     title=forms.CharField(
#         max_length=32,
#         widget=forms.TextInput(attrs={'class':'form-control'}),
#         required=True
#     )
#     url=forms.CharField(
#         max_length=128,
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         required=True
#     )
#     name=forms.CharField(
#         max_length=64,
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         required=True
#     )
#
#     menu_id = forms.ChoiceField(
#         choices=[(None, '-----')],
#         widget=forms.Select(attrs={'class': "form-control"}),
#         required=False,
#
#     )
#     parent_id=forms.ChoiceField(
#         choices=[(None, '-----')],  # 二选一
#         widget=forms.Select(attrs={'class': 'form-control'}),
#         required=False
#     )
#
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['menu_id'].choices += models.Menu.objects.values_list('id', 'title')
#         self.fields['parent_id'].choices += models.Permission.objects.filter(parent_id__isnull=True).exclude(
#             menu_id__isnull=True).values_list('id', 'title')
#
#     def clean(self):
#         menu_id = self.cleaned_data.get('menu_id')
#         parent_id = self.cleaned_data.get('parent_id')
#         if menu_id and parent_id:
#             raise forms.ValidationError('菜单和根权限同时只能选择一个')
#         return parent_id

class MultiPermissionForm(forms.Form):
    id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    menu_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': "form-control"}),
        required=False,

    )

    parent_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': "form-control"}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu_id'].choices += models.Menu.objects.values_list('id', 'title')
        self.fields['parent_id'].choices += models.Permission.objects.filter(parent__isnull=True).exclude(
            menu__isnull=True).values_list('id', 'title')

    def clean_parent_id(self):
        menu = self.cleaned_data.get('menu_id')
        parent_id = self.cleaned_data.get('parent_id')
        if menu and parent_id:
            raise forms.ValidationError('菜单和根权限同时只能选择一个')
        return parent_id

