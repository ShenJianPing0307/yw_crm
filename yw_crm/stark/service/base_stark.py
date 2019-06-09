from django.urls import re_path
from django.shortcuts import HttpResponse, render, redirect
import functools
import json
from types import FunctionType
from django.utils.safestring import mark_safe
from django.urls import reverse
from django import forms
from django.db.models import Q
from django.http import QueryDict
from django.db.models import ForeignKey, ManyToManyField, OneToOneField
from django.utils.safestring import mark_safe
from django.forms import ModelForm
# from django.db.models.fields.related import ForeignKey,ManyToManyField,OneToOneField
from django.db.models.fields import DateField,DateTimeField


# #########实现choice取值，可以自己配置，只需要在list_play中调用get_choice_text('gender','性别')
# #利用闭包以及反射
# def get_choice_text(field, head):
#     def inner(self, row=None, header=None):
#         if header:
#             return head
#         func_name = 'get_%s_display' % field
#         return getattr(row, func_name)()
#
#     return inner

class RowQueryset(object):

    def __init__(self, row_queryset, option, view_class):
        """

        :param row_queryset: 封装的row_queryset的数据
        :param option: 每一个option对象
        """
        self.row_queryset = row_queryset
        self.option = option
        self.view_class = view_class  # 这是changeView类，里面封装了请求的request对象

    def __iter__(self):  # 为了循环这个对象，实现iter方法，iter返回的是什么，页面显示的就是什么

        yield """<div class="whole">"""
        ##################生成全部选项的url############
        total_query_dict = self.view_class.request.GET.copy()  # 深拷贝一份
        total_query_dict._mutable = True
        origin_url_list = self.view_class.request.GET.getlist(self.option.field)  # 获取所有GET的搜索参数[],['2'],['3']
        if origin_url_list:  # 请求中有值，就将自己字段去掉
            total_query_dict.pop(self.option.field)
            yield """<a href="?%s">全部</a>""" % total_query_dict.urlencode()
        else:
            yield """<a class="active" href="?%s">全部</a>""" % total_query_dict.urlencode()
        yield """</div>"""
        yield """<div class="others">"""

        for obj in self.row_queryset:  # 循环得到的要不就是queryset中的对象，要不就是元组对象
            query_dict = self.view_class.request.GET.copy()  # 深拷贝一份
            query_dict._mutable = True  # 修改参数
            if not self.option.is_multi:  # 支持单选
                query_dict[self.option.field] = self.option.get_value(obj)  # 获取数据库中对应的值
                val = self.option.get_value(obj)  # 从数据库中取出值与之前请求作比较，看是否加入选中的样式
                if str(val) in origin_url_list:
                    query_dict.pop(self.option.field)  # 点击第二次后会移除自身
                    yield '<a class="active" href="?%s">%s</a>' % (
                    query_dict.urlencode(), self.option.get_text(obj))  # 引入text_func是为了解决choice,元组的问题
                else:
                    yield '<a href="?%s">%s</a>' % (
                    query_dict.urlencode(), self.option.get_text(obj))  # 引入text_func是为了解决choice,元组的问题
            else:
                multi_value_list = self.view_class.request.GET.getlist(self.option.field)  # 获取请求的所有搜索参数
                val = self.option.get_value(obj)
                if str(val) in origin_url_list:
                    multi_value_list.remove(str(val))  # 如果请求中已经存在就将其移除
                    query_dict.setlist(self.option.field, multi_value_list)  # 将已经变化的参数重新设置到querydict中
                    yield '<a class="active" href="?%s">%s</a>' % (
                    query_dict.urlencode(), self.option.get_text(obj))  # 引入text_func是为了解决choice,元组的问题

                else:
                    multi_value_list.append(val)
                    query_dict.setlist(self.option.field, multi_value_list)
                    yield '<a href="?%s">%s</a>' % (
                    query_dict.urlencode(), self.option.get_text(obj))  # 引入text_func是为了解决choice,元组的问题
        yield """</div>"""

