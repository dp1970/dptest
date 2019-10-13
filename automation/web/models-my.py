from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField

# Create your models here.

purpose_list = (('Web','web服务器'),('DB','mysql数据库'),('Cache','缓存数据库'))
environmental_list = (('Test','测试环境'),('Production','生产环境'),('准Production','准生产环境'))
status_list = (('Up','正常'),('Down','关机'),('Warning','维修'))
department_list = (('Test','测试'),('Development','研发'),('Operational Maintenance','运维'))
roles_list = (('User','普通用户'),('Admin','管理员'))
result_list = (('Success','成功'),('Faild','失败'))

class Host(models.Model):
    ip = models.CharField('主机地址',unique=True,help_text='格式:192.168.1.10')
    hostname = models.CharField('主机名',unique=True,help_text='格式:hostname')
    purpose = models.CharField('用途',choices=purpose_list)
    environmental = models.CharField('使用环境',choices=environmental_list)
    version = models.CharField('服务器版本',null=True,blank=True,help_text='格式:CentOS Linux release 7')
    user = models.ManyToManyField('UserInfo',verbose_name='登陆人',null=True,blank=True)
    status = models.CharField('服务器状态',choices=status_list)

class UserInfo(AbstractUser):
    roles = models.CharField('部门',choices=department_list)
    role = models.CharField('角色',choices=roles_list)

class Command(models.Model):
    command = models.CharField('执行操作',null=True,blank=True)
    user = models.CharField('执行人')
    result = models.CharField('执行结果',choices=result_list,null=True,blank=True)
    host = models.ManyToManyField('Host')
    date = models.DateField('执行时间',auto_now_add=True)

class Cron(models.Model):
    date = models.DateField('创建任务时间')
    job = models.CharField('计划任务')
    user = models.ManyToManyField('UserInfo',verbose_name='使用人')
    create = models.ManyToManyField('UserInfo',verbose_name='创建者')
    info = models.CharField('描述信息',max_length=150,null=True,blank=True)
    name = models.CharField('任务名称')

class Initialization(models.Model):
    path = models.CharField('脚本位置')
    user = models.ManyToManyField('UserInfo',verbose_name='创建人')
    date = models.DateField('创建时间')
    name = models.CharField('脚本名称')
    info = models.CharField('脚本描述',max_length=150,null=True,blank=True)

class Initialization_Log(models.Model):
    date = models.DateField('创建时间')
    user = models.ManyToManyField('UserInfo',verbose_name='执行人')
    script = models.ForeignKey('Initialization',verbose_name='执行的脚本')
    result = models.CharField('执行结果')

class Project(models.Model):
    name = models.CharField('项目名称')
    info = models.CharField('项目描述',max_length=150,null=True,blank=True)
    date = models.DateField('创建时间')
    host = models.ManyToManyField('Host',verbose_name='主机')
    path = models.CharField('项目位置')
    git = models.CharField('Git仓库地址')
    leader = models.ManyToManyField('UserInfo',verbose_name='项目负责人')
    devel = models.ManyToManyField('UserInfo',verbose_name='开发者')
    test = models.ManyToManyField('UserInfo',verbose_name='测试者')
    Operational_Maintenance = models.ManyToManyField('UserInfo',verbose_name='运维者')
    nginx_host = models.ForeignKey('Host','nginx主机')
    nginx_conf = models.CharField('nginx配置文件')

Release_list = (('success','发布成功'),('field','发布失败'),('running','发布中'),('waiting','等待测试'),('success_test','测试通过'),('rollback','回滚'))
class Release(models.Model):
    date = models.DateField('发布时间')
    publisher = models.ManyToManyField('UserInfo',verbose_name='发布人')
    project = models.ForeignKey('Project','项目名称')
    status = models.CharField('项目状态',choices=Release_list)
    info = models.CharField('描述信息',max_length=150,null=True,blank=True)
    version = models.CharField('发布版本')

class Host_Release(models.Model):
    publish = models.CharField('发布' )
    host = models.ManyToManyField('Host',verbose_name='发布的主机')
    status = models.CharField('发布状态',choices=Release_list)