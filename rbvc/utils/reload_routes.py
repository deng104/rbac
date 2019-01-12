from django.conf import settings
from django.utils.module_loading import import_string
from django.urls import RegexURLResolver
from collections import OrderedDict


def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    for item in urlpatterns:
        # 如果是嵌套的URL
        if isinstance(item, RegexURLResolver):
            if pre_namespace:
                if item.namespace:
                    namespace = '{}:{}'.format(pre_namespace, item.namespace,)
                else:
                    namespace = pre_namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None
            # 如果还有嵌套的三级、四级...路由就递归的执行
            recursion_urls(namespace, pre_url + item.regex.pattern, item.url_patterns, url_ordered_dict)
        # 普通URL
        else:
            if pre_namespace:
                name = '{}:{}'.format(pre_namespace, item.name,)
            else:
                name = item.name
            if not item.name:
                raise Exception('URL路由中必须设置name属性')
            url = pre_url + item.regex.pattern
            # 把分析出来的每一条路由都以 命名空间:路由别名 为key 存到有序字典里
            url_ordered_dict[name] = {'name': name, 'url': url.replace('^', '').replace('$', '')}


def get_all_url_dict(ignore_namespace_list=None):
    """获取路由中"""
    ignore_list = ignore_namespace_list or []
    # 生成一个有序的字典
    url_ordered_dict = OrderedDict()
    # 导入Django的路由配置
    root_url_conf = import_string(settings.ROOT_URLCONF)
    # 生成一个空列表
    urlpatterns = []
    # for循环项目所有的路由
    for item in root_url_conf.urlpatterns:
        if isinstance(item, RegexURLResolver) and item.namespace in ignore_list:
            continue
        urlpatterns.append(item)
    # 调用上方的函数分析并收集项目中的路由
    recursion_urls(None, '/', urlpatterns, url_ordered_dict)
    return url_ordered_dict
