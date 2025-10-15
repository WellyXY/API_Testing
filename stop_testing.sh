#!/bin/bash

# 停止 Testing Backend SSH 隧道的脚本

echo "🛑 停止 Testing Backend SSH 隧道"
echo "================================"
echo ""

# 查找 SSH 隧道进程
ssh_pids=$(pgrep -f "ssh.*52.54.232.223.*9580")

if [ -z "$ssh_pids" ]; then
    echo "ℹ️  未找到运行中的 SSH 隧道"
    echo ""
    echo "检查端口 9580 使用情况："
    lsof -i :9580 2>/dev/null || echo "   端口 9580 未被占用"
    exit 0
fi

echo "📋 找到以下 SSH 隧道进程："
echo "$ssh_pids" | while read pid; do
    echo "   PID: $pid"
    ps -p "$pid" -o command= | head -c 80
    echo "..."
done

echo ""
read -p "❓ 是否要停止这些进程? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "⏳ 正在停止 SSH 隧道..."
    
    pkill -f "ssh.*52.54.232.223.*9580"
    
    if [ $? -eq 0 ]; then
        sleep 1
        
        # 再次检查
        if pgrep -f "ssh.*52.54.232.223.*9580" >/dev/null 2>&1; then
            echo "⚠️  部分进程可能仍在运行"
            echo "   尝试强制终止..."
            pkill -9 -f "ssh.*52.54.232.223.*9580"
        fi
        
        echo "✅ SSH 隧道已停止"
        echo ""
        echo "验证端口状态："
        lsof -i :9580 2>/dev/null || echo "   端口 9580 已释放 ✅"
    else
        echo "❌ 停止失败"
        echo ""
        echo "手动停止方法："
        echo "   sudo pkill -9 -f \"ssh.*52.54.232.223.*9580\""
    fi
else
    echo ""
    echo "❌ 操作已取消"
fi

echo ""

