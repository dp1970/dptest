from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,User,PermissionsMixin
from multiselectfield import MultiSelectField

# Create your models here.

course_choices = (('LinuxL', 'Linux中高级'),
                  ('PythonFullStack', 'Python高级全栈开发'),)

class_type_choices = (('fulltime', '脱产班',),
                      ('online', '网络班'),
                      ('weekend', '周末班',),)

source_type = (('qq', "qq群"),
               ('referral', "内部转介绍"),
               ('website', "官方网站"),
               ('baidu_ads', "百度推广"),
               ('office_direct', "直接上门"),
               ('WoM', "口碑"),
               ('public_class', "公开课"),
               ('website_luffy', "路飞官网"),
               ('others', "其它"),)

enroll_status_choices = (('signed', "已报名"),
                         ('unregistered', "未报名"),
                         ('studying', '学习中'),
                         ('paid_in_full', "学费已交齐"))

seek_status_choices = (('A', '近期无报名计划'), ('B', '1个月内报名'), ('C', '2周内报名'), ('D', '1周内报名'),
                       ('E', '定金'), ('F', '到班'), ('G', '全款'), ('H', '无效'),)
pay_type_choices = (('deposit', "订金/报名费"),
                    ('tuition', "学费"),
                    ('transfer', "转班"),
                    ('dropout', "退学"),
                    ('refund', "退款"),)

attendance_choices = (('checked', "已签到"),
                      ('vacate', "请假"),
                      ('late', "迟到"),
                      ('absence', "缺勤"),
                      ('leave_early', "早退"),)

score_choices = ((100, 'A+'),
                 (90, 'A'),
                 (85, 'B+'),
                 (80, 'B'),
                 (70, 'B-'),
                 (60, 'C+'),
                 (50, 'C'),
                 (40, 'C-'),
                 (0, ' D'),
                 (-1, 'N/A'),
                 (-100, 'COPY'),
                 (-1000, 'FAIL'),)

class UserInfo(AbstractUser):
    roles = models.ManyToManyField('Role')

    def __str__(self):
        return self.username

class Customer(models.Model):
    """
    客户表（最开始的时候大家都是客户，销售就不停的撩你，你还没交钱就是个客户）
    """
    qq = models.CharField(verbose_name='QQ', max_length=64, unique=True, help_text='QQ号必须唯一')
    qq_name = models.CharField('QQ昵称', max_length=64, blank=True, null=True)
    name = models.CharField('姓名', max_length=32, blank=True, null=True, help_text='学员报名后，请改为真实姓名')
    sex_type = (('male', '男'), ('female', '女'))
    sex = models.CharField("性别", choices=sex_type, max_length=16, default='male', blank=True, null=True) #存的是male或者female，字符串
    birthday = models.DateField('出生日期', default=None, help_text="格式yyyy-mm-dd", blank=True, null=True)

    phone = models.CharField('手机号', blank=True, null=True,max_length=32)
    # phone = models.CharField('手机号', blank=True, null=True)
    source = models.CharField('客户来源', max_length=64, choices=source_type, default='qq')

    introduce_from = models.ForeignKey('self', verbose_name="转介绍自学员", blank=True, null=True)  #self指的就是自己这个表，和下面写法是一样的效果


    # introduce_from = models.ForeignKey('Customer', verbose_name="转介绍自学员", blank=True, null=True,on_delete=models.CASCADE)
    course = MultiSelectField("咨询课程", choices=course_choices) #多选，并且存成一个列表的格式
    # course = models.CharField("咨询课程", choices=course_choices) #如果你不想用上面的多选功能，可以使用Charfield来存
    class_type = models.CharField("班级类型", max_length=64, choices=class_type_choices, default='fulltime')
    customer_note = models.TextField("客户备注", blank=True, null=True, )
    status = models.CharField("状态", choices=enroll_status_choices, max_length=64, default="unregistered",help_text="选择客户此时的状态") #help_text这种参数基本都是针对admin应用里面用的

    date = models.DateTimeField("咨询日期", auto_now_add=True)

    last_consult_date = models.DateField("最后跟进日期", auto_now_add=True) #考核销售的跟进情况，如果多天没有跟进，会影响销售的绩效等
    next_date = models.DateField("预计再次跟进时间", blank=True, null=True) #销售自己大概记录一下自己下一次会什么时候跟进，也没啥用

    #用户表中存放的是自己公司的所有员工。
    consultant = models.ForeignKey('UserInfo', verbose_name="销售", blank=True, null=True)

    def __str__(self):
        return self.name+":"+self.qq  #主要__str__最好是个字符串昂，不然你会遇到很多的坑，还有我们返回的这两个字段填写数据的时候必须写上数据，必然相加会报错，null类型和str类型不能相加等错误信息。

    # def get_classlist(self):  #当我们通过self.get_classlist的时候，就拿到了所有的班级信息，前端显示的时候用
    #
    #     l=[]
    #     for cls in self.class_list.all():
    #         l.append(str(cls))
    #     # return mark_safe(",".join(l)) #纯文本，不用mark_safe也可以昂
    #     return ",".join(l) #纯文本，不用mark_safe也可以昂

class Campuses(models.Model):
    """
    校区表
    """
    name = models.CharField(verbose_name='校区', max_length=64)
    address = models.CharField(verbose_name='详细地址', max_length=512, blank=True, null=True)

    def __str__(self):
        return self.name

class ConsultRecord(models.Model):
    customer = models.ForeignKey('Customer',verbose_name='所咨询的客户')
    note = models.TextField('跟进内容',null=True,blank=True)
    status = models.CharField('跟进状态',choices=seek_status_choices,max_length=8)
    consultant = models.ForeignKey('UserInfo',verbose_name='跟进人')
    date = models.DateTimeField('跟进日期')
    delete_status = models.BooleanField('删除状态',default=False)

class Role(models.Model):
    name = models.CharField(max_length=32)
    permissions = models.ManyToManyField('Permission')
    def __str__(self):
        return self.name

class Menu(models.Model):
    name = models.CharField(max_length=32,verbose_name='一级菜单')

class Permission(models.Model):
    name = models.CharField(max_length=32)
    url = models.CharField(max_length=128)
    menu = models.ForeignKey('Menu',null=True,blank=True)
    pid = models.ForeignKey('self',null=True)

    # is_menu = models.BooleanField(default=False,verbose_name='是否是菜单')

    def __str__(self):
        return self.name


class ClassList(models.Model):
    """
    班级表
    """
    course = models.CharField("课程名称", max_length=64, choices=course_choices)
    semester = models.IntegerField("学期") #python20期等
    campuses = models.ForeignKey('Campuses', verbose_name="校区",on_delete=models.CASCADE)
    price = models.IntegerField("学费", default=10000)
    memo = models.CharField('说明', blank=True, null=True, max_length=100)
    start_date = models.DateField("开班日期")
    graduate_date = models.DateField("结业日期", blank=True, null=True)

    teachers = models.ManyToManyField('UserInfo', verbose_name="老师")

    class_type = models.CharField(choices=class_type_choices, max_length=64, verbose_name='班额及类型', blank=True,null=True)

    def __str__(self):
        return "{}{}({})".format(self.get_course_display(), self.semester, self.campuses)