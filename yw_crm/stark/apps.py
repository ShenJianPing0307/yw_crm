from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

class StarkConfig(AppConfig):
    name = 'stark'

    def ready(self):
        autodiscover_modules('stark') #自动发现每一个app下的stark.py模块文件


