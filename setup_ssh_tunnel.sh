#!/bin/bash

# SSH 隧道设置脚本 - 用于连接到新的测试后端
# 这将把远程服务器的 9580 端口映射到本地 9580 端口

echo "🚀 正在建立 SSH 隧道到测试后端..."
echo "📍 远程服务器: 52.54.232.223"
echo "🔌 端口映射: localhost:9580 -> 52.54.232.223:9580"
echo ""
echo "⚠️  请保持此窗口打开，关闭将断开隧道"
echo "⚠️  使用 Ctrl+C 停止隧道"
echo ""

# 检查 SSH 密钥文件
if [ ! -f "ssh_key" ]; then
    echo "❌ 错误: 找不到 ssh_key 文件"
    echo "请确保 ssh_key 文件在当前目录"
    exit 1
fi

# 设置正确的密钥文件权限（SSH 要求私钥权限为 600）
chmod 600 ssh_key

# 建立 SSH 隧道
# -i: 指定私钥文件
# -L: 本地端口转发 (本地端口:远程主机:远程端口)
# -N: 不执行远程命令，仅做端口转发
# -v: 显示详细信息（调试用）
ssh -i ssh_key \
    -L 9580:localhost:9580 \
    -N \
    -o "ServerAliveInterval=60" \
    -o "ServerAliveCountMax=3" \
    -o "StrictHostKeyChecking=no" \
    ec2-user@52.54.232.223

# 如果 SSH 连接断开，显示消息
echo ""
echo "🔴 SSH 隧道已断开"

