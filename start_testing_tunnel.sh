#!/bin/bash

# Testing Provider SSH Tunnel Script
# 将远程服务器的 9580 端口映射到本地 9580 端口

REMOTE_HOST="52.54.232.223"
REMOTE_USER="ec2-user"
REMOTE_PORT="9580"
LOCAL_PORT="9580"
SSH_KEY="./ssh_key"

echo "🔧 启动 Testing Provider SSH 隧道..."
echo "   远程: ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PORT}"
echo "   本地: localhost:${LOCAL_PORT}"
echo ""

# 检查 SSH 密钥权限
if [ ! -f "$SSH_KEY" ]; then
    echo "❌ 错误: SSH 密钥文件不存在: $SSH_KEY"
    exit 1
fi

chmod 600 "$SSH_KEY"

# 检查端口是否已被占用
if lsof -Pi :${LOCAL_PORT} -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  端口 ${LOCAL_PORT} 已被占用"
    echo "   现有连接:"
    lsof -i :${LOCAL_PORT} | grep LISTEN
    echo ""
    read -p "是否关闭现有连接? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🔄 关闭现有连接..."
        lsof -ti:${LOCAL_PORT} | xargs kill -9 2>/dev/null
        sleep 1
    else
        echo "❌ 取消操作"
        exit 1
    fi
fi

echo "🚀 建立 SSH 隧道..."
echo "   按 Ctrl+C 停止隧道"
echo ""

# 建立 SSH 隧道 (前台运行，便于调试)
# -N: 不执行远程命令
# -L: 本地端口转发
# -o ServerAliveInterval=60: 每60秒发送心跳
# -o ServerAliveCountMax=3: 3次心跳失败后断开
ssh -N \
    -L ${LOCAL_PORT}:localhost:${REMOTE_PORT} \
    -i "$SSH_KEY" \
    -o StrictHostKeyChecking=no \
    -o ServerAliveInterval=60 \
    -o ServerAliveCountMax=3 \
    ${REMOTE_USER}@${REMOTE_HOST}

echo ""
echo "⏹️  SSH 隧道已关闭"

