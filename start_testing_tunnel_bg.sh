#!/bin/bash

# Testing Provider SSH Tunnel Script (后台运行)
# 将远程服务器的 9580 端口映射到本地 9580 端口

REMOTE_HOST="52.54.232.223"
REMOTE_USER="ec2-user"
REMOTE_PORT="9580"
LOCAL_PORT="9580"
SSH_KEY="./ssh_key"
PID_FILE="./testing_tunnel.pid"

echo "🔧 启动 Testing Provider SSH 隧道 (后台模式)..."
echo "   远程: ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PORT}"
echo "   本地: localhost:${LOCAL_PORT}"
echo ""

# 检查 SSH 密钥
if [ ! -f "$SSH_KEY" ]; then
    echo "❌ 错误: SSH 密钥文件不存在: $SSH_KEY"
    exit 1
fi

chmod 600 "$SSH_KEY"

# 检查是否已有隧道在运行
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p $OLD_PID > /dev/null 2>&1; then
        echo "⚠️  SSH 隧道已在运行 (PID: $OLD_PID)"
        echo "   使用 ./stop_testing_tunnel.sh 停止现有隧道"
        exit 1
    else
        echo "🧹 清理过期的 PID 文件..."
        rm -f "$PID_FILE"
    fi
fi

# 检查端口是否已被占用
if lsof -Pi :${LOCAL_PORT} -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  端口 ${LOCAL_PORT} 已被其他进程占用"
    lsof -i :${LOCAL_PORT} | grep LISTEN
    exit 1
fi

echo "🚀 在后台建立 SSH 隧道..."

# 建立 SSH 隧道 (后台运行)
ssh -f -N \
    -L ${LOCAL_PORT}:localhost:${REMOTE_PORT} \
    -i "$SSH_KEY" \
    -o StrictHostKeyChecking=no \
    -o ServerAliveInterval=60 \
    -o ServerAliveCountMax=3 \
    ${REMOTE_USER}@${REMOTE_HOST}

# 等待隧道建立
sleep 2

# 验证隧道是否成功
if lsof -Pi :${LOCAL_PORT} -sTCP:LISTEN -t >/dev/null 2>&1; then
    SSH_PID=$(lsof -ti:${LOCAL_PORT} | head -1)
    echo $SSH_PID > "$PID_FILE"
    echo "✅ SSH 隧道已建立 (PID: $SSH_PID)"
    echo "   使用 ./stop_testing_tunnel.sh 停止隧道"
else
    echo "❌ SSH 隧道建立失败"
    exit 1
fi

