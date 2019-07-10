王胜辉

自动化的系统

代码发布

nginx+uwsgi

部署 把代码通过某种方式发布到服务器上供别人访问的过程 发布

前戏

ansible  批量执行远程主机上的命令或者脚本

git 版本控制的工具

openpyxl  操作excel 表格

 celery 分布式的一个异步工具

网络的基础知识



# git

git init . 将当前目录变成git的仓库

git add .或者文件文件夹 .代表当前目录的所有文件

git commit -m “提交信息” 提交  写的多的人

git remote add origin https://url.git 将本地仓库和远程仓库做关联

git push origin master 将本地的文件推送到远程仓库

## 区域

工作区 当前工作的地方 status 看到的颜色为红色

缓存区 git add 之后的区域 status 看到的颜色为绿色

本地仓库 commit 之后的区域

远程仓库 远程的仓库，比如说码云、github

django 创建一个项目

django-admin startproject zdh

cd zdh

python manage.py startapp web

回退、回滚

git log 查看本次提交之前的提交记录

git reset --hard hash值

git reflog 查看所有的提交记录

git diff  对比本地仓库和工作区的区别

git diff --cached 对比的本地仓库和缓存区的区别

git checkout 将工作区的内容回退到最近一次提交的地方

git reset HEAD 文件 将缓存区的文件回退到工作区，不会覆盖工作区的内容



# git 快照

git stash 创建一个快照

git stash list 查看快照

git stash pop 回到拍摄快照之前并删除快照 = git stash apply + git stash drop

git stash apply 回到拍摄快照之前

git stash drop 删除快照

只适用于一个人开发的时候，快照不要拍摄太多，一次只拍摄一次

冲突

同一行做了修改 只能通过人工来决定要保留什么

# 分支

git branch 查看分支

git branch name 新建分支

git  checkout name 切换分支

git checkout -b 新建分支并且切换分支= git branch name + git checkout name

git merge name 合并分支，在合并到的分支上做合并 先checkout

git  branch -d name 删除分支

工作中一般都有多个分支

- master 线上的代码
- dev 正在开发的代码，测试用
- review 代码审核
  - 谁审核?  组长 
  - 审核什么?  逻辑？质量？pep8规范 逻辑
- 一个人一个分支

一般情况下

- 一般一个小功能 开发完成之后就做一个合并（2-3）
- 合并代码，大家都在

git 和github一样吗

git 做版本控制 linux的创始人 

github 就是一个网站 全球最大的同性交友网站

码云

gitlab 私有化部署

git  无中心化

svn 中心化

区块链 

因为没有权限

```SHELL
remote: Permission to 417685417/zdh.git denied to xiadongzhi1988.
fatal: unable to access 'https://github.com/417685417/zdh.git/': The requested URL returned error: 403
```

控制面板-凭据管理-windows凭据 把这个里面的都删掉

git push origin name   把本地分支上传到远程

git clone https://url.git 下载远程仓库的文件

git checkout -b dev origin/dev = git branch dev origin/dev + git checkout dev

以远程仓库的dev分支做母版创建一个dev分支’

git pull origin name 将远程仓库的文件拉取到本地

```SHELL
 ! [rejected]        dev1 -> dev1 (fetch first)
error: failed to push some refs to 'https://github.com/417685417/zdh.git'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. This is usually caused by another repository pushing
hint: to the same ref. You may want to first integrate the remote changes
hint: (e.g., 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

先pull 下来，然后push

# git配置信息查看

git config --global -l 查看设置的用户名和邮箱信息



# 作业

1.git命令

2 django 实现登录和注册 （不要看之前代码） modelform

随机

https://blog.51cto.com/wangfeng7399/2352670

https://blog.51cto.com/wangfeng7399/2352669

正则

https://blog.51cto.com/wangfeng7399/2339556

贡献代码
