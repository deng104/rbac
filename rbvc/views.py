from django.shortcuts import render, redirect, HttpResponse
from rbvc.models import UserInfo, Role, Menu, Permission
from rbvc.utils import permission, reload_routes
from rbvc.forms import RoleForm, MenuForm, PermissionForm
from django.urls import reverse
from django.forms import modelformset_factory, formset_factory
import logging

# 生成一个以当前模块名为名字的logger实例
logger = logging.getLogger(__name__)
# 生成一个名字是collect的logger实例
collect_logger = logging.getLogger('collect')


# Create your views here.


# 登录
def login(request):
    error_msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = UserInfo.objects.filter(username=username, password=password).first()
        if user_obj:
            # 登录成功
            permission.init(request, user_obj)
            return redirect('/customer/list/')
        else:
            error_msg = '用户名或密码错误'
    return render(request, 'login.html', {'error_msg': error_msg})


# 注销
def logout(request):
    request.session.flush()
    return redirect('/login/')


# 角色列表
def role_list(request):
    data = Role.objects.all()
    return render(request, 'role_list.html', {'role_list': data})


# 编辑和添加
def op_role(request, edit_id=None):
    role_obj = Role.objects.filter(pk=edit_id).first()
    form_obj = RoleForm(instance=role_obj)
    if request.method == 'POST':
        form_obj = RoleForm(request.POST, instance=role_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('role_list'))
    return render(request, 'op_role.html', {'form_obj': form_obj, 'edit_id': edit_id})


# 删除角色
def role_del(request, del_id=None):
    Role.objects.filter(pk=del_id).delete()
    return redirect(reverse('role_list'))


# 菜单列表
def menu_list(request):
    menu_queryset = Menu.objects.all()
    menu_id = request.GET.get('menu_id')
    if menu_id:
        permission_queryset = Permission.objects.filter(menu_id=menu_id)
    else:
        permission_queryset = Permission.objects.all()
    return render(request, 'menu_list.html', {'menu_list': menu_queryset, 'permission_list': permission_queryset})


# 添加和编辑
def op_menu(request, edit_id=None):
    menu_obj = Menu.objects.filter(pk=edit_id).first()
    form_obj = MenuForm(instance=menu_obj)
    if request.method == 'POST':
        form_obj = MenuForm(request.POST, instance=menu_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('menu_list'))
    return render(request, 'op_menu.html', {'form_obj': form_obj, 'edit_id': edit_id})


# 删除
def menu_del(request, del_id=None):
    Menu.objects.filter(pk=del_id).delete()
    return redirect(reverse('menu_list'))


# 添加和编辑
def op_permission(request, edit_id=None):
    permission_obj = Permission.objects.filter(pk=edit_id).first()
    form_obj = PermissionForm(instance=permission_obj)
    if request.method == 'POST':
        form_obj = PermissionForm(request.POST, instance=edit_id)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('menu_list'))
    return render(request, 'op_permission.html', {'form_obj': form_obj, 'edit_id': edit_id})


# 删除
def permission_del(request, del_id=None):
    Permission.objects.filter(pk=del_id).delete()
    next_url = request.GET.get('next', reverse('menu_list'))
    return redirect(next_url)


# 权限录入
def permission_entry(request):
    # 项目里面所有的路由
    all_urls = reload_routes.get_all_url_dict(ignore_namespace_list=['admin', ])
    # 数据中权限表中储存的所有路由
    all_permissions = Permission.objects.all()
    # 用集合去判断
    # 项目中所有的路由集合
    project_url_set = set(all_urls.keys())
    # 数据库中permission表中的路由集合
    db_url_set = set([i.name for i in all_permissions])
    # 项目中由, 数据库中没有的
    only_in_project = project_url_set - db_url_set
    # 这些路由应该是等待添加到数据库中权限表里面的数据
    AddFormset = formset_factory(PermissionForm, extra=0)
    add_formset_obj = AddFormset(initial=[v for k, v in all_urls.items() if k in only_in_project])
    # =============================================================
    # 项目中存在, Permission表中也存在的路由数据
    project_db_set = project_url_set & db_url_set
    # 从Permission数据库中查询符合要求的路由信息
    urls = Permission.objects.filter(name__in=project_db_set)
    # 造一个ModelFormet
    ModelFormSet = modelformset_factory(Permission, PermissionForm, extra=0)
    edit_formset_obj = ModelFormSet(queryset=urls)
    if request.method == 'POST':
        # 取出URL中的post_type参数
        post_type = request.GET.get('post_type', None)
        if post_type == 'add':
            add_formset_obj = AddFormset(request.POST)
            if add_formset_obj.is_valid():
                objs = (Permission(**item) for item in add_formset_obj.cleaned_data)
                Permission.objects.bulk_create(objs)

        if post_type == 'edit':
            edit_formset_obj = ModelFormSet(request.POST, queryset=urls)
            if edit_formset_obj.is_valid():
                edit_formset_obj.save()

        return redirect(reverse('permission_entry'))
    # 获取只在permission表中存在但是不在项目中的那些路由
    only_in_db = db_url_set - project_url_set
    del_urls = Permission.objects.filter(name__in=only_in_db)
    del_formset_obj = ModelFormSet(queryset=del_urls)
    return render(request,
                  'permission_entry.html',
                  {
                      'add_formset_obj': add_formset_obj,
                      'edit_formset_obj': edit_formset_obj,
                      'del_formset_obj': del_formset_obj,
                  }
                  )


# 批量权限更新
def permission_update(request):
    # 取出所有的用户数据
    all_user = UserInfo.objects.all()
    # 取出所有的角色数据
    all_role = Role.objects.all()
    # 取出所有的菜单数据
    all_menu = Menu.objects.all()
    # 当在页面上点击用户列表里面的用户名时会携带user_id发来请求
    user_id = request.GET.get('user_id', None)
    user_obj = UserInfo.objects.filter(pk=user_id).first()
    # 当在页面上点击角色列表里面的角色时会携带role_id发来请求
    role_id = request.GET.get('role_id', None)
    role_obj = Role.objects.filter(pk=role_id).first()
    if request.method == 'POST':
        post_type = request.POST.get('post_type', None)
        # 选中用户更新对应的角色
        if user_id and post_type == 'role':
            role_ids = request.POST.getlist('role_id')
            user_obj.roles.set(Role.objects.filter(id__in=role_ids))
            logger.info('更新了{}的角色'.format(user_obj.username))

        # 选中角色更新对应的权限
        if role_id and post_type == 'permission':
            permission_ids = request.POST.getlist('permission_id')
            role_obj.permissions.set(Permission.objects.filter(id__in=permission_ids))
            collect_logger.info('又来更新权限信息了...')

    return render(
        request,
        'permission_update.html',
        {
            'all_user': all_user,
            'all_role': all_role,
            'all_menu': all_menu,
            'user_obj': user_obj,
            'role_obj': role_obj,
        }
    )