class Option(object):
    """
    将传入的值进行封装，也就是现在list_filter列表中不是一个个字段而是一个个option对象
    """

    def __init__(self, field, condition=None, is_choice=False, text_func=None, value_func=None, is_multi=False):
        self.field = field  # 传递的字段
        if not condition:
            condition = {}
        self.condition = condition  # 传递的显示过滤条件
        self.is_choice = is_choice
        self.text_func = text_func  # 中文
        self.value_func = value_func
        self.is_multi = is_multi  # 是否支持多选搜索

    def get_queryset(self, _field_obj, model_class, view_class):

        if isinstance(_field_obj, ForeignKey) or isinstance(_field_obj,ManyToManyField):  # 如果对应字段对象是Foreignkey类型，就取出另一张表中的数据
            # row_queryset=_field_obj.remote_field.model.objects.filter(**self.condition) #rel如果不行就是用remote_field
            row_queryset = RowQueryset(_field_obj.remote_field.model.objects.filter(**self.condition), self, view_class)  # 传入self是因为需要用到option中的一些参数text_func
        else:
            if self.is_choice:
                # row_queryset=_field_obj.choices
                row_queryset = RowQueryset(_field_obj.choices, self, view_class)
            else:
                # row_queryset=model_class.objects.filter(**self.condition)
                row_queryset = RowQueryset(model_class.objects.filter(**self.condition), self, view_class)
        return row_queryset

    def get_text(self, obj):
        """
        获取文本值，如果text_func有值就按照设定好的，如果没有的话就执行str()
        :param item:
        :return:
        """
        if self.text_func:
            return self.text_func(obj)
        return str(obj)

    def get_value(self, obj):
        """
        构建url后的值
        :param obj:
        :return:
        """
        if self.value_func:
            return self.value_func(obj)
        if self.is_choice:
            return obj[0]
        return obj.pk

class BaseRequestModelForm(object):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(BaseRequestModelForm, self).__init__(*args, **kwargs)

class BaseModelForm(BaseRequestModelForm,forms.ModelForm):

    def __init__(self,request,*args,**kwargs):
        super().__init__(request,*args,**kwargs)
        #####给modelform字段加样式
        for name,field in self.fields.items():
            attrs_dict={'class':'form-control'}
            if 'DateTimeField' in field.__repr__():
                attrs_dict = {'class': 'form-control', 'date_time': 'datetimepicker', 'size': '16'}
            field.widget.attrs.update(attrs_dict)

class BaseRequestForm(object):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(BaseRequestForm, self).__init__(*args, **kwargs)

