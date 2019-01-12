from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from django.conf import settings
import re


class RBACMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 获取当前请求的URL
        current_url = request.path_info
        # 判断当前访问的URL在不在白名单中
        for url in getattr(settings, 'WHITE_URLS', []):
            if re.match(r'^{}$'.format(url), current_url):
                # 如果是白名单的URL直接放行
                return
            # 判断当前访问的URL在不在白名
        key = getattr(settings, 'PERMISSION_SESSION_KEY', 'permission_dict')
        # 当前登录的这个人他的权限是什么
        permission_dict = request.session.get(key, [])
        # 为面包屑导航准备数据
        request.bread_crumb = [{'title': '首页', 'url': '#'}]
        # 从session中取到菜单的字典
        menu_key = getattr(settings, 'MENU_SESSION_KEY', 'menu_dict')
        # 从session中取出菜单信息
        menu_dict = request.session[menu_key]
        # 因为django URL存在模糊匹配, 所以校验权限的时候也要用正则去匹配
        for item in permission_dict.values():
            if re.match('^{}$'.format(item['url']), current_url):
                # 有权限
                # 如果根据权限找到它的父级菜单是谁, 塞到request.bread_crumb
                menu_title = menu_dict[str(item['menu_id'])]['title']
                request.bread_crumb.append({'title': menu_title})
                return None
        else:
            return HttpResponse('没有权限')
