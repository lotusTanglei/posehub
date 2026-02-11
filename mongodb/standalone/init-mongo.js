// 初始化脚本
db = db.getSiblingDB('admin');

// 创建应用数据库用户
db.createUser({
  user: 'app_user',
  pwd: 'app_password',
  roles: [
    { role: 'readWrite', db: 'app_db' }
  ]
});

// 切换到应用数据库
db = db.getSiblingDB('app_db');

// 创建集合
db.createCollection('users');
db.createCollection('products');

// 插入示例数据
db.users.insertMany([
  { name: 'Alice', email: 'alice@example.com', created_at: new Date() },
  { name: 'Bob', email: 'bob@example.com', created_at: new Date() }
]);

print('MongoDB initialization completed!');
