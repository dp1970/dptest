import time
import os
from django.shortcuts import render, redirect
from web import models, form
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from utils.ansible2.inventory import Inventory
from utils.ansible2.runner import AdHocRunner
from utils.ansible2.runner import PlayBookRunner, CommandRunner
from django.db.models import Q
from django.template.response import TemplateResponse
from utils.git_helper import GitRepo


# Create your views here.

# 登陆页面
# @login_required()
def login(request):
    response_msg = {'code': None, 'msg': None}
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        print(username)
        user_obj = models.UserProfile.objects.filter(name=username, password=pwd).first()
        if user_obj:
            request.session["user_id"] = user_obj.pk
            response_msg['code'] = 100
            response_msg['msg'] = '登陆成功'
        else:
            response_msg['code'] = 400
            response_msg['msg'] = '账户名密码错误!'

    return JsonResponse(response_msg)


# 注销
def logout(request):
    request.session.flush()
    return redirect('login')


# 查看默认页面
def index(request):
    return render(request, 'master/base.html')


# 查看用户数据
def user(request):
    search = request.GET.get("table_search", "")
    user_obj = models.UserProfile.objects.filter(
        Q(name__contains=search) | Q(email__contains=search) | Q(role__contains=search)).exclude(id=2)
    return TemplateResponse(request, 'user.html', {'all_user': user_obj, 'page_title': '用户列表'})


# 添加用户
def useradd(request):
    if request.method == 'GET':
        user_obj = form.User()
        return render(request, 'useradd.html', {'user_obj': user_obj})
    else:
        User_obj = form.User(request.POST)
        if User_obj.is_valid():
            User_obj.save()
            return JsonResponse({'status': 0, 'msg': '添加成功'})
        else:
            return JsonResponse({'status': 1, 'msg': '添加失败,原因是{}'.format(User_obj.errors)})


# 编辑用户
def edit(request, pk):
    if request.method == 'GET':
        user_obj = models.UserProfile.objects.get(pk=pk)
        form_obj = form.User(instance=user_obj)
        return render(request, 'edit.html', {'form_obj': form_obj, 'pk': pk})
    else:
        user_obj = models.UserProfile.objects.get(pk=pk)
        form_obj = form.User(request.POST, instance=user_obj)
        print(form_obj)
        if form_obj.is_valid():
            form_obj.save()
            return JsonResponse({'status': 0, 'msg': '修改成功'})
        else:
            return JsonResponse({'status': 1, 'msg': '修改失败,原因是{}'.format(form_obj.errors)})


# 删除用户
def userdel(request, pk):
    user_obj = models.UserProfile.objects.filter(pk=pk).delete()
    return JsonResponse({'status': 0, 'msg': '删除成功'})


# 查看主机
def host(request):
    search = request.GET.get("table_search", "")
    host_obj = models.Host.objects.filter(
        Q(name__contains=search) | Q(hostip__contains=search) | Q(env__contains=search))
    return TemplateResponse(request, 'host.html', {'host_obj': host_obj, 'page_title': '主机管理'})


# 添加主机
def hostadd(request):
    if request.method == 'GET':
        host_obj = form.Host()
        return render(request, 'hostadd.html', {'host_obj': host_obj})
    else:
        host_obj = form.Host(request.POST)
        if host_obj.is_valid():
            status = hostping(host_obj.cleaned_data['hostip'], host_obj.cleaned_data['ssh_port'],
                              host_obj.cleaned_data['user'])
            if status:
                host_obj.save()
                return JsonResponse({'status': 0, 'msg': '添加成功'})
            else:
                return JsonResponse({'status': 1, 'msg': '主机不在线'})
        else:
            return JsonResponse({'status': 1, 'msg': '添加失败,原因是{}'.format(host_obj.errors)})


