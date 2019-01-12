from django.db import models

# Create your models here.


# 菜单表
class Menu(models.Model):
    title = models.CharField(max_length=24, verbose_name='菜单名称', unique=True)
    icon = models.CharField(max_length=24, null=True, blank=True)  # 菜单图标
    weight = models.PositiveIntegerField(default=50, verbose_name='菜单权重')

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


# 权限表
class Permission(models.Model):
    title = models.CharField(verbose_name='标题', max_length=32)
    url = models.CharField(max_length=32)
    show = models.BooleanField(default=False)  # 是否能做菜单
    menu = models.ForeignKey(to='Menu', verbose_name='所属菜单')
    name = models.CharField(max_length=24, verbose_name='路由别名', unique=True, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '权限'
        verbose_name_plural = verbose_name


# 用户表
class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    roles = models.ManyToManyField(to='Role', null=True, blank=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


# 角色表
class Role(models.Model):
    title = models.CharField(max_length=32)
    permissions = models.ManyToManyField(to='Permission', null=True, blank=True)

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = verbose_name

    def show_permission(self):
        return '|'.join([i[0] for i in self.permissions.all().values_list('title')])

    def __str__(self):
        return self.title

