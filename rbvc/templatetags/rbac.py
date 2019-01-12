from django import template
from django.conf import settings
import re

register = template.Library()


@register.inclusion_tag(filename='rbac/menu.html')
def show_menu(request):
    # 先从配置文件中找到存放菜单信息的session key是什么
    menu_key = getattr(settings, 'MENU_SESSION_KEY', 'menu_dict')
    # 从session中取出菜单信息
    menu_dict = request.session[menu_key]
    # menu_list = menu_dict.values()
    # 对菜单按照权重(weight)排序
    menu_list = sorted(menu_dict.values(), key=lambda x: x['weight'], reverse=True)
    # 给当前的菜单添加active样式
    for menu in menu_list:
        menu['class'] = 'hide'  # 默认让菜单上所有的body隐藏
        for child in menu['children']:
            # 当二级菜单和当前访问的URL匹配上
            if re.match(r'^{}$'.format(child['url']), request.path_info):
                # 这个二级菜单加上一个active样式
                child['class'] = 'active'
                menu['class'] = ''  # 让它的父级菜单展开
                break
    return {'menu_list': menu_list}


# 生成面包屑导航
@register.inclusion_tag(filename='rbac/bread_crumb.html')
def bread_crumb(request):
    bread_crumb_list = request.bread_crumb
    return {'bread_crumb_list': bread_crumb_list}


# 自定义filter 实现按钮是否显示
@register.filter()
def has_permission(request, value):
    key = getattr(settings, 'PERMISSION_SESSION_KEY', 'permission_dict')
    # 当前登录的这个人他的权限列表是什么
    permission_dict = request.session.get(key, {})
    return value in permission_dict


# 判断菜单的高亮显示
@register.filter()
def is_this_menu(request, menu_id):
    m_id = request.GET.get('menu_id', 0)
    return str(m_id) == str(menu_id)
