from django.contrib import admin
from rbvc.models import UserInfo, Permission, Role, Menu

# Register your models here.


class PermissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'show', 'menu', 'name']  # 控制admin页面显示哪些字段
    list_editable = ['url', 'show', 'menu', 'name']  # 可以直接在admin页面编辑的字段


# 自定制一个权限类的admin
class MenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'weight']  # 控制admin页面显示哪些字段
    list_editable = ['icon', 'weight']  # 可以之间在admin页面编辑的字段


admin.site.register(UserInfo)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(Role)
admin.site.register(Menu, MenuAdmin)
