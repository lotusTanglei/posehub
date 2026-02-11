# PoseHub - Docker Compose 中间件合集

收集整理常用的 Docker Compose 配置文件，方便快速部署各类中间件和服务。

## 目录结构

```
posehub/
├── mysql/                    # MySQL 数据库
│   ├── standalone/          # 单实例部署
│   └── cluster/             # 主从复制集群
├── redis/                    # Redis 缓存
│   ├── standalone/          # 单实例部署
│   ├── sentinel/            # Sentinel 哨兵模式
│   └── cluster/             # Cluster 集群模式
├── nginx/                    # Nginx Web 服务器
│   ├── standalone/          # 单实例部署
│   └── ha/                  # 高可用部署（HAProxy 负载均衡）
├── postgresql/              # PostgreSQL 数据库
│   ├── standalone/          # 单实例部署
│   └── ha/                  # 主从复制高可用
├── mongodb/                 # MongoDB 文档数据库
│   ├── standalone/          # 单实例部署
│   ├── replica-set/         # 副本集
│   └── sharded-cluster/     # 分片集群
├── rabbitmq/               # RabbitMQ 消息队列
│   ├── standalone/          # 单实例部署
│   └── cluster/             # 集群部署
├── kafka/                   # Kafka 消息队列
│   ├── standalone/          # 单实例部署
│   └── cluster/             # 集群部署
├── elasticsearch/           # Elasticsearch 搜索引擎
│   ├── standalone/          # 单节点部署
│   └── cluster/             # 集群部署
├── prometheus/              # Prometheus 监控
│   ├── standalone/          # 单实例部署
│   └── ha/                  # 高可用部署
└── grafana/                 # Grafana 可视化
    ├── standalone/          # 单实例部署
    └── ha/                  # 高可用部署
```

## 快速开始

### MySQL 单实例部署

```bash
cd mysql/standalone
docker-compose up -d
```

### Redis Sentinel 高可用部署

```bash
cd redis/sentinel
docker-compose up -d
```

### Nginx 高可用部署

```bash
cd nginx/ha
docker-compose up -d
```

### Kafka 集群部署

```bash
cd kafka/cluster
docker-compose up -d
```

## 部署说明

### 使用前必读

1. **修改默认密码**：所有配置文件中的密码都是示例密码，生产环境请务必修改
2. **端口冲突**：确保所需端口未被占用
3. **数据持久化**：数据会存储在 Docker Volume 中，删除容器不会丢失数据
4. **资源限制**：生产环境建议配置资源限制（CPU、内存）

### 通用操作

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 查看服务状态
docker-compose ps
```

## 中间件详情

### MySQL

- **版本**: 8.0
- **端口**: 3306
- **默认密码**: root_password
- **配置文件**: `conf.d/my.cnf`

### Redis

- **版本**: 7-alpine
- **端口**: 6379
- **持久化**: RDB + AOF
- **配置文件**: `redis.conf`

### Nginx

- **版本**: Alpine
- **端口**: 80, 443
- **配置目录**: `conf/`, `conf.d/`
- **静态文件**: `html/`

### PostgreSQL

- **版本**: 16-alpine
- **端口**: 5432
- **默认密码**: postgres_password
- **健康检查**: 已启用

### MongoDB

- **版本**: 7
- **端口**: 27017
- **认证**: 已启用
- **初始化脚本**: `init-mongo.js`

### RabbitMQ

- **版本**: 3.13-management-alpine
- **端口**: 5672 (AMQP), 15672 (管理界面)
- **默认账号**: admin / admin_password
- **管理界面**: http://localhost:15672

### Kafka

- **版本**: 3.6 (Bitnami)
- **端口**: 9092
- **Kafka UI**: http://localhost:8080
- **依赖**: ZooKeeper

### Elasticsearch

- **版本**: 8.11.0
- **端口**: 9200 (HTTP), 9300 (Transport)
- **默认密码**: elastic_password
- **Kibana**: http://localhost:5601

### Prometheus

- **版本**: Latest
- **端口**: 9090
- **配置文件**: `prometheus.yml`
- **告警规则**: `alerts/`

### Grafana

- **版本**: Latest
- **端口**: 3000
- **默认账号**: admin / admin_password
- **数据源配置**: 自动配置 Prometheus

## 贡献指南

欢迎提交 PR 添加更多中间件的 Docker Compose 配置！

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- 仓库地址: https://gitee.com/lotus-ian-tanglei/posehub.git

## 注意事项

- 本仓库提供的配置文件仅供学习和开发环境使用
- 生产环境使用请根据实际需求调整配置
- 请务必修改默认密码和密钥
- 建议配置适当的资源限制和监控告警
