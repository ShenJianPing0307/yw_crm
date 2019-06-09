from django.shortcuts import HttpResponse,render
import functools

class HandleView(object):

    def wrapper(self,func):
        @functools.wraps(func)  #保留原函数的信息
        def inner(*args,**kwargs):
            return func(*args,**kwargs)
        return inner

    def changelist_view(self,request):
        queryset=self.model_class.object.all()

        return render(request,'')

    def add_view(self,request):
        pass

    def change_view(self,request):
        pass

    def del_view(self,request):
        pass