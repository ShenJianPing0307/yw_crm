from django.db import models

class Menu(models.Model):
    """
    菜单表
    """
    title = models.CharField(verbose_name='菜单名称',max_length=32,unique=True)
    icon = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.title

class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name='权限标题', max_length=32)
    url = models.CharField(verbose_name='含正则的URL', max_length=128)
    name=models.CharField(verbose_name='url别名',max_length=64,unique=True) #控制权限到按钮
    parent=models.ForeignKey(verbose_name='父权限',to='self',null=True,blank=True,on_delete=models.CASCADE,limit_choices_to={'parent__isnull':True})#构建非菜单权限关系，菜单默认展开
    menu=models.ForeignKey(verbose_name='菜单',to='Menu',null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Role(models.Model):
    """
    角色
    """
    title = models.CharField(verbose_name='角色名称', max_length=32)
    permissions = models.ManyToManyField(verbose_name='拥有的所有权限', to='Permission', blank=True)


    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """
    用户表
    """
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    email = models.CharField(verbose_name='邮箱', max_length=32)
    roles = models.ManyToManyField(verbose_name='拥有的所有角色', to=Role, blank=True)

    class Meta:
        abstract=True

    def __str__(self):
        return self.username
