#!/bin/bash

# 等待 MongoDB 启动
sleep 10

# 初始化副本集
mongosh --host mongodb-primary --port 27017 -u admin -p admin_password --authenticationDatabase admin <<EOF
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongodb-primary:27017", priority: 2 },
    { _id: 1, host: "mongodb-secondary1:27017", priority: 1 },
    { _id: 2, host: "mongodb-secondary2:27017", priority: 1 }
  ]
})
EOF

# 保持容器运行
tail -f /dev/null
