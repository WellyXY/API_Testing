@echo off
REM SSH 隧道设置脚本 (Windows 版本) - 用于连接到新的测试后端
REM 这将把远程服务器的 9580 端口映射到本地 9580 端口

echo ========================================
echo    SSH 隧道设置 - Testing Backend
echo ========================================
echo.
echo 远程服务器: 52.54.232.223
echo 端口映射: localhost:9580 -^> 52.54.232.223:9580
echo.
echo 请保持此窗口打开，关闭将断开隧道
echo 使用 Ctrl+C 停止隧道
echo.
echo ========================================

REM 检查 SSH 密钥文件
if not exist "ssh_key" (
    echo [错误] 找不到 ssh_key 文件
    echo 请确保 ssh_key 文件在当前目录
    pause
    exit /b 1
)

REM Windows 不需要修改权限，但需要确保使用 OpenSSH 客户端
where ssh >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [错误] 找不到 SSH 客户端
    echo 请安装 OpenSSH 客户端：
    echo 设置 ^> 应用 ^> 可选功能 ^> 添加功能 ^> OpenSSH 客户端
    pause
    exit /b 1
)

echo [启动] 正在建立 SSH 隧道...
echo.

REM 建立 SSH 隧道
REM -i: 指定私钥文件
REM -L: 本地端口转发 (本地端口:远程主机:远程端口)
REM -N: 不执行远程命令，仅做端口转发
ssh -i ssh_key ^
    -L 9580:localhost:9580 ^
    -N ^
    -o "ServerAliveInterval=60" ^
    -o "ServerAliveCountMax=3" ^
    -o "StrictHostKeyChecking=no" ^
    ec2-user@52.54.232.223

echo.
echo [断开] SSH 隧道已断开
pause

