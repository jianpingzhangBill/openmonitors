启用 docker swarm集群
```
docker swarm init
```

创建加入master/worker节点token
```
docker swarm join-token manager 
docker swarm join-token worker
```

查看集群的node状态， * 是当前的主节点
```
docker node ls 

ID                            HOSTNAME   STATUS    AVAILABILITY   MANAGER STATUS   ENGINE VERSION
lduizi096fnhbtmfrih6frqow *   docker1    Ready     Active         Reachable        24.0.2
uo6ftb4pux62dnrw3pjggzksn     docker2    Ready     Active         Leader           24.0.2
7w0gkcyrws6eaugtx05g478t2     docker3    Ready     Active         Reachable        24.0.2
```

在其他节点执行
```
 docker swarm join --token xxxx xxxx # 由 init 或者 init-token创建
```