# 编辑主机
def hostedit(request, pk):
    if request.method == 'GET':
        host_obj = models.Host.objects.get(pk=pk)
        form_obj = form.Host(instance=host_obj)
        return render(request, 'hostedit.html', {'form_obj': form_obj, 'pk': pk})
    else:
        host_obj = models.Host.objects.get(pk=pk)
        form_obj = form.Host(request.POST, instance=host_obj)
        if form_obj.is_valid():
            status = hostping(form_obj.cleaned_data['hostip'], form_obj.cleaned_data['ssh_port'],
                              form_obj.cleaned_data['user'])
            if status:
                form_obj.save()
                return JsonResponse({'status': 0, 'msg': '编辑成功'})
            else:
                return JsonResponse({'status': 1, 'msg': '主机不在线'})
        else:
            return JsonResponse({'status': 1, 'msg': '编辑失败,失败原因是{}'.format(form_obj.errors)})


# 删除主机
def hostdel(request, pk):
    host_obj = models.Host.objects.filter(pk=pk).delete()
    return JsonResponse({'status': 0, 'msg': '删除成功'})


# 查看host状态
def hostping(hostip, port, username):
    host_data = [
        {
            "hostname": hostip,
            "ip": hostip,
            "port": port,
            "username": username
        },
    ]  # 主机列表
    inventory = Inventory(host_data)  # 动态生成主机配置信息
    runner = AdHocRunner(inventory)
    tasks = [{"action": {'module': 'ping'}, "name": "ping"}]
    ret = runner.run(tasks)
    if ret.results_raw['ok']:
        return True
    else:
        return False


# 查看初始化状态
def init(request):
    search = request.GET.get("table_search", "")
    init_obj = models.Init.objects.filter(name__contains=search)
    return TemplateResponse(request, 'init.html', {'init_obj': init_obj, 'page_title': '初始化'})


# 添加初始化
def initadd(request):
    if request.method == 'GET':
        init_obj = form.Init()
        return render(request, 'initadd.html', {'init_obj': init_obj})
    else:
        init_obj = form.Init(request.POST)
        if init_obj.is_valid():
            init_obj.instance.create_user = request.account
            init_obj.save()
            return JsonResponse({'status': 0, 'msg': '添加成功'})
        else:
            return JsonResponse({'status': 1, 'mas': '添加失败,原因是{}'.format(init_obj.errors)})


# 编辑初始化
def initedit(request, pk):
    if request.method == 'GET':
        init_obj = models.Init.objects.get(pk=pk)
        form_obj = form.Init(instance=init_obj)
        return render(request, 'initedit.html', {'form_obj': form_obj, 'pk': pk})
    else:
        init_obj = models.Init.objects.get(pk=pk)
        form_obj = form.Init(request.POST, instance=init_obj)
        if form_obj.is_valid():
            form_obj.instance.create_user = request.account
            form_obj.save()
            return JsonResponse({'status': 0, 'msg': '编辑成功'})
        else:
            return JsonResponse({'status': 1, 'msg': '编辑失败,原因是{}'.format(init_obj)})


# 删除初始化
def initdel(request, pk):
    models.Init.objects.filter(pk=pk).delete()
    return JsonResponse({'status': 0, 'msg': '删除成功'})


# 初始化主机
def inithost(request):
    if request.method == 'GET':
        host_obj = form.Initlog()
        return render(request, 'inithost.html', {'host_obj': host_obj})
    else:
        host_obj = form.Initlog(request.POST)
        if host_obj.is_valid():
            host_obj.instance.user = request.account
            res = ansible(host_obj.cleaned_data['hosts_list'], host_obj.cleaned_data['init'].play_book)
            host_obj.instance.result = res['stats']
            host_obj.save()
            return JsonResponse({'status': 0, "msg": '执行成功'})
        else:
            return JsonResponse({'status': 1, 'msg': '执行失败{}'.format(host_obj)})


# ansible执行情况
def ansible(hostip, playbook):
    host_data = [{'hostname': host.hostip, "ip": host.hostip, 'port': host.ssh_port, 'username': host.user} for host in
                 hostip]
    inventory = Inventory(host_data)
    runner = PlayBookRunner(inventory)
    ret = runner.run(playbook)
    return ret


# 查看初始化详情
def initlog(request, name):
    form_obj = models.InitLog.objects.filter(init__name=name)
    return render(request, 'initlog.html', {'form_obj': form_obj})


