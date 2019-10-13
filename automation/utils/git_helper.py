from git import Repo
import os
from git import Git
import subprocess
class GitRepo():

    def __init__(self,path):
        self.path=path

    def is_dir(self,url):
        path=os.path.join(self.path,".git")
        if not os.path.exists(path):
            Repo.clone_from(url,self.path)

    def get_branch(self):
        return [str(b).split("/")[1] for b in Repo(self.path).remote().refs if str(b) !="origin/HEAD"]


    def get_commit(self,bra):
        # 将本地的分支强制与origin/分支一致，回退到拉取下来的位置
        try:
            active = Repo(self.path).active_branch
        except Exception as e:
            active = "master"
        subprocess.getoutput("cd {} && git reset --hard origin/{}".format(self.path, active))
        Git(self.path).checkout(bra)# 因为本地没有这个分支，所以才会报错，先切换这个分支，还能下载
        return [{"id":commit.hexsha,"msg":commit.message} for commit in Repo(self.path).iter_commits(bra)]

    def get_tag(self):
        return [str(t) for t in Repo(self.path).tags]


    def checkout(self,bra,commit=None,type=None):
        try:
            active=Repo(self.path).active_branch
        except Exception as e:
            active="master"
        subprocess.getoutput("cd {} && git reset --hard origin/{}".format(self.path,active))
        Git(self.path).checkout(bra)
        if type !=None:
            Repo(self.path).index.reset(commit=commit,head=True)

### 实现
# 发布
# 灰度发布
# 先发布一台
# 测试
#发布剩余的
# 回滚 cp