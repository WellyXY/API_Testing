# 🎯 新架构测试后端配置总结

## ✅ 已完成的修改

### 1. 前端界面更新 (`parrot_api_frontend.html`)

#### 新增功能：
- ✅ 添加了 **Testing Provider** 配置
  - 基础 URL: `http://localhost:9580`
  - API 路径: `/api/v1/generate/v0/`
  - 默认 API Key: `test-api-key-123456`

- ✅ 修改了 **API 请求逻辑**
  - Testing provider 直接请求本地 9580 端口
  - 其他 provider 继续使用代理服务器
  - 支持新的 API 路径格式

- ✅ 更新了 **状态查询逻辑**
  - Testing provider: `GET /api/v1/generate/v0/videos/{id}`
  - 其他 provider: 使用原有代理方式

- ✅ UI 更新
  - Provider 下拉菜单新增 "🧪 Testing (New Architecture)" 选项
  - 默认选中 Testing provider
  - Benchmark 模式也支持 Testing provider

### 2. SSH 隧道脚本

创建了两个版本的 SSH 隧道脚本：

#### `setup_ssh_tunnel.sh` (macOS/Linux)
- 自动设置 SSH 密钥权限（600）
- 建立端口转发：`localhost:9580 → 52.54.232.223:9580`
- 包含连接保活配置
- 已添加执行权限 ✅

#### `setup_ssh_tunnel.bat` (Windows)
- Windows 版本的 SSH 隧道脚本
- 自动检测 SSH 客户端
- 相同的端口转发配置

### 3. 测试脚本

#### `test_testing_backend.sh`
- 自动检测端口 9580 是否开放
- 创建测试图片并发送 API 请求
- 验证连接、认证和 API 响应
- 提供详细的诊断信息
- 已添加执行权限 ✅

### 4. 文档

#### `README_TESTING_BACKEND.md`
- 完整的技术文档
- API 端点详细说明
- 故障排查指南
- 与其他 Provider 的对比

#### `QUICKSTART_TESTING.md`
- 3 步快速入门指南
- 常见问题快速解答

---

## 🚀 开始使用（3 个步骤）

### 步骤 1: 启动 SSH 隧道

打开终端，运行：

```bash
cd /Users/welly/Downloads/API_Testing-main
./setup_ssh_tunnel.sh
```

**重要**: 保持这个终端窗口开启！

### 步骤 2: 测试连接（可选但推荐）

打开**新的**终端窗口，运行：

```bash
cd /Users/welly/Downloads/API_Testing-main
./test_testing_backend.sh
```

期望看到：
```
✅ 测试成功！
   - SSH 隧道工作正常
   - API 服务可访问
   - 认证通过
```

### 步骤 3: 使用前端界面

1. 在浏览器中打开 `parrot_api_frontend.html`

2. 确认 Provider 选择为 **"🧪 Testing (New Architecture)"**

3. API Key 应该已自动填充为 `test-api-key-123456`

4. 上传图片并生成视频！

---

## 📋 技术架构说明

### 连接流程

```
浏览器 → localhost:9580 → SSH隧道 → 52.54.232.223:9580 → API服务
```

### 为什么需要 SSH 隧道？

1. **远程服务器不公开访问**: API 服务运行在私有 EC2 实例上
2. **安全性**: 通过 SSH 加密传输
3. **灵活性**: 可以在本地测试远程服务

### API 对比

| 功能 | Testing Backend | Original/Staging |
|------|----------------|------------------|
| 提交任务 | POST `/api/v1/generate/v0/image-to-video` | POST `/generate/v0/image-to-video` |
| 查询状态 | GET `/api/v1/generate/v0/videos/{id}` | GET `/videos/{id}?provider=xxx` |
| 连接方式 | 直连 localhost:9580 | 通过代理服务器 |
| 认证头 | `X-API-Key` | `X-API-KEY` |

---

## 🔍 验证配置

### 检查 SSH 隧道是否运行

```bash
# macOS/Linux
lsof -i :9580

# 应该看到 ssh 进程占用 9580 端口
```

### 手动测试 API

