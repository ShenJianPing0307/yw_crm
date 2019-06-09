from stark.service.stark import site
from crm import models
from crm.stark_config.UserInfoStark import UserInfoStark
from crm.stark_config.DepartmentStark import DepartmentStark
from crm.stark_config.CustomerStark import PersonalCustomerStark
from crm.stark_config.ProductStark import ProductStark
from crm.stark_config.ConsultantRecordStark import PersonalConsultantRecordStark
from crm.stark_config.PaymentRecordStark import PaymentRecordStark,AuditPaymentStark
from crm.stark_config.ProductParameterStark import ProductParameterStark
from crm.stark_config.ProcedureStark import ProcedureStark
from crm.stark_config.WorkShopStark import WorkShopStark
from crm.stark_config.ProductAuditStark import ProductAuditStark
from crm.stark_config.OrderStark import OrderStark,CheckOrderStark,CustomerOrderStark











site.register(models.UserInfo,UserInfoStark)
site.register(models.DepartMent,DepartmentStark)
site.register(models.Customer,PersonalCustomerStark,'per')
# site.register(models.Customer,CustomerStark)
site.register(models.Product,ProductStark)
site.register(models.ConsultantRecord,PersonalConsultantRecordStark,'per')
# site.register(models.ConsultantRecord,ConsultantRecordStark)
# site.register(models.PaymentRecord,PersonalPaymentRecordStark,'per')
site.register(models.Order,CustomerOrderStark)
site.register(models.ProductParameter,ProductParameterStark)
site.register(models.Procedure,ProcedureStark)
site.register(models.ProductAudit,ProductAuditStark)

site.register(models.WorkShop,WorkShopStark)
# site.register(models.ProductAudit,ProductAuditStark)
# site.register(models.Order,PersonOrderStark,'per')
site.register(models.Order,OrderStark)
site.register(models.Order,CheckOrderStark)



site.register(models.PaymentRecord,PaymentRecordStark)
site.register(models.PaymentRecord,AuditPaymentStark)





