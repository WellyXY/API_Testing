# Testing Provider 设置指南

## 问题

当前 `ssh_key` 文件为空，无法建立 SSH 隧道连接到测试服务器。

## 解决方案

### 1. 放置 SSH 私钥

将 EC2 的 SSH 私钥文件内容复制到 `ssh_key` 文件中：

```bash
# 方法 1: 如果你有 aws-general.pem 或其他密钥文件
cp /path/to/your/key.pem ./ssh_key

# 方法 2: 直接编辑 ssh_key 文件
nano ssh_key
# 或
vim ssh_key
```

SSH 私钥应该以以下格式开头：
```
-----BEGIN RSA PRIVATE KEY-----
或
-----BEGIN OPENSSH PRIVATE KEY-----
```

### 2. 设置正确的权限

```bash
chmod 600 ssh_key
```

### 3. 启动 SSH 隧道

```bash
# 后台运行（推荐）
./start_testing_tunnel_bg.sh

# 或前台运行（可以看到日志）
./start_testing_tunnel.sh
```

### 4. 停止 SSH 隧道

```bash
./stop_testing_tunnel.sh
```

### 5. 验证连接

隧道启动后，应该可以通过以下方式访问：

```bash
# 检查端口是否监听
lsof -i :9580

# 测试 API（如果服务器已启动）
curl -X GET "http://localhost:9580/api/v1/generate/v0/videos/test" \
     -H "X-API-Key: test-api-key-123456"
```

## 使用流程

1. **启动隧道**: `./start_testing_tunnel_bg.sh`
2. **打开前端**: 在浏览器中打开 `parrot_api_frontend.html`
3. **选择 Provider**: 在下拉菜单中选择 "Testing (New Architecture)"
4. **开始测试**: 上传图片并生成视频
5. **完成后**: `./stop_testing_tunnel.sh`

## 故障排除

### SSH 连接失败

```bash
# 测试 SSH 连接
ssh -i ./ssh_key ec2-user@52.54.232.223

# 如果提示 "invalid format"，检查密钥格式
cat ssh_key | head -5
```

### 端口已被占用

```bash
# 查看占用端口的进程
lsof -i :9580

# 强制关闭
./stop_testing_tunnel.sh
```

### 权限问题

```bash
# 重置 SSH 密钥权限
chmod 600 ssh_key
```

