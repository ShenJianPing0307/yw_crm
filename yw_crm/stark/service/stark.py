from .base_stark import BaseStark
from django.urls import path

class ModelStarkMapping(object):

    def __init__(self,model_class,stark_class,prev):
        self.model_class=model_class
        self.stark_class=stark_class
        self.prev=prev

class AdminSite(object):

    def __init__(self):
        self._registry=[]
        self.app_name='stark'
        self.namespace='stark'

    def register(self,model_class,stark_class=None,prev=None):#引入stark_class类是为了扩展其它功能
        #self._registry[model_class] = model_class没有意义
        if not stark_class:
            stark_class=BaseStark

        self._registry.append(ModelStarkMapping(model_class,stark_class(model_class,self,prev),prev))
        #self._registry.append({'model':model_class,'stark_class':stark_class(model_class,self,prev),prev})
        # for k,v in self._registry.items():
        #     print(k,v)0
        """
        _registry={
        'UserInfo':BaseStark(UserInfo,site) 封装UserInfo类和site
        'Role':RoleStark(Role,site) 封装 Role类和site
        }
        """

    def get_urls(self):
        urlpatterns=[]

        for item in self._registry: #循环得到的是每一个ModelStarkMapping对象
            app_label=item.model_class._meta.app_label
            model_name=item.model_class._meta.model_name
            if item.prev:
                temp = path('%s/%s/%s/' % (app_label, model_name,item.prev), (item.stark_class.urls, None, None))
            else:
                temp = path('%s/%s/' % (app_label, model_name,), (item.stark_class.urls, None, None))
            urlpatterns.append(temp)
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(),self.app_name,self.namespace

site=AdminSite()