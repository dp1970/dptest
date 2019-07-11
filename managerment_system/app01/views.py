from django.shortcuts import render,HttpResponse,redirect
import os
from app01 import form,models
from django.contrib import auth
import random
from PIL import ImageFont,ImageDraw,Image
from managerment_system import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from app01 import page
from django.db.models import Q
# 获取权限组件
from rbac.service.permission_injection import privileges

# Create your views here.
# 注册
def regiest(request):
    if request.method == 'GET':
        form_obj = form.UserForm()
        return render(request,'regiest.html',{'form_obj':form_obj})
    else:
        print(request.POST)
        form_obj = form.UserForm(request.POST)
        if form_obj.is_valid():
            date = form_obj.cleaned_data
            date.pop('r_password')
            models.UserInfo.objects.create_user(**date)
            return redirect('login')
        else:
            return render(request,'regiest.html',{'form_obj':form_obj})

# 登录
def login(request):
    response_msg = {'code':None,'msg':None}
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        print(request.POST)
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        code = request.POST.get('code')

        # 校验验证码
        if code.upper() == request.session.get('valid_str').upper():
            user_obj = auth.authenticate(username=username,password=pwd)
            if user_obj:
                auth.login(request,user_obj)

                request.session['user'] = user_obj.username

                # 使用获取权限组件
                privileges(request,user_obj)

                response_msg['code'] = 100
                response_msg['msg'] = '登陆成功'
            else:
                response_msg['code'] = 400
                response_msg['msg'] = '账户名密码错误!'
        else:
            response_msg['code'] = 101
            response_msg['msg'] = '验证码错误'

        return JsonResponse(response_msg)

# 验证码图片
def code(request):
    def get_random_color():
        return (random.randint(0,255),random.randint(0,255),(random.randint(0,255)))
    img_obj = Image.new('RGB',(200,34),get_random_color())
    draw_obj =ImageDraw.Draw(img_obj)
    font_path = os.path.join(settings.BASE_DIR,'conf/font/NAUERT__.TTF')
    font_obj = ImageFont.truetype(font_path,18)
    sum_str = ''
    for i in range(6):
        a = random.choice([str(random.randint(0,9)),chr(random.randint(97,122)),chr(random.randint(65,90))])
        sum_str += a
    print(sum_str)
    draw_obj.text((64,10),sum_str,fill=get_random_color(),font=font_obj)

    width=300
    height=34
    for i in range(5):
        x1=random.randint(0,width)
        x2=random.randint(0,width)
        y1=random.randint(0,height)
        y2=random.randint(0,height)
        draw_obj.line((x1,y1,x2,y2),fill=get_random_color())
    # # 添加噪点
    for i in range(10):
        # 这是添加点，50个点
        draw_obj.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        # 下面是添加很小的弧线，看上去类似于一个点，50个小弧线
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw_obj.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    from io import BytesIO
    f = BytesIO()
    img_obj.save(f, 'png')
    data = f.getvalue()

    # 验证码对应的数据保存到session里面
    request.session['valid_str'] = sum_str

    return HttpResponse(data)

# 默认页面
@login_required()
def index(request):
    return render(request,'index.html')

# 注销
def logout(request):
    auth.logout(request)
    return redirect('login')

# 展示所有用户信息
def customers(request):
    if request.method == 'GET':
        wd = request.GET.get('wd','')
        condition = request.GET.get('condition','')

        all_customers = models.Customer.objects.filter(consultant__isnull=True)
        if wd:
            q = Q()
            q.children.append((condition,wd))
            all_customers = all_customers.filter(q)

        current_page_num = request.GET.get('page', 1)

        per_page_counts = 6
        page_number = 5

        total_count = all_customers.count()

        page_obj = page.PageNation(request.path, current_page_num, total_count,request,per_page_counts,page_number)

        all_customers = all_customers.order_by('-pk')[page_obj.start_num:page_obj.end_num]

        ret_html = page_obj.page_html()
        return render(request,'customers.html',{'all_customers':all_customers,'ret_html':ret_html})
    else:
        select_id = request.POST.getlist('selected_id')
        action = request.POST.get('action')
        print(select_id)
        if action:
            if select_id:
                if action == 'batch_delete':
                    models.Customer.objects.filter(pk__in=select_id).delete()
                elif action == 'batch_update':
                    print(666)
                    models.Customer.objects.filter(pk__in=select_id).update(source='百度推广')
                elif action == 'batch_reverse':
                    models.Customer.objects.filter(pk__in=select_id).update(consultant=request.user)
            else:
                return HttpResponse('没有选择操作对象')
        else:
            return HttpResponse('没有选择操作')
        return redirect('customers')

# 添加公户
def add(request):
    if request.method == 'GET':
        customer_obj = form.Customer()
        return render(request,'add.html',{'customer_obj':customer_obj})
    else:
        customer_obj = form.Customer(request.POST)
        if customer_obj.is_valid():
            customer_obj.save()
            return redirect('customers')
        else:
            return render(request, 'add.html', {'customer_obj': customer_obj})

# 删除数据（公有，私有）
def delete(request,pk):
    pk_list = models.Customer.objects.filter(consultant=request.user).values('pk')
    pk_status = False
    for p in pk_list:
        if p['pk'] == int(pk):
            pk_status = True
    models.Customer.objects.filter(pk=pk).delete()
    if pk_status:
        return redirect('mycustomers')
    else:
        return redirect('customers')

# 编辑数据
def edit(request,pk):
    if request.method == 'GET':
        customer_obj = models.Customer.objects.get(pk=pk)
        form_obj = form.Customer(instance=customer_obj)
        return render(request,'edit.html',{'form_obj':form_obj})
    else:
        customer_obj = models.Customer.objects.get(pk=pk)
        pk_list = models.Customer.objects.filter(consultant=request.user).values('pk')
        form_obj = form.Customer(request.POST,instance=customer_obj)
        if form_obj.is_valid():
            form_obj.save()
            for p in pk_list:
                if int(pk) == p['pk']:
                    return redirect('mycustomers')
            else:
                return redirect('customers')
        else:
            return render(request,'edit.html',{'form_obj':form_obj})

#展示私有客户信息
def mycustomers(request):
    if request.method == 'GET':

        wd = request.GET.get('wd','')
        condition = request.GET.get('condition','')

        my_customers = models.Customer.objects.filter(consultant=request.user)

        if wd:
            q = Q()
            q.children.append((condition,wd))
            my_customers = my_customers.filter(q)

        current_page_num = request.GET.get('page', 1)

        per_page_counts = 5
        page_number = 6

        total_count = my_customers.count()

        page_obj = page.PageNation(request.path, current_page_num, total_count, request, per_page_counts, page_number)

        my_customers = my_customers.order_by('pk')[page_obj.start_num:page_obj.end_num]

        ret_html = page_obj.page_html()
        return render(request, 'mycustomers.html', {'my_customers': my_customers,'ret_html':ret_html})
    else:
        select_id = request.POST.getlist('selected_id')
        action = request.POST.get('action')
        print(select_id)
        if action:
            if select_id:
                if action == 'batch_delete':
                    models.Customer.objects.filter(pk__in=select_id).delete()
                elif action == 'batch_update':
                    print(666)
                    models.Customer.objects.filter(pk__in=select_id).update(source='百度推广')
                elif action == 'batch_reverse':
                    models.Customer.objects.filter(pk__in=select_id).update(consultant=None)
            else:
                return HttpResponse('没有选择操作对象')
        else:
            return HttpResponse('没有选择操作')
        return redirect('mycustomers')

# 查看跟进记录
def followrecord(request,pk=None):
    if request.method == 'GET':

        wd = request.GET.get('wd','')
        condition = request.GET.get('condition','')
        print(condition)

        if pk:
            my_followrecord = models.ConsultRecord.objects.filter(customer__pk=pk)
        else:
            my_followrecord = models.ConsultRecord.objects.filter(consultant=request.user)

        if wd:
            q = Q()
            q.children.append((condition,wd))
            print(q)
            my_followrecord = my_followrecord.filter(q)

        current_page_num = request.GET.get('page', 1)

        per_page_counts = 6
        page_number = 5

        total_count = my_followrecord.count()
        page_obj = page.PageNation(request.path, current_page_num, total_count, request, per_page_counts, page_number)

        my_followrecord = my_followrecord.order_by('pk')[page_obj.start_num:page_obj.end_num]

        ret_html = page_obj.page_html()

        return render(request,'followrecord.html',{'my_followrecord':my_followrecord,'ret_html':ret_html})
    else:
        select_id = request.POST.getlist('selected_id')
        action = request.POST.get('action')
        print(select_id)
        if action:
            if select_id:
                if action == 'batch_delete':
                    models.ConsultRecord.objects.filter(pk__in=select_id).delete()
                elif action == 'batch_update':
                    print(666)
                    models.ConsultRecord.objects.filter(pk__in=select_id).update(status='1个月内报名')
            else:
                return HttpResponse('没有选择操作对象')
        else:
            return HttpResponse('没有选择操作')
        return redirect('followrecord')

# 添加跟进记录
def addfollow(request,pk=None):
    if request.method == 'GET':
        obj = models.ConsultRecord.objects.filter(pk=pk).first()
        follow_obj = form.ConsultRecord(request,instance=obj)
        return render(request,'addfollow.html',{'follow_obj':follow_obj})
    else:
        follow_obj = form.ConsultRecord(request,request.POST)
        if follow_obj.is_valid():
            follow_obj.save()
            return redirect('followrecord')
        else:
            return render(request,'addfollow.html',{'follow_obj':follow_obj})

# 删除跟进记录
def delfollow(request,pk):
    models.ConsultRecord.objects.filter(pk=pk).delete()
    return redirect('followrecord')

# 编辑跟进记录
def editfollow(request,pk):
    if request.method == 'GET':
        follow_obj = models.ConsultRecord.objects.get(pk=pk)
        form_obj = form.ConsultRecord(request,instance=follow_obj)
        return render(request,'editfollow.html',{'form_obj':form_obj})
    else:
        follow_obj = models.ConsultRecord.objects.get(pk=pk)
        form_obj = form.ConsultRecord(request,request.POST,instance=follow_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('followrecord')
        else:
            return render(request,'editfollow.html',{'form_obj':form_obj})

# 查看班级记录
def showclass(request):
    if request.method == 'GET':
        wd = request.GET.get('wd', '')
        condition = request.GET.get('condition', '')

        all_class = models.ClassList.objects.filter().values('pk','course','semester','campuses','teachers__username','price')

        if wd:
            q = Q()
            q.children.append((condition,wd))
            all_class = all_class.filter(q)

        current_page_num = request.GET.get('page', 1)

        per_page_counts = 6
        page_number = 5

        total_count = all_class.count()

        page_obj = page.PageNation(request.path, current_page_num, total_count, request, per_page_counts, page_number)

        all_class = all_class.order_by('-pk')[page_obj.start_num:page_obj.end_num]

        ret_html = page_obj.page_html()
        return render(request,'showclass.html',{'all_class':all_class,'ret_html':ret_html})
