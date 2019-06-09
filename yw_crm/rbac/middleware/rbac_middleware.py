from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render,HttpResponse,redirect
from django.conf import settings
import re

class PermissionMiddleWare(MiddlewareMixin):
    """
    权限控制的中间件
    """

    def process_request(self, request):
        """
        权限控制
        :param request:
        :return:
        """
        # 1. 获取当前请求URL
        current_url = request.path_info
        print('current_path',current_url)

        # 1.5 白名单处理
        for reg in settings.VALID_URL:
            if re.match(reg,current_url):
                return None

        # 2. 获取当前用户session中所有的权限
        permissions_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        if not permissions_dict:
            return redirect('/login/')

        # 3. 进行权限校验
        flag = False
        request.breadcrumb_list=[{'title':'首页','url':'/index/'}]
        for item in permissions_dict.values():
            id=item['id']
            pid=item['pid']
            reg = "%s$" % item['url']
            print('reg',reg)
            if re.match(reg, current_url):
                if pid: #访问的是添加客户网页
                    request.current_menu_id=pid #让它与可以作为权限菜单的客户列表挂钩
                    ###导航条自动生成
                    request.breadcrumb_list.extend([
                        {'title':permissions_dict[item['pname']]['title'],'url':permissions_dict[item['pname']]['url']},
                        {'title':item['title'],'url':item['url']}
                        ]
                    )
                else:
                    request.current_menu_id=id
                    ###导航条自动生成
                    request.breadcrumb_list.extend([
                        {'title':item['title'],'url':item['url']}
                    ]
                    )
                flag = True
                break
        if not flag:
            return HttpResponse('无权访问')