# 查看项目
def project(request):
    search = request.GET.get("table_search", "")
    project_obj = models.Project.objects.filter(Q(name__contains=search) | Q(boss__name__contains=search))
    return TemplateResponse(request, 'project.html', {'project_obj': project_obj, 'page_title': '项目管理'})


# 查看项目详情
def projectinfo(request, name):
    form_obj = models.Project.objects.filter(name=name)
    return render(request, 'projectinfo.html', {'form_obj': form_obj})


# 添加项目
def projectadd(request):
    if request.method == 'GET':
        project_obj = form.Project()
        return render(request, 'projectadd.html', {'project_obj': project_obj})
    else:
        project_obj = form.Project(request.POST)
        if project_obj.is_valid():
            project_obj.instance.create_user = request.account
            project_obj.save()
            return JsonResponse({'status': 0, 'msg': '添加成功'})
        else:
            return JsonResponse({'status': 1, 'msg': '添加失败,原因是{}'.format(project_obj)})


# 编辑项目
def projectedit(request, pk):
    project_obj = models.Project.objects.get(pk=pk)
    if request.method == 'GET':
        form_obj = form.Project(instance=project_obj)
        return render(request, 'projectedit.html', {'form_obj': form_obj, 'pk': pk})
    else:
        form_obj = form.Project(request.POST, instance=project_obj)
        if form_obj.is_valid():
            form_obj.instance.create_user = request.account
            form_obj.save()
            return JsonResponse({'status': 0, 'msg': '编辑成功'})
        else:
            return JsonResponse({'status': 1, 'msg': '编辑失败,原因是{}'.format(project_obj)})


# 删除项目
def projectdel(request, pk):
    models.Project.objects.filter(pk=pk).delete()
    return JsonResponse({'status': 0, 'msg': '删除成功'})


# 添加命令下发任务
def codeissuance(request):
    form_obj = models.Host.objects.all()
    ips = [{'id': 1, 'pId': 0, 'name': "选择主机", 'open': 'true'}]
    for v in form_obj:
        ips.append({'id': 3, 'pId': 1, 'name': v.hostip})
    if request.method == 'POST':
        nodeips = request.POST.getlist('node_ips[]')
        host_list = models.Host.objects.filter(hostip__in=nodeips)
        res = command(host_list, request.POST.get('command'))
        models.Command.objects.create(hosts_list=nodeips, command=request.POST.get('command'), user=request.account,
                                      result=res)
        return JsonResponse({'status': 0, 'msg': res})
    return render(request, 'codeissuance.html', {'page_title': '命令下发', 'ips': ips})


# 命令下发执行ansible
def command(hostlist, command):
    host_data = [{"hostname": h.hostip, "ip": h.hostip, "port": h.ssh_port} for h in hostlist]
    inventory = Inventory(host_data)  # 重新组成虚拟组
    runner = CommandRunner(inventory)
    res = runner.execute(command)
    return res.results_raw


# 查看命令下发记录
def showissuance(request):
    search = request.GET.get("table_search", "")
    issuance_obj = models.Command.objects.filter(command__contains=search)
    return render(request, 'showissuance.html', {'issuance_obj': issuance_obj, 'page_title': '命令下发'})


# 查看计划任务记录
def showcron(request):
    search = request.GET.get('table_search', '')
    cron_obj = models.Cron.objects.filter(name__contains=search)
    return render(request, 'showcron.html', {'cron_obj': cron_obj, 'page_title': '定时任务'})


# 添加计划任务
def cronadd(request):
    cron_obj = form.Cron()
    if request.method == 'POST':
        form_obj = form.Cron(request.POST)
        if form_obj.is_valid():
            time = [form_obj.cleaned_data['minute'], form_obj.cleaned_data['hour'], form_obj.cleaned_data['day'],
                    form_obj.cleaned_data['month'], form_obj.cleaned_data['weekday']]
            form_obj.instance.time = time
            res = cron_ansible(form_obj.cleaned_data['hosts_list'], time, job=form_obj.cleaned_data['job'],
                               name=form_obj.cleaned_data['name'], user=form_obj.cleaned_data['user'])
            if res:
                form_obj.instance.create_user = request.account
                form_obj.save()
                return JsonResponse({'status': 0, 'msg': '添加成功'})
            else:
                return JsonResponse({'status': 1, 'msg': '添加失败'})
        else:
            return JsonResponse({'status': 1, 'msg': f'操作失败，失败的原因是{cron_obj.errors}'})
    return render(request, 'cron.html', {'cron_obj': cron_obj, 'page_title': '定时任务'})


