# 说明

portainer工作在 stack模式下 最好指定在一个服务器上执行

有条件的话，上DNS服务，这里推荐使用 dnsmasq

## 编辑 /etc/hosts
```
xxx.xxx.xxx.xxx docker1 
xxx.xxx.xxx.xxx docker2
xxx.xxx.xxx.xxx docker3
```

## 部署到swarm
```
docker stack deploy -c portainer-stack.yaml portainer
```


## 页面打开


## 初始化管理员


## 编辑stack模版


## 部署stack


## 管理 configs 


## 管理 secrets


## 管理 networks