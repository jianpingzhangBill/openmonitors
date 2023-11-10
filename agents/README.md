如果是安装在 stack模式
只要部署一次

prometheus 通过 dockerswarm_sd_configs 自动发现

其他类型的自动发现 ec2, consul, http, dns 自行参考prometheus官方文档

# cadvisor 自动发现
```
  - job_name: 'cadvisor'
    dockerswarm_sd_configs:
      - host: unix:///var/run/docker.sock
        role: tasks
    relabel_configs:
      - source_labels: [__meta_dockerswarm_service_name,__meta_dockerswarm_network_ingress,__meta_dockerswarm_task_state]
        regex: .*cadvisor;false;running
        action: keep
      - source_labels: [__address__]
        regex: (.*):.*
        replacement: $1:8080
        target_label: __address__
      - source_labels: [__meta_dockerswarm_node_hostname]
        target_label: hostname
      - source_labels: [__meta_dockerswarm_service_label_com_docker_stack_namespace]
        target_label: stack
      - source_labels: [__meta_dockerswarm_service_name]
        target_label: service
```

# node 自动发现
```
  - job_name: 'node-exporter'
    dockerswarm_sd_configs:
      - host: unix:///var/run/docker.sock
        role: tasks
    relabel_configs:
      - source_labels: [__meta_dockerswarm_service_name,__meta_dockerswarm_network_ingress,__meta_dockerswarm_task_state]
        regex: .*node-exporter;false;running
        action: keep
      - source_labels: [__address__]
        regex: (.*):.*
        replacement: $1:9100
        target_label: __address__
      - source_labels: [__meta_dockerswarm_node_hostname]
        target_label: hostname
```