class BaseForm(BaseRequestForm,forms.Form):

    def __init__(self, request,*args, **kwargs):
        super(BaseForm, self).__init__(request,*args, **kwargs)
        # 统一给Form生成字段添加样式
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class BaseStark(object):

    def __init__(self, model_class, site,prev):
        self.model_class = model_class
        self.site = site
        self.prev=prev #反向生成url的别名需要用到的参数
        self.request = None
        self.back_condition_key = "_filter"  # 保留原搜索条件

    order_by = ['-id']
    list_display = []  # 页面需要展示的字段
    model_form_class = None
    action_list = []
    search_list = []
    list_filter = []
    list_editable= []
    filter_horizontal=[]
    has_add_btn=True

    def get_filter_horizontal(self):

        return self.filter_horizontal

    def get_list_editable(self):

        return self.list_editable

    def get_order_by(self):

        return self.order_by

    def get_list_display(self):  # 通过函数调用，这样可以重写这个函数，其他功能可以加到这个函数中，如果单纯的列表是无法实现的
        val=[]
        val.extend(self.list_display)
        val.append(BaseStark.display_del)
        val.append(BaseStark.display_edit)
        return val

    def get_action_list(self):

        return self.action_list

    def get_action_dict(self):  # 字典比列表取值快
        action_dict = {}
        for item in self.get_action_list():
            action_dict[item.__name__] = item
        return action_dict

    def get_search_list(self):

        return self.search_list

    def get_list_filter(self):

        return self.list_filter

    def get_list_filter_condition(self):
        comb_condition = {}
        for option in self.get_list_filter():
            filter_list = self.request.GET.getlist(option.field)
            if filter_list:
                comb_condition["%s__in" % option.field] = filter_list
            """
            {
            title:['a','b'],
            }
            """
        return comb_condition

    def muti_delete(self,request,*args,**kwargs):
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(pk__in=pk_list).delete()
        return redirect(self.reverse_changelist_url())

    muti_delete.attr_dict = {'text':'批量删除'}

    def muti_init(self,request,*args,**kwargs):
        return None

    muti_init.attr_dict = {'text':'批量初始化'}

    def create_list_editable_model_form(self,field):
        """默认为修改表单"""

        class Meta:
            model = self.model_class
            fields = field

        dynamic_form = type("DynamicModelForm", (ModelForm,), {'Meta': Meta, })
        return dynamic_form

    def muti_editable_save(self, request,*args,**kwargs):
        """
        ajax实现list_editble保存，通过判断是否有id属性 muti_editable_save.attr_dict = {'text':'批量保存','id':'submit'}
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        editable_data = str(request.body, encoding='utf-8')
        if editable_data:
            editable_data = json.loads(editable_data) ## for list editable
            del editable_data[0]
        print('反射',editable_data) # [{'confirm_user': '7', 'confirm_date': '1899-12-13 09:50:00+00:00', 'id': '2'}]
        for row_data in editable_data:
            obj_id = row_data.get('id')
            if obj_id:
                print("editable data", row_data, list(row_data.keys()))#['id', 'confirm_user', 'confirm_date']
                obj = self.model_class.objects.get(id=obj_id)
                model_form = self.create_list_editable_model_form(list(row_data.keys()))
                form_obj = model_form(instance=obj, data=row_data)
                if form_obj.is_valid():
                    form_obj.save()

        # editable_data = json.loads(str(request.body, encoding='utf-8'))
        # if editable_data:  # for list editable
        #     for row_data in editable_data:
        #         print(row_data)
        #         obj_id = row_data.get('id')
        #         if obj_id:
        #             print("editable data", row_data, list(row_data.keys()))
        #             obj = self.model_class.objects.get(id=obj_id)
        #             model_form = self.create_list_editable_model_form(list(row_data.keys()))
        #             form_obj = model_form(instance=obj, data=row_data)
        #             if form_obj.is_valid():
        #                 form_obj.save()
    muti_editable_save.attr_dict = {'text':'批量保存','id':'submit'}

    def get_url_name(self,param):
        app_label = self.model_class._meta.app_label
        model_name = self.model_class._meta.model_name
        if self.prev:
            name='%s_%s_%s_%s' % (app_label, model_name,self.prev,param)
        else:
            name='%s_%s_%s' % (app_label, model_name,param)
        return name

    @property
    def get_list_url_name(self):
        return self.get_url_name('changelist')

    @property
    def get_edit_url_name(self):
        return self.get_url_name('change')

    @property
    def get_add_url_name(self):
        return self.get_url_name('add')

    @property
    def get_del_url_name(self):
        return self.get_url_name('del')

    def reverse_common_url(self,name,*args,**kwargs):
        common_name = "%s:%s" % (self.site.namespace, name,)
        base_url = reverse(common_name,args=args,kwargs=kwargs)
        if not self.request.GET:
            add_url=base_url
        else:
            param_str = self.request.GET.urlencode()
            new_query_dict = QueryDict(mutable=True)
            new_query_dict[self.back_condition_key] = param_str
            add_url = "%s?%s" % (base_url, new_query_dict.urlencode(),)
        return add_url

    def reverse_edit_url(self,*args,**kwargs):
        return self.reverse_common_url(self.get_edit_url_name,*args,**kwargs)

    def reverse_del_url(self,*args,**kwargs):

        return self.reverse_common_url(self.get_del_url_name,*args,**kwargs)

    def reverse_add_url(self,*args,**kwargs):

        return self.reverse_common_url(self.get_add_url_name,*args,**kwargs)

    def reverse_changelist_url(self,*args,**kwargs):
        namespace = self.site.namespace
        list_url = reverse('%s:%s' % (namespace, self.get_list_url_name),args=args,kwargs=kwargs)
        origin_url = self.request.GET.get(self.back_condition_key)

        if not origin_url:
            return list_url

        list_url = "%s?%s" % (list_url, origin_url)  # /stark_config/app01/userinfo/list/?q=k
        return list_url

    def display_checkbox(self, row=None, header_body=False, *args, **kwargs):
        if not header_body:
            return mark_safe('<input type="checkbox" id="SelectAll" />')
        return mark_safe('<input type="checkbox" name="pk" is_select="SelectEach" value="%s"/>' % row.pk)

    def display_edit(self, row=None, header_body=False, *args, **kwargs):
        if not header_body:
            return '编辑'
        return mark_safe(
            '<a href="%s"> <i class="fa fa-edit" aria-hidden="true"></i></a>' % self.reverse_edit_url(pk=row.pk))

    def display_del(self, row=None, header_body=False, *args, **kwargs):
        if not header_body:
            return '删除'
        return mark_safe(
            '<a href="%s"> <i class="fa fa-trash-o" aria-hidden="true"></i></a>' % self.reverse_del_url(pk=row.pk))

    def display_edit_del(self, row=None, header_body=False, *args, **kwargs):
        """
        返回表格中不是数据库中的信息，自定制数据库之外的信息
        :param row:
        :param header_body:
        :return:
        """
        if not header_body:
            return '操作'
        tpl = """
        <a href="%s"> <i class="fa fa-edit" aria-hidden="true"></i></a>|
        <a href="%s"> <i class="fa fa-trash-o" aria-hidden="true"></i></a>
        """ % (self.reverse_edit_url(pk=row.pk), self.reverse_del_url(pk=row.pk))
        return mark_safe(tpl)

    def get_add_btn(self,request,*args,**kwargs):
        if self.has_add_btn:
            return mark_safe('<a href="%s" class="btn btn-primary">添加</a>' % self.reverse_add_url(*args,**kwargs))
        return None
    #######处理搜索功能############
    def get_search_condition(self):
        search_list = self.get_search_list()
        q = self.request.GET.get('q', '')
        con = Q()
        con.connector = 'OR'
        for field in search_list:
            con.children.append(('%s__contains' % field, q))
        return search_list, con, q

    ######获取queryset对象，根据需求重新此方法进行筛选
    def get_queryset(self,request,*args,**kwargs):
        return self.model_class.objects

    def changelist_view(self, request,*args,**kwargs):
        """
        处理显示数据的页面
        :param request:
        :return:
        """

        if request.method == 'POST':
            editable_data=str(request.body,encoding='utf-8')
            if editable_data:
                editable_data=json.loads(editable_data)
            action_name=editable_data[0].get('action')
            if action_name:
                print(action_name)
            # print(editable_data)
            # print('querydict',type(editable_data))
            # editable_data = request.POST.get("editable_data")
            # print('data',type(str(request.body,encoding='utf-8')))

            # editable_data=json.loads(str(request.body,encoding='utf-8'))
            action_name = request.POST.get('action') or action_name  # 获取请求的什么功能，批量删除还是批量初始化
            if action_name:
                if action_name not in self.get_action_dict():  # 防止前端客户刻意修改代码，进行验证
                    return HttpResponse('非法请求！')
                response = getattr(self, action_name)(request,*args,**kwargs)  # 反射执行函数 action_name就是函数名称
                if response:
                    return response  # 返回什么结果就是什么

            # if editable_data:  # for list editable
            #
            #     for row_data in  editable_data:
            #         print(row_data)
            #         obj_id = row_data.get('id')
            #         if obj_id:
            #             print("editable data", row_data, list(row_data.keys()))
            #             obj =self.model_class.objects.get(id=obj_id)
            #             model_form = self.create_list_editable_model_form(list(row_data.keys()))
            #             form_obj = model_form(instance=obj, data=row_data)
            #             if form_obj.is_valid():
            #                 form_obj.save()

        ###################Hsearch搜索################
        search_list, con, q = self.get_search_condition()

        # ########## 6. 添加按钮 #########
        add_btn = self.get_add_btn(request, *args, **kwargs)

        ##################分页######################
        from stark.utils.stark.pagination import Pagination
        total_count = self.model_class.objects.filter(con).count()
        query_params = request.GET.copy()  # 拷贝request.GET参数，不会影响后来者
        query_params._mutable = True  # 设置为True可以进行修改QueryDict字典
        page = Pagination(request.GET.get('page'), total_count, request.path_info, query_params, per_page=7)
        origin_queryset=self.get_queryset(request,*args,**kwargs)
        queryset = origin_queryset.filter(con).filter(**self.get_list_filter_condition()).order_by(
            *self.get_order_by()).distinct()[page.start:page.end]  # distinct是为了防止多对多字段中,is_multi=True出项重复数据

        #############表头########
        header_list=self.header_list(request,*args,**kwargs)

        #########表内容#########
        body_list=self.body_list(request,queryset,*args,**kwargs)

        cl = ChangeList(self, search_list, q, page, queryset,header_list,body_list,*args,**kwargs)  # 封装到ChangeList类中

        return render(request, 'stark/changelist.html', {'cl': cl,})

    def header_list(self,request,*args,**kwargs):
        list_display = self.get_list_display()
        if list_display:
            for field in list_display:
                if isinstance(field, FunctionType):
                    header_name = field(self, row=None, header_body=False, *args, **kwargs)  # 加后面的编辑框
                else:
                    header_name = self.model_class._meta.get_field(field).verbose_name  # 获取对应字段的verbose_name
                yield header_name
        else:
            yield self.model_class._meta.model_name  # 如果list_display中没有值显示表名

    def render_editable_value(self,row,field_or_func):
        field_obj = self.model_class._meta.get_field(field_or_func)  # 获取字段对象
        if hasattr(row,field_or_func):
            if field_obj.get_internal_type() == "ForeignKey":
                field_val=getattr(row,"%s_id"%(field_obj.name))
            else:
                field_val=getattr(row,field_or_func)
        else:
            field_val=''
        if not field_obj.choices and field_obj.get_internal_type() != "ForeignKey" :
            if field_obj.get_internal_type() == "DateTimeField":
                val = '''<input data-tag='editable' class='form-control' type='text' name='%s' value='%s'  date_time='datetimepicker'>''' % (field_obj.name, getattr(row, field_obj.name) or '')
            else:
                val = '''<input data-tag='editable' class='form-control' type='text' name='%s' value='%s' >''' %(field_obj.name,getattr(row,field_obj.name) or '')
        else:
            val = '''<select data-tag='editable' class='form-control'  name='%s' >''' % field_obj.name
            for option in field_obj.get_choices():
                if option[0] == field_val:
                    selected_attr = "selected"
                else:
                    selected_attr = ''
                val += '''<option value='%s' %s >%s</option>'''% (option[0],selected_attr,option[1])
        return mark_safe(val)

    def body_list(self,request,queryset,*args,**kwargs):
        list_display = self.get_list_display()
        for row in queryset:
            row_list = []  # 注意必须放在这个循环下面
            if not list_display:  # list_display中没有值
                row_list.append(row)
                yield row_list
                continue
            for field_or_func in list_display:

                # list_display中有值
                if isinstance(field_or_func, FunctionType):
                    val = field_or_func(self, row=row, header_body=True, *args, **kwargs)
                elif field_or_func in self.list_editable:
                    val = self.render_editable_value(row,field_or_func)
                else:
                    field_obj = self.model_class._meta.get_field(field_or_func)  # 获取字段对象
                    if field_obj.choices:
                        val = getattr(row, "get_%s_display" % field_or_func)()
                    elif isinstance(field_obj, ManyToManyField):
                        queryset = getattr(row, field_or_func).all()  # ManyToManyField反射需要加all()
                        val_list = []
                        for obj in queryset:
                            val_list.append(str(obj))
                        val = '、'.join(val_list)
                    else:
                        val = getattr(row, field_or_func)  # ForeignKey字段反射，ManyToManyField会出现问题
                    if not val:
                        val = ''
                row_list.append(val)
            yield row_list

    def get_model_form_class(self, is_add,request,pk, *args,**kwargs):
        """
        获取添加、修改功能的modelform
        :return:
        """
        if self.model_form_class:
            return self.model_form_class

        class AddModelForm(BaseModelForm,forms.ModelForm):
            class Meta:
                model = self.model_class
                fields = '__all__'
                ###加样式

            # def __new__(cls, *args, **kwargs):
            #
            #     for field_name in cls.base_fields:  # field_name  字段名
            #         field_obj = cls.base_fields[field_name]  # 字段对象
            #         if 'DatetimeField' in field_obj.__repr__():
            #             attr_dic = {'class': 'form-control', 'date_time': 'datetimepicker', 'size': '16', }
            #             field_obj.widget.attrs.update(attr_dic)
            #     return forms.ModelForm.__new__(cls)

        return AddModelForm
    ##################pop功能未使用，已经在simtag中实现
    def is_pop(self, form):
        from django.forms.boundfield import BoundField
        from django.forms.models import ModelChoiceField
        for bfield in form:
            print(type(bfield))
            if isinstance(bfield.field, ModelChoiceField):
                is_pop = True
                namespace =self.site.namespace
                related_app_lebel = bfield.field.queryset.model._meta.app_label
                related_model_name = bfield.field.queryset.model._meta.model_name
                add_url = reverse('%s:%s_%s_add' % (namespace, related_app_lebel, related_model_name))
                form.is_pop=is_pop
                form.a_url=mark_safe("""<a onclick="pop('{{ %s }}')" style="position: absolute;right: -30px;top: 20px"><span style="font-size: 28px">+</span></a>""" % add_url)
        return form

    ####对于一些排除字段，重新此方法进行添加
    def save(self,request,form,is_modify,*args,**kwargs):

        return form.save()

    def add_view(self,request,*args,**kwargs):
        # 处理所有添加功能，使用ModelForm来实现
        Add_Model_Form = self.get_model_form_class(True,request,None,*args,**kwargs)
        if request.method == 'GET':
            form = Add_Model_Form(request=request)
            return render(request, 'stark/change.html', {'form': form,'starkclass':self})
        form = Add_Model_Form(request=request,data=request.POST)
        if form.is_valid():
            obj=self.save(request,form,False,*args,**kwargs)
            # obj=form.save()
            pop_post_id=request.GET.get('pop_id')
            if pop_post_id:
                res={'pop_post_id':pop_post_id,'pk':obj.pk,'obj':str(obj)}
                return render(request,'stark/pop.html',res)

            return redirect(self.reverse_changelist_url(*args,**kwargs))
        return render(request, 'stark/change.html', {'form': form})

    def change_view(self, request,pk,*args,**kwargs):
        """
        处理所有修改表单
        :param request:
        :param pk:
        :return:
        """
        Edit_Model_Form = self.get_model_form_class(False,request,pk,*args,**kwargs)
        obj = self.model_class.objects.filter(pk=pk).first()
        if not obj:
            return HttpResponse('该用户不存在')
        if request.method == 'GET':
            form = Edit_Model_Form(request,instance=obj)
            return render(request, 'stark/change.html', {'form': form})
        form = Edit_Model_Form(request=request,data=request.POST,instance=obj)
        if form.is_valid():
            self.save(request,form,True,*args,**kwargs)
            return redirect(self.reverse_changelist_url(*args,**kwargs))
        filter_horizontal=self.get_filter_horizontal()
        el=EditList(self,request,pk,filter_horizontal,*args,**kwargs)#修改和添加共用一个页面，所以form没有进行封装
        return render(request, 'stark/change.html', {'form': form,'el':el})

    def del_view(self, request,pk,*args,**kwargs):
        """
        处理删除表弟
        :param request:
        :param pk:
        :return:
        """
        obj = self.model_class.objects.filter(pk=pk).first()
        if not obj:
            return HttpResponse('该内容不存在')
        if request.method == 'GET':
            return render(request, 'stark/delete.html', {'obj': obj, 'cancel_url': self.reverse_changelist_url(*args,**kwargs)})
        self.model_class.objects.filter(pk=pk).delete()
        return redirect(self.reverse_changelist_url(*args,**kwargs))

    def wrapper(self, func):  # 将视图函数加上装饰器，这样可以在处理视图之前之后都可以加上一定的功能
        @functools.wraps(func)  # 保留原函数的信息
        def inner(request, *args, **kwargs):
            self.request = request  # 将request传给当前对象，在处理视图函数之前
            BaseRequestForm(request)
            BaseRequestModelForm(request)
            return func(request, *args, **kwargs)

        return inner

    def get_urls(self):
        urlpatterns = [
            re_path('list/$', self.wrapper(self.changelist_view), name=self.get_list_url_name ),
            re_path('add/$', self.wrapper(self.add_view), name=self.get_add_url_name),
            re_path('(?P<pk>\d+)/change/$', self.wrapper(self.change_view), name=self.get_edit_url_name),
            re_path('(?P<pk>\d+)/del/$', self.wrapper(self.del_view), name=self.get_del_url_name),

        ]
        extra_urls = self.extra_urls()

        if extra_urls:
            urlpatterns.extend(extra_urls)

        return urlpatterns

    def extra_urls(self):  # 用于扩展url 返回的是一个列表，一次性扩展多个值
        pass

    @property
    def urls(self):

        return self.get_urls()

class ChangeList(object):
    """
    将显示页面的数据封在该对象中
    """

    def __init__(self, stark_class, search_list, q, page, queryset,header_list,body_list,*args,**kwargs):
        self.stark_class = stark_class
        self.action_list = [{'name': func.__name__, 'attr_dict': func.attr_dict} for func in
                            stark_class.get_action_list()]  ##封装action_list
        self.search_list = search_list
        self.list_editable=stark_class.get_list_editable()
        self.q = q
        self.page = page
        self.add_btn = stark_class.get_add_btn(stark_class.request,*args,**kwargs)
        self.queryset = queryset
        self.header_list=header_list
        self.body_list=body_list
        self.list_display = stark_class.get_list_display()
        self.args=args,
        self.kwargs=kwargs


    def list_filter_rows(self):
        #####################组合搜索 可以通过yield返回一个个的RowQueryset对象#############
        list_filter = self.stark_class.get_list_filter()  # 获取对象列表['Option()','Option()']
        for option in list_filter:
            _field_obj = self.stark_class.model_class._meta.get_field(option.field)  # 取到每一个字段对象
            row_queryset = option.get_queryset(_field_obj, self.stark_class.model_class,
                                               self.stark_class)  # 取到数据库中对应的一行数据
            yield row_queryset

class EditList(object):
    """
    将修改页面的数据封到该对象中
    """
    def __init__(self,stark_class,request,pk,filter_horizontal,*args,**kwargs):
        self.stark_class=stark_class
        self.request=request
        self.pk=pk
        self.filter_horizontal=filter_horizontal
        self.args=args
        self.kwargs=kwargs



