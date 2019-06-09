from django.template import Library
from types import FunctionType
from django.forms.models import ModelChoiceField
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.db.models import ForeignKey, ManyToManyField, OneToOneField
from django.db.models.fields import DateField
from django.db.models.query import QuerySet
from django.db import models
from django.conf import settings
from crm.permissions.permissios import Permissions

register=Library()

######################使用生成器
def header_list(cl):

    if cl.list_display:
        for field in cl.list_display:
            if isinstance(field, FunctionType):
                header_name = field(cl.stark_class, row=None, header_body=False)  # 加后面的编辑框
            else:
                header_name = cl.stark_class.model_class._meta.get_field(field).verbose_name  # 获取对应字段的verbose_name
            yield header_name
    else:
        yield cl.stark_class.model_class._meta.model_name  # 如果list_display中没有值显示表名

def body_list(cl):
    for row in cl.queryset:
        row_list = []  # 注意必须放在这个循环下面
        """
        ['id','name']
        """
        """
        body_list=[
        ['id','name']
        ...
        ]
        """
        if not cl.list_display:  # list_display中没有值
            row_list.append(row)
            yield row_list
            continue
        for field in cl.list_display:  # list_display中有值
            if isinstance(field, FunctionType):
                val = field(cl.stark_class, row=row, header_body=True)
            else:
                field_obj=cl.stark_class.model_class._meta.get_field(field) #获取字段对象
                if field_obj.choices:
                    val=getattr(row,"get_%s_display"%field)()
                elif isinstance(field_obj,DateField):
                    val = getattr(row, field)
                    if val:
                        val=val.strftime("%Y-%m-%d")
                elif isinstance(field_obj,ManyToManyField):
                    queryset = getattr(row,field).all()#ManyToManyField反射需要加all()
                    val_list=[]
                    for obj in queryset:
                        val_list.append(str(obj))
                    val='、'.join(val_list)
                else:
                    val = getattr(row, field) #ForeignKey字段反射，ManyToManyField会出现问题
                if not val:
                    val=''
            row_list.append(val)
        yield row_list

@register.inclusion_tag('stark/table.html')
def table_list(cl):

    return {'header_list':header_list(cl),'body_list':body_list(cl)}


@register.simple_tag()
def gen_is_pop(bfield,starkclass):
    if isinstance(bfield.field,ModelChoiceField):
        namespace=starkclass.site.namespace
        related_app_lebel=bfield.field.queryset.model._meta.app_label
        related_model_name=bfield.field.queryset.model._meta.model_name

        url_name='%s:%s_%s_add'%(namespace,related_app_lebel,related_model_name)
        # if Permissions().permission_dict and url_name in Permissions().permission_dict: #判断权限，pop功能的+是否显示
        add_url=reverse(url_name)
        add_url=add_url+'?pop_id=id_%s'%bfield.name
        return mark_safe("""<a onclick="pop('%s')" style="position: absolute;right: -30px;top: 20px"><span style="font-size: 28px">+</span></a>"""%add_url)
    return bfield


@register.simple_tag()
def m2m_data(form,field,stark_class):
    """
    出项在左侧的可选项
    :param form:
    :param field:
    :param stark_class:
    :return:
    """
    field_name=field.name
    field_obj=stark_class.model_class._meta.get_field(field_name)
    if isinstance(field_obj,ManyToManyField):
        data_set = set(field_obj.remote_field.model.objects.all())
        if form.instance.id:
            selected_data_set=set(getattr(form.instance,field_obj.name).all())
            queryset=data_set-selected_data_set
            return queryset
        return data_set

@register.simple_tag()
def m2m_un_data(form,field,stark_class):
    """
    出项在左侧已选项
    :param form:
    :param field:
    :return:
    """
    field_name = field.name
    field_obj=stark_class.model_class._meta.get_field(field_name)
    if isinstance(field_obj,ManyToManyField):
        if form.instance.id:
            selected_data_set = getattr(form.instance, field_obj.name).all()
            return selected_data_set
        else:
            return []

@register.inclusion_tag('stark/m2m.html')
def m2m_all_data(form,field,stark_class):
    return {'m2m_data':m2m_data(form,field,stark_class),'m2m_un_data':m2m_un_data(form,field,stark_class),'field':field}



