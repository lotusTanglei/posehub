#!/bin/bash

echo "Waiting for mongodb-primary to be ready..."

# 循环检查直到能够连接
until mongosh --host mongodb-primary --port 27017 -u admin -p admin_password --authenticationDatabase admin --eval "print(\"waited for connection\")"
do
    echo "Retrying connection..."
    sleep 2
done

echo "MongoDB is ready. Initiating replica set..."

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

echo "Replica set initialized."
