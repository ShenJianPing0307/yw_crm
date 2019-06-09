from django.db import models
from rbac.models import UserInfo as RbacUserInfo

# Create your models here.

class UserInfo(RbacUserInfo):
    """
    员工表
    """
    name=models.CharField(max_length=32,verbose_name="真实姓名")
    phone=models.CharField(max_length=32,verbose_name='手机号')
    gender_choices=(
        (1,'男'),
        (2,'女')
    )
    gender=models.IntegerField(choices=gender_choices,verbose_name='性别')
    department=models.ForeignKey(to='DepartMent',verbose_name='所属部门',on_delete=models.CASCADE)

    def __str__(self):
        return "%s"%self.name


class DepartMent(models.Model):
    """
    部门表
    """
    name=models.CharField(max_length=32,verbose_name='部门')

    def __str__(self):
        return "%s"%self.name

class Customer(models.Model):
    """
    客户表
    """
    name=models.CharField(max_length=32,verbose_name='客户姓名')
    contact=models.CharField(max_length=32,verbose_name='联系方式',help_text='电话/微信等')
    status_choices=(
        (1,'已签合同'),
        (2,'未签合同')
    )
    status=models.IntegerField(choices=status_choices,verbose_name='状态',default=2)
    sales_choices=(
        (1,'官方网站'),
        (2,'销售宣传'),
        (3,'代理商')
    )
    source=models.IntegerField(choices=sales_choices,verbose_name='销售渠道',null=True,blank=True)
    referral_from=models.ForeignKey(to='self',
                                    verbose_name='自己内部顾客介绍',
                                    related_name='referral',
                                    null=True,
                                    blank=True,
                                    on_delete=models.CASCADE
                                   )
    product=models.ForeignKey(to='Product',verbose_name='咨询的产品',on_delete=models.CASCADE,null=True,blank=True)
    consultant=models.ForeignKey(to='UserInfo',verbose_name='咨询顾问',on_delete=models.CASCADE,limit_choices_to={'department__name':'项目部'})
    consultant_date=models.DateTimeField(verbose_name='咨询日期',null=True,blank=True)

    def __str__(self):
        return "%s"%self.name

class ConsultantRecord(models.Model):
    """
    客户跟进记录
    """
    customer = models.ForeignKey(verbose_name="所咨询客户", to='Customer',on_delete=models.CASCADE)
    consultant = models.ForeignKey(verbose_name="跟进人", to='UserInfo',limit_choices_to={'department__name':'项目部'},on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name="跟进日期", auto_now_add=True)
    content = models.TextField(verbose_name="跟进内容")

    def __str__(self):
        return "%s-%s"%(self.customer,self.content)

class Order(models.Model):
    customer = models.ForeignKey(verbose_name="客户", to='Customer',on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(to='Product',verbose_name='购买的产品',on_delete=models.CASCADE,null=True,blank=True)
    consultant = models.ForeignKey(verbose_name="咨询顾问", to='UserInfo',limit_choices_to={'department__name':'项目部'},on_delete=models.CASCADE,null=True,blank=True)
    quantity=models.IntegerField(verbose_name='产品数量',null=True,blank=True)
    check_date=models.DateTimeField(verbose_name='订单审核',null=True,blank=True)
    delivery_date=models.DateTimeField(verbose_name='交货日期',null=True,blank=True)
    note = models.TextField(verbose_name="备注", blank=True, null=True)

    def __str__(self):
        return "%s-%s-%s"%(self.customer,self.product,self.quantity)

class PaymentRecord(models.Model):
    """
    费用记录
    """
    order=models.ForeignKey(verbose_name='订单',to='Order',on_delete=models.CASCADE,null=True,blank=True)
    payment_type_choices = [

        (1, "定金"),
        (2, "尾款"),
        (3, "其它"),
    ]
    payment=models.IntegerField(choices=payment_type_choices,verbose_name='付款类型')
    paid_fee=models.CharField(max_length=16,verbose_name='费用')
    confirm_date = models.DateTimeField(verbose_name="确认日期",null=True, blank=True)
    confirm_user = models.ForeignKey(verbose_name="确认人", to='UserInfo',limit_choices_to={'department__name':'财务部'}, related_name='confirms', null=True, blank=True,
                                     on_delete=models.CASCADE)
    note = models.TextField(verbose_name="备注", blank=True, null=True)

    def __str__(self):
        return "%s-%s"%(self.payment,self.paid_fee)

class Product(models.Model):
    """
    产品
    """
    name=models.CharField(max_length=32,verbose_name='产品名称')
    price=models.CharField(max_length=16,verbose_name='产品价格')
    paramters=models.TextField(verbose_name='产品参数',null=True,blank=True)

    def __str__(self):
        return "%s"%self.name

class WorkShop(models.Model):
    """
    生产车间
    """
    name = models.CharField(max_length=16, verbose_name='车间',null=True,blank=True)

    def __str__(self):
        return "%s"%self.name

class ProductParameter(models.Model):
    """
    产品生产参数
    """
    workshop=models.ForeignKey(verbose_name='车间',to='WorkShop',on_delete=models.CASCADE)
    product = models.ForeignKey(to='Product',verbose_name='产品',on_delete=models.CASCADE,null=True,blank=True)
    technology=models.TextField(verbose_name='工艺参数',null=True,blank=True)
    quality=models.TextField(verbose_name='品质参数',null=True,blank=True)

    def __str__(self):
        return "%s-%s-%s-%s"%(self.workshop,self.product,self.technology,self.quality)

class Procedure(models.Model):
    """
    生产流程表
    """
    order=models.ForeignKey(to='Order',verbose_name='订单',on_delete=models.CASCADE,null=True,blank=True)
    workshop=models.ForeignKey(to='WorkShop',verbose_name='生产车间',on_delete=models.CASCADE)
    name=models.CharField(max_length=32,verbose_name='生产流程名称')
    status_choices=(
        (1,'未准备好'),
        (2,'已准备好')
    )
    status=models.IntegerField(choices=status_choices,default=2,verbose_name='生产流程状态')
    parent=models.ForeignKey(to='self',verbose_name='上一个流程',on_delete=models.CASCADE,null=True,blank=True)
    reason=models.TextField(verbose_name='原因',null=True,blank=True,help_text='如果该流程出现问题，请说明原因')
    product_choices=(
        (1,'未完成'),
        (2,'已完成')
    )
    product_status=models.IntegerField(choices=product_choices,verbose_name='产品完成状态',default=1)
    scedule=models.TextField(verbose_name='产品完成情况',null=True,blank=True)
    start=models.DateTimeField(verbose_name='开始时间',null=True,blank=True)
    end=models.DateTimeField(verbose_name='结束时间',null=True,blank=True)

    def __str__(self):
        return "%s"%self.order

class ProductAudit(models.Model):
    """
    产品审核
    """
    procedure=models.ForeignKey(to='Procedure',verbose_name='订单-产品信息',on_delete=models.CASCADE,null=True,blank=True)
    user=models.ForeignKey(to='UserInfo',verbose_name='审核人',limit_choices_to={'department__name':'总经理办'},on_delete=models.CASCADE,null=True,blank=True)
    audit_choices=(
        (1,'审核通过'),
        (2,'审核未通过')
    )
    status=models.IntegerField(choices=audit_choices,verbose_name='审核状态',default=2)
    reason=models.TextField(verbose_name='未通过原因',null=True,blank=True)
    audit_date=models.DateTimeField(verbose_name='审核时间',null=True,blank=True)

    def __str__(self):

        return "%s-%s"%(self.procedure,self.status)




