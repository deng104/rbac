"""
RBAC组件
权限相关的模块
"""
from django.conf import settings


def init(request, user_obj):
    """
    根据当前登录的用户初始化权限信息和菜单信息, 保存到session中
    :param request: 请求对象
    :param user_obj: 登录的用户对象
    :return:
    """
    # 登陆成功, 将当前用户的权限信息查询出来
    queryset = user_obj.roles.all().filter(permissions__isnull=False).values(
        'permissions__url',  # 权限的URL
        'permissions__title',  # 权限的名称
        'permissions__name',  # 路由别名
        'permissions__show',  # 权限是否显示
        'permissions__menu_id',  # 菜单的id
        'permissions__menu__title',  # 菜单的标题
        'permissions__menu__icon',  # 菜单的图标
        'permissions__menu__weight',  # 菜单的权重
    ).distinct()
    # 先取到权限列表
    permission_dict = {}
    # {
    #   'web:customer_list': {'url': item['permissions__url'], 'menu_id': item['permissions__menu_id']}
    # }
    # 存放菜单信息的列表
    menu_dict = {}
    for item in queryset:
        dict_key = item['permissions__name']
        permission_dict[dict_key] = {'url': item['permissions__url'], 'menu_id': item['permissions__menu_id']}  # 唔够访问的权限表
        p_id = item['permissions__menu_id']
        if p_id not in menu_dict:
            menu_dict[p_id] = {
                'id': p_id,
                'title': item['permissions__menu__title'],
                'icon': item['permissions__menu__icon'],
                'weight': item['permissions__menu__weight'],
                'children': [{'title': item['permissions__title'], 'url': item['permissions__url'], 'show': item['permissions__show']}]
            }
        else:
            menu_dict[p_id]['children'].append({'title': item['permissions__title'], 'url': item['permissions__url'], 'show': item['permissions__show']})
    # 将权限信息保存到session数据中
    permission_key = getattr(settings, 'PERMISSION_SESSION_KEY', 'permission_list')
    menu_key = getattr(settings, 'MENU_SESSION_KEY', 'menu_dict')
    request.session[permission_key] = permission_dict
    # 存菜单信息到session数据中
    request.session[menu_key] = menu_dict