```bash
# 测试查询端点
curl -X GET "http://localhost:9580/api/v1/generate/v0/videos/test-id" \
     -H "X-API-Key: test-api-key-123456"

# 应该返回 JSON 响应（可能是 404，但说明连接正常）
```

---

## 🐛 故障排查

### 问题 1: "Connection refused"

**症状**: 前端显示网络错误

**原因**: SSH 隧道未建立

**解决**:
1. 检查 SSH 隧道窗口是否还在运行
2. 重新运行 `./setup_ssh_tunnel.sh`

---

### 问题 2: "Permission denied (publickey)"

**症状**: SSH 隧道无法建立

**原因**: SSH 密钥权限不正确

**解决**:
```bash
chmod 600 ssh_key
./setup_ssh_tunnel.sh
```

---

### 问题 3: 端口已被占用

**症状**: "Address already in use"

**解决**:
```bash
# 查找并终止占用 9580 端口的进程
lsof -ti:9580 | xargs kill -9

# 然后重新启动隧道
./setup_ssh_tunnel.sh
```

---

### 问题 4: 前端 Test 按钮失败

**可能原因**:
1. SSH 隧道未运行 → 运行 `./setup_ssh_tunnel.sh`
2. 远程服务器宕机 → 联系管理员
3. API Key 错误 → 检查是否为 `test-api-key-123456`

**调试步骤**:
1. 按 F12 打开浏览器控制台
2. 查看 Console 标签的错误信息
3. 查看 Network 标签的请求详情

---

## 📁 项目文件结构

```
API_Testing-main/
├── parrot_api_frontend.html       # 前端界面（已更新 ✅）
├── ssh_key                         # SSH 私钥（不要分享！）
├── setup_ssh_tunnel.sh            # SSH 隧道脚本 (macOS/Linux) ✅
├── setup_ssh_tunnel.bat           # SSH 隧道脚本 (Windows) ✅
├── test_testing_backend.sh        # 测试脚本 ✅
├── README_TESTING_BACKEND.md      # 完整文档 ✅
├── QUICKSTART_TESTING.md          # 快速入门 ✅
└── SETUP_SUMMARY.md               # 本文档 ✅
```

---

## 🎓 使用建议

### 开发流程

1. **启动会话时**:
   ```bash
   ./setup_ssh_tunnel.sh  # 启动隧道
   ```

2. **测试连接**:
   ```bash
   ./test_testing_backend.sh  # 验证一切正常
   ```

3. **开始工作**:
   - 打开 `parrot_api_frontend.html`
   - 选择 Testing provider
   - 开始测试

4. **结束会话时**:
   - 在 SSH 隧道窗口按 `Ctrl+C`
   - 关闭浏览器

### 多个 Provider 对比

前端支持 Benchmark 模式，可以同时对比两个 Provider：

1. 启用 "Benchmark Mode" 开关
2. Path A: 选择 Testing
3. Path B: 选择 Original 或 Staging
4. 上传相同图片，对比结果

---

## 🔒 安全提醒

1. **ssh_key 文件**
   - 包含私钥，不要分享
   - 不要提交到 Git
   - 权限应为 600

2. **API Key**
   - `test-api-key-123456` 仅用于测试
   - 生产环境使用不同的 Key

3. **SSH 隧道**
   - 仅在需要时开启
   - 不使用时关闭以节省资源

---

## 📞 技术支持

遇到问题时，请提供：

1. **系统信息**:
   ```bash
   uname -a
   ssh -V
   ```

2. **SSH 隧道状态**:
   ```bash
   lsof -i :9580
   ```

3. **测试脚本输出**:
   ```bash
   ./test_testing_backend.sh
   ```

4. **浏览器控制台日志**:
   - F12 → Console 标签
   - 截图或复制错误信息

---

## ✨ 下一步

现在你可以：

1. ✅ 使用新的测试后端架构
2. ✅ 对比不同 Provider 的性能
3. ✅ 测试新的 API 功能
4. ✅ 报告 Bug 或提供反馈

---

**祝测试愉快！** 🎉

有任何问题，随时查阅 [README_TESTING_BACKEND.md](./README_TESTING_BACKEND.md) 获取更多详情。

