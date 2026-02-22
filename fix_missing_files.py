import os

# Define the root path relative to where script runs (project root)
ROOT = "."

# Helper to create directories
def ensure_dir(path):
    full_path = os.path.join(ROOT, path)
    if not os.path.exists(full_path):
        print(f"Creating directory: {full_path}")
        os.makedirs(full_path)

# Helper to create files with content
def ensure_file(path, content):
    full_path = os.path.join(ROOT, path)
    # Only create if not exists to avoid overwriting user changes (though audit said they are missing)
    if not os.path.exists(full_path):
        print(f"Creating file: {full_path}")
        # Ensure parent dir exists
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)

# 1. PostgreSQL Standalone
ensure_dir("postgresql/standalone/init")

# 2. PostgreSQL HA (Pgbouncer + Postgres)
ensure_file("postgresql/ha/postgresql.conf", """
listen_addresses = '*'
max_connections = 100
shared_buffers = 128MB
dynamic_shared_memory_type = posix
log_timezone = 'UTC'
datestyle = 'iso, mdy'
timezone = 'UTC'
lc_messages = 'en_US.utf8'
lc_monetary = 'en_US.utf8'
lc_numeric = 'en_US.utf8'
lc_time = 'en_US.utf8'
default_text_search_config = 'pg_catalog.english'
""")

ensure_file("postgresql/ha/pg_hba.conf", """
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             all                                     trust
host    all             all             127.0.0.1/32            trust
host    all             all             ::1/128                 trust
host    all             all             0.0.0.0/0               md5
""")

ensure_file("postgresql/ha/pgbouncer.ini", """
[databases]
* = host=postgres port=5432

[pgbouncer]
listen_port = 6432
listen_addr = *
auth_type = md5
auth_file = /etc/pgbouncer/users.txt
logfile = /var/log/pgbouncer/pgbouncer.log
pidfile = /var/run/pgbouncer/pgbouncer.pid
admin_users = postgres
""")

ensure_file("postgresql/ha/users.txt", '"postgres" "md53175bce1d3201d16594cebf9d7eb3f9d"')

# 3. Redis Sentinel
ensure_file("redis/sentinel/redis.conf", """
bind 0.0.0.0
protected-mode no
port 6379
""")

ensure_file("redis/sentinel/redis-slave.conf", """
bind 0.0.0.0
protected-mode no
port 6379
replicaof redis-master 6379
""")

ensure_file("redis/sentinel/sentinel.conf", """
port 26379
dir /tmp
sentinel monitor mymaster redis-master 6379 2
sentinel down-after-milliseconds mymaster 30000
sentinel parallel-syncs mymaster 1
sentinel failover-timeout mymaster 180000
sentinel deny-scripts-reconfig yes
""")

# 4. Grafana
ensure_dir("grafana/standalone/dashboards")

# 5. RabbitMQ Cluster (HAProxy)
ensure_file("rabbitmq/cluster/haproxy.cfg", """
global
    log 127.0.0.1 local0
    maxconn 4096

defaults
    log     global
    mode    tcp
    option  tcplog
    retries 3
    timeout connect 5000
    timeout client  50000
    timeout server  50000

listen rabbitmq
    bind *:5672
    mode tcp
    balance roundrobin
    server rabbitmq1 rabbitmq1:5672 check inter 5000 rise 2 fall 3
    server rabbitmq2 rabbitmq2:5672 check inter 5000 rise 2 fall 3
    server rabbitmq3 rabbitmq3:5672 check inter 5000 rise 2 fall 3

listen stats
    bind *:15672
    mode http
    stats enable
    stats uri /
    stats realm Haproxy\ Statistics
    stats auth admin:admin
""")

# 6. Nginx Standalone
ensure_dir("nginx/standalone/html")
ensure_file("nginx/standalone/html/index.html", "<h1>Hello from Nginx Standalone!</h1>")
ensure_dir("nginx/standalone/ssl")
ensure_dir("nginx/standalone/logs")

# 7. Nginx HA
ensure_dir("nginx/ha/html")
ensure_file("nginx/ha/html/index.html", "<h1>Hello from Nginx HA!</h1>")
ensure_dir("nginx/ha/ssl")
ensure_dir("nginx/ha/logs1")
ensure_dir("nginx/ha/logs2")
ensure_dir("nginx/ha/conf.d")
ensure_file("nginx/ha/nginx.conf", """
user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log notice;
pid        /var/run/nginx.pid;

events {
    worker_connections  1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    keepalive_timeout  65;

    include /etc/nginx/conf.d/*.conf;
    
    server {
        listen 80;
        server_name localhost;
        location / {
            root /usr/share/nginx/html;
            index index.html index.htm;
        }
    }
}
""")

# 8. Prometheus
ensure_dir("prometheus/standalone/grafana/provisioning")

# 9. Elasticsearch Standalone
ensure_file("elasticsearch/standalone/elasticsearch.yml", """
cluster.name: "docker-cluster"
network.host: 0.0.0.0
discovery.type: single-node
""")

print("Fixes applied successfully!")
