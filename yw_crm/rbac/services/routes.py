import re
from collections import OrderedDict
from django.conf import settings
from django.utils.module_loading import import_string
# for django 1.0
# from django.urls import RegexURLResolver, RegexURLPattern
# for django 2.0
from django.urls.resolvers import URLResolver, URLPattern


def check_url_exclude(url):
    """
    排除一些特定的URL
    :param url:
    :return:
    """
    for regex in settings.AUTO_DISCOVER_EXCLUDE:
        if re.match(regex, url):
            return True


def recursion_urls(pre_namespace, pre_url, valid_urlpattern_list, url_ordered_dict):
    """
    递归的去获取URL
    :param pre_namespace: namespace前缀，以后用户拼接name
    :param pre_url: url前缀，以后用于拼接url
    :param urlpatterns: 路由关系列表
    :param url_ordered_dict: 用于保存递归中获取的所有路由
    :return:
    """
    for item in valid_urlpattern_list:
        if isinstance(item, URLPattern):  # 非路由分发，讲路由添加到url_ordered_dict
            if not item.name:
                continue
            if pre_namespace:
                name = "%s:%s" % (pre_namespace, item.name,)
            else:
                name = item.name
            if not item.name:
                raise Exception('URL路由中必须设置name属性')
            url = pre_url + str(item.pattern)
            url_ordered_dict[name] = {'name': name, 'url': url.replace('^', '').replace('$', '')}

        elif isinstance(item, URLResolver):  # 路由分发，递归操作
            if pre_namespace:
                if item.namespace:
                    namespace = "%s:%s" % (pre_namespace, item.namespace,)
                else:
                    namespace = pre_namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None
            recursion_urls(namespace, pre_url + str(item.pattern), item.url_patterns, url_ordered_dict)


def get_all_url_dict(ignore_namespace_list=None):
    """
    获取项目中所有的URL（必须有name别名）
    :return:
    """
    ignore_namespace_list=ignore_namespace_list or []
    valid_urlpattern_list=[]
    url_ordered_dict = OrderedDict()

    urlpatterns_list= import_string(settings.ROOT_URLCONF).urlpatterns  # from luff.. import urls

    for urlpattern in urlpatterns_list:
        if isinstance(urlpattern, URLResolver):
            if urlpattern.namespace in ignore_namespace_list:
                continue
            else:
                valid_urlpattern_list.append(urlpattern)
        valid_urlpattern_list.append(urlpattern)

    recursion_urls(None, '/', valid_urlpattern_list, url_ordered_dict)  # 递归去获取所有的路由

    return url_ordered_dict