#!/bin/bash

# 停止 Testing Provider SSH 隧道

PID_FILE="./testing_tunnel.pid"

echo "🛑 停止 Testing Provider SSH 隧道..."

if [ ! -f "$PID_FILE" ]; then
    echo "❌ 未找到 PID 文件，隧道可能未运行"
    
    # 尝试查找并关闭 9580 端口的 SSH 进程
    SSH_PID=$(lsof -ti:9580 2>/dev/null | head -1)
    if [ ! -z "$SSH_PID" ]; then
        echo "⚠️  发现端口 9580 的进程 (PID: $SSH_PID)"
        read -p "是否关闭此进程? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            kill $SSH_PID
            echo "✅ 进程已关闭"
        fi
    fi
    exit 0
fi

PID=$(cat "$PID_FILE")

if ps -p $PID > /dev/null 2>&1; then
    echo "⏹️  关闭 SSH 隧道 (PID: $PID)..."
    kill $PID
    sleep 1
    
    # 如果进程还在运行，强制关闭
    if ps -p $PID > /dev/null 2>&1; then
        echo "🔨 强制关闭..."
        kill -9 $PID
    fi
    
    echo "✅ SSH 隧道已关闭"
else
    echo "⚠️  进程 (PID: $PID) 未运行"
fi

rm -f "$PID_FILE"
echo "🧹 已清理 PID 文件"

