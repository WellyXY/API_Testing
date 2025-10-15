# 新测试后端 (Testing Backend) 使用说明

## 📋 概述

新的测试后端采用了新的架构设计，运行在远程 EC2 服务器上。由于前端无法直接访问远程服务器，我们需要通过 SSH 隧道来建立连接。

## 🔧 架构信息

- **远程服务器**: `52.54.232.223`
- **API 端口**: `9580`
- **API 基础路径**: `/api/v1/generate/v0/`
- **认证方式**: `X-API-Key` Header
- **测试 API Key**: `test-api-key-123456`

## 📡 API 端点

### 1. 生成视频 (POST)
```bash
POST http://localhost:9580/api/v1/generate/v0/image-to-video
Headers:
  X-API-Key: test-api-key-123456
Body (FormData):
  image: [图片文件]
  promptText: [可选提示词]
```

### 2. 查询状态 (GET)
```bash
GET http://localhost:9580/api/v1/generate/v0/videos/{video_id}
Headers:
  X-API-Key: test-api-key-123456
```

## 🚀 快速开始

### 方法 1: 使用自动化脚本 (推荐)

#### macOS/Linux 用户:

1. 打开终端，进入项目目录
2. 运行脚本：
   ```bash
   chmod +x setup_ssh_tunnel.sh
   ./setup_ssh_tunnel.sh
   ```

#### Windows 用户:

1. 确保已安装 OpenSSH 客户端：
   - 设置 → 应用 → 可选功能 → 添加功能 → OpenSSH 客户端
2. 双击运行 `setup_ssh_tunnel.bat`

### 方法 2: 手动设置 SSH 隧道

#### macOS/Linux:
```bash
# 设置密钥文件权限
chmod 600 ssh_key

# 建立 SSH 隧道
ssh -i ssh_key \
    -L 9580:localhost:9580 \
    -N \
    -o "ServerAliveInterval=60" \
    -o "ServerAliveCountMax=3" \
    ec2-user@52.54.232.223
```

#### Windows (PowerShell/CMD):
```cmd
ssh -i ssh_key ^
    -L 9580:localhost:9580 ^
    -N ^
    -o "ServerAliveInterval=60" ^
    -o "ServerAliveCountMax=3" ^
    ec2-user@52.54.232.223
```

## 🌐 使用前端界面

1. **启动 SSH 隧道**（如上所述）

2. **打开前端页面**:
   - 浏览器中打开 `parrot_api_frontend.html`

3. **选择 Testing Provider**:
   - Provider 下拉菜单中选择 `🧪 Testing (New Architecture)`
   - API Key 会自动填充为 `test-api-key-123456`

4. **上传图片并生成**:
   - 上传一张或多张图片
   - 输入提示词（可选）
   - 点击"生成视频"按钮

## 🔍 测试连接

在前端界面中，可以点击 **🔍 Test** 按钮来测试连接是否正常。

成功的连接测试应该显示：
- ✅ Connection test successful!
- Status: 200/201/202

## ❗ 常见问题

### 1. "Connection refused" 或 "Network Error"

**原因**: SSH 隧道未建立或已断开

**解决方案**:
- 检查 SSH 隧道脚本是否在运行
- 确保终端窗口保持打开
- 重新运行 SSH 隧道脚本

### 2. "Permission denied (publickey)"

**原因**: SSH 密钥权限不正确（仅限 macOS/Linux）

**解决方案**:
```bash
chmod 600 ssh_key
```

### 3. "Port 9580 already in use"

**原因**: 端口已被占用

**解决方案**:
```bash
# macOS/Linux
lsof -ti:9580 | xargs kill -9

# Windows
netstat -ano | findstr :9580
taskkill /PID [进程ID] /F
```

### 4. SSH 连接超时

**原因**: 网络问题或服务器不可达

**解决方案**:
- 检查网络连接
- 确认服务器 IP 地址是否正确
- 联系服务器管理员检查服务器状态

## 🔐 安全注意事项

1. **SSH 密钥保护**:
   - `ssh_key` 文件包含私钥，请勿分享或提交到公共代码仓库
   - 已添加到 `.gitignore` 中

2. **API Key 保护**:
   - 测试 API Key (`test-api-key-123456`) 仅用于开发测试
   - 生产环境请使用正式的 API Key

## 📊 调试信息

### 查看详细日志

前端控制台会显示详细的请求/响应信息：
- 按 `F12` 打开开发者工具
- 切换到 Console 标签
- 查看带有 `===` 标记的调试信息

### 手动测试 API

使用 curl 命令直接测试：

```bash
# 测试生成接口
curl -X POST "http://localhost:9580/api/v1/generate/v0/image-to-video" \
     -H "X-API-Key: test-api-key-123456" \
     -F "image=@/path/to/your/image.jpg" \
     -F "promptText=A beautiful sunset"

# 测试查询接口
curl -X GET "http://localhost:9580/api/v1/generate/v0/videos/[video_id]" \
     -H "X-API-Key: test-api-key-123456"
```

## 📝 与其他 Provider 的区别

| 特性 | Testing Backend | Staging/Original |
|------|----------------|------------------|
| 连接方式 | SSH 隧道 → 直连 | 通过代理服务器 |
| API 路径 | `/api/v1/generate/v0/` | `/generate/` 或 `/generate/2.2/` |
| 认证头 | `X-API-Key` | `X-API-KEY` |
| 响应格式 | 新格式 | 旧格式 |
| 状态查询 | 直连 API | 通过代理 |

## 🛠️ 开发者信息

### 修改历史
- 添加了 `testing` provider 配置
- 修改 `checkVideoStatus()` 支持新查询路径
- 修改 `submitTask()` 支持直连请求
- 更新了 UI 下拉选择器

### 相关文件
- `parrot_api_frontend.html` - 前端界面（已更新）
- `setup_ssh_tunnel.sh` - Linux/macOS SSH 隧道脚本
- `setup_ssh_tunnel.bat` - Windows SSH 隧道脚本
- `ssh_key` - SSH 私钥文件（不要分享！）

## 🤝 技术支持

如遇到问题，请提供：
1. 使用的操作系统
2. SSH 隧道是否成功建立
3. 浏览器控制台的错误信息
4. 测试连接的完整响应

---

**注意**: 使用完毕后，记得关闭 SSH 隧道（Ctrl+C）以释放资源。

