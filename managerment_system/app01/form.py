from app01 import models
from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError

class UserForm(forms.Form):
    username = forms.CharField(max_length=32,min_length=6,label='用户名',
                               error_messages={'required':'这个字段必须填写','max_length':'最大不能超过32位','min_length':'最小不能低于6位'})
    password = forms.CharField(max_length=32,min_length=6,label='密码',
                               error_messages={'required':'这个字段必须填写','max_length':'最大不超过32位','min_length':'最小不少于6位'},widget=forms.widgets.PasswordInput)
    r_password = forms.CharField(max_length=32,min_length=6,label='确认密码',
                                 error_messages={'required':'这个字段必须填写','max_length':'最大不超过32位','min_length':'最小不低于6位'},widget=widgets.PasswordInput)
    email = forms.EmailField(label='邮箱',error_messages={'required':'这个字段必须填写','invalid':'邮箱格式不正确'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        obj = models.UserInfo.objects.filter(username=username).first()
        if obj:
            raise ValidationError('用户名已经存在')
        else:
            return username

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        if pwd.isdecimal():
            raise ValidationError('密码不能全为数字')
        else:
            return pwd

    def clean(self):
        pwd = self.cleaned_data.get('password')
        r_pwd = self.cleaned_data.get('r_password')
        if pwd != r_pwd:
            self.add_error('r_password','两次密码不一致')
        else:
            return self.cleaned_data

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })

from multiselectfield.forms.fields import MultiSelectFormField

class Customer(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            print(field,type(field))
            if isinstance(field, MultiSelectFormField) is False:
                field.widget.attrs.update({
                    'class': 'form-control'
                })

class ConsultRecord(forms.ModelForm):
    class Meta:
        model = models.ConsultRecord
        fields = '__all__'
        exclude = ['delete_status']
        error_messages = {
            'customer':{'required':'不能为空'},
            'note':{'required':'不能为空'},
            'status':{'required':'不能为空'},
            'custconsultantomer':{'required':'不能为空'},
            'date':{'required':'不能为空'},
        }

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['consultant'].queryset = models.UserInfo.objects.filter(pk=request.user.pk)
        self.fields['customer'].queryset = models.Customer.objects.filter(consultant=request.user)

        for field in self.fields.values():
            print(field)
            field.widget.attrs.update({
                'class':'form-control'
            })

class ClassList(forms.ModelForm):
    class Mate:
        models = models.ClassList
        fields = '__all__'

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class':'form-control'
            })