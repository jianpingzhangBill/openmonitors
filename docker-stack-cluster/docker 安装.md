# docker的安装


## ubuntu系统
```bash
# 切换到root账户
sudo -i
apt update
apt install docker.io

# 加速docker服务， 这里使用七牛云  其他参考 https://www.runoob.com/docker/docker-mirror-acceleration.html
cat > /etc/docker/daemon.json <<-EOF
{"registry-mirrors":["https://reg-mirror.qiniu.com/"]}
EOF
systemctl enable docker
systemctl restart docker
```

## centos / rocky 系统
```bash
# 关闭 selinux

# 修改limits

# 如果有旧的docker 卸载
$ sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine
# 安装docker-ce
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun

# 其他安装 可以参考 https://www.runoob.com/docker/centos-docker-install.html
```

建议安装 docker-ce，自带 docker compose 命令，否则自行安装 docker-compose
RHEL ```yum install docker-compose -y```
DEBIAN ```apt install docker-compose -y```