# 编辑计划任务
def cronedit(request, pk):
    cron_obj = models.Cron.objects.filter(pk=pk)
    if request.method == 'GET':
        form_obj = form.Cron(instance=cron_obj)
        # TODO 编辑出现问题
        return render(request, 'cronedit.html', {'form_obj': form_obj, 'page_title': '编辑任务', 'pk': pk})


# 添加cron的ansible任务
def cron_ansible(host_list, time=None, job=None, name=None, user=None, type=None):
    host_data = [{'hostname': host.hostip, 'ip': host.hostip, 'port': host.ssh_port} for host in host_list]
    inventory = Inventory(host_data)  # 动态生成主机配置信息
    runner = AdHocRunner(inventory)
    if type == 1:
        tasks = [{"action": {"module": "cron", "args": "name={} user={} state=absent".format(name, user)}}]
    else:
        tasks = [{"action": {"module": "cron",
                             "args": f"minute={time[0]} hour={time[1]} day={time[2]} month={time[3]} weekday={time[4]} name = {name} job = {job} user = {user}"}, "name": "cron"}]
        ret = runner.run(tasks)
        print(tasks)
        print(ret.results_raw)
        if ret.results_raw["ok"]:
            print('pk')
    return True

# else:
# print('false')
# return False


# 查看发布列表
def showpublish(request):
    search = request.GET.get('table_search', '')
    publish_obj = models.Issue.objects.filter(project__name__contains=search)
    return TemplateResponse(request, 'showpublish.html', {'publish_obj': publish_obj, 'page_title': '发布列表'})


# 上传文件
def createfile(request):
    form_obj = form.FileForm()
    if request.method == 'POST':
        form_obj = form.FileForm(request.POST, request.FILES)
        t = int(time.time())
        if form_obj.is_valid():
            status = handle_uploaded_file(request.FILES.getlist('file_field'), t)
            if not status:
                return JsonResponse({"status": 1, "msg": "请上传readme.xlsx文件"})
            form_obj.instance.user = request.account
            form_obj.instance.upload_path = t
            form_obj.instance.type = "0"
            form_obj.save()
            return JsonResponse({"status": 0, "msg": "操作成功"})
        else:
            return JsonResponse({"status": 1, "msg": "操作失败,失败原因为{}".format(form_obj.errors)})
    return render(request, 'createfile.html', {'form_obj': form_obj})


# 上传文件的函数
def handle_uploaded_file(files, t):
    path = "/updata/file/{}".format(t)
    filename = [f.name for f in files]
    print(filename)
    if "readme.xlsx" not in filename:
        return False
    if not os.path.exists(path):
        os.makedirs(path)
    for f in files:
        with open('{}/{}'.format(path, f.name), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    return True


# git更新
def creategit(request):
    form_obj = form.GitForm()
    if request.method == 'POST':
        form_obj = form.GitForm(request.POST)
        t = int(time.time())
        if form_obj.is_valid():
            form_obj.instance.user = request.account
            form_obj.instance.upload_path = t
            form_obj.instance.type = "1"
            path = "/updata/git/{}".format(form_obj.cleaned_data["project"].name)
            if request.POST.get("type") == "bra":
                GitRepo(path).checkout(request.POST.get("bra_name"), request.POST.get("com_name"))
            else:
                GitRepo(path).checkout(request.POST.get("tag_name"), type="tag")
            form_obj.save()
            return JsonResponse({"status": 0, "msg": "操作成功"})
        else:
            return JsonResponse({"status": 1, "msg": "操作失败,失败原因为{}".format(form_obj.errors)})
    return render(request, 'creategit.html', {'form_obj': form_obj})


def git_branch(request, pk):
    path = "/update/git/{}".format()
