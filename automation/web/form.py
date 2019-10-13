from web import models
from django import forms
from utils import auth



class User(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = '__all__'

        widgets = {
            "password":forms.PasswordInput(attrs={"class":"form-control"})  #密码显示密文
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })

class Host(forms.ModelForm):
    class Meta:
        model = models.Host
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for field in self.fields.values():
            field.widget.attrs.update(
                {'class':'form-control'}
            )

class Init(forms.ModelForm):
    class Meta:
        model = models.Init
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for field in self.fields.values():
            field.widget.attrs.update(
                {'class':'form-control'}
            )

class Initlog(forms.ModelForm):
    class Meta:
        model = models.InitLog
        fields = "__all__"
        exclude = ['result']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class':'form-control'
            })

class Project(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = "__all__"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class':'form-control'
            })

class Cron(forms.ModelForm):
    m = []
    h = [('*','*'),]
    d = [('*','*'),]
    mon = [('*','*'),]
    w = [('*','*'),('1','星期一'),('2','星期二'),('3','星期三'),('4','星期四'),('5','星期五'),('6','星期六'),('0','星期日')]
    for i in range(60):
        if i > 0:
            m.append(('*/{}'.format(i),'*/{}'.format(i)))
        m.append((i, i))
    for i in range(24):
        h.append((i,i))
        h.append(('*/{}'.format(i),'*/{}'.format(i)))
    for i in range(1,32):
        d.append((i,i))
        d.append(('*/{}'.format(i),'*/{}'.format(i)))
    for i in range(1,13):
        mon.append((i,i))
        mon.append(('*/{}'.format(i),'*/{}'.format(i)))
    minute = forms.ChoiceField(m,label='分钟')
    hour = forms.ChoiceField(h,label='小时')
    day = forms.ChoiceField(d,label='日')
    month = forms.ChoiceField(mon,label='月')
    weekday = forms.ChoiceField(w,label='周')
    class Meta:
        model = models.Cron
        fields = ['minute','hour','day','month','weekday','name','hosts_list','job','user','note']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class':'form-control'
            })

class FileForm(auth.NewModelForm):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),label="上传文件")

    class Meta:
        model=models.Issue
        fields=["project","file_field"]

class GitForm(auth.NewModelForm):

    class Meta:
        model=models.Issue
        fields=["project","backup"]