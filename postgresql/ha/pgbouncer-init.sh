#!/bin/sh
# pgbouncer-init.sh
# Generate configuration files with correct permissions (UID 70 for 'postgres' in pgbouncer image)

CONFIG_DIR="/etc/pgbouncer"
mkdir -p "$CONFIG_DIR"

# Generate users.txt
echo '"postgres" "md53175bce1d3201d16594cebf9d7eb3f9d"' > "$CONFIG_DIR/users.txt"

# Generate pgbouncer.ini
cat <<EOF > "$CONFIG_DIR/pgbouncer.ini"
[databases]
* = host=postgres-primary port=5432

[pgbouncer]
listen_port = 6432
listen_addr = *
auth_type = md5
auth_file = /etc/pgbouncer/users.txt
logfile = /dev/null
; pidfile = /var/run/pgbouncer/pgbouncer.pid
admin_users = postgres
EOF

# Set ownership to postgres:root (70:0) or 999 depending on base image.
# The official pgbouncer/pgbouncer uses 'postgres' user with UID 70.
chown -R 70:0 "$CONFIG_DIR"
chmod -R 640 "$CONFIG_DIR"
chmod 750 "$CONFIG_DIR"

echo "PgBouncer configuration initialized."
