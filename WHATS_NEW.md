# 🆕 更新说明 - Testing Backend 集成

**更新日期**: 2025年10月15日

---

## 📦 新增内容

### 1. 新的 Testing Provider
- ✨ 支持新架构后端 (localhost:9580)
- 🔐 通过 SSH 隧道安全连接到远程服务器
- 🎯 新的 API 路径格式: `/api/v1/generate/v0/`

### 2. 自动化脚本工具

#### 🚀 一键启动
```bash
./start_testing.sh
```
自动完成所有设置，包括：
- SSH 密钥权限检查
- 端口冲突检测
- SSH 隧道建立
- 连接测试

#### 🛑 一键停止
```bash
./stop_testing.sh
```
安全停止 SSH 隧道，释放资源

#### 🔧 手动设置
```bash
./setup_ssh_tunnel.sh      # 建立 SSH 隧道
./test_testing_backend.sh  # 测试连接
```

### 3. 完整文档

- 📖 **SETUP_SUMMARY.md** - 配置总结和完整指南
- 🚀 **QUICKSTART_TESTING.md** - 3步快速入门
- 📚 **README_TESTING_BACKEND.md** - 技术详细文档
- 🎉 **本文档** - 更新说明

### 4. 前端增强

`parrot_api_frontend.html` 新功能：
- 新增 Testing Provider 选项（默认选中）
- 自动识别 Provider 类型并选择正确的请求方式
- 支持新的查询路径格式
- Benchmark 模式支持 Testing Provider

---

## 🎯 快速开始

### 最简单的方式（推荐）

```bash
# 1. 一键启动
./start_testing.sh

# 2. 打开浏览器
open parrot_api_frontend.html

# 3. 开始测试！
# Provider 已自动选中 "🧪 Testing (New Architecture)"
```

### 分步方式

```bash
# 1. 建立 SSH 隧道
./setup_ssh_tunnel.sh
# 保持窗口开启！

# 2. (新终端窗口) 测试连接
./test_testing_backend.sh

# 3. 使用前端界面
# 打开 parrot_api_frontend.html
```

---

## 📋 文件列表

### 新增文件 ✨

```
API_Testing-main/
├── start_testing.sh              ⭐ 一键启动脚本
├── stop_testing.sh               ⭐ 一键停止脚本
├── setup_ssh_tunnel.sh           ⭐ SSH 隧道脚本 (Linux/Mac)
├── setup_ssh_tunnel.bat          ⭐ SSH 隧道脚本 (Windows)
├── test_testing_backend.sh       ⭐ 连接测试脚本
├── SETUP_SUMMARY.md              ⭐ 配置总结文档
├── QUICKSTART_TESTING.md         ⭐ 快速入门指南
├── README_TESTING_BACKEND.md     ⭐ 技术详细文档
├── WHATS_NEW.md                  ⭐ 本文档
└── .gitignore                    ⭐ Git 忽略规则
```

### 更新文件 🔄

```
parrot_api_frontend.html          🔄 前端界面（增强功能）
```

---

## 🔄 与现有功能的兼容性

### ✅ 完全兼容
- 所有原有的 Provider（Staging, Original, Minimax）**完全正常工作**
- 现有的 Benchmark 模式继续支持
- 所有现有功能保持不变

### 🆕 新增功能
- Testing Provider 作为新选项添加
- 可在任何时候切换回其他 Provider
- 支持 Testing vs 其他 Provider 的对比测试

---

## 🎮 使用场景

### 场景 1: 快速测试新架构
```bash
./start_testing.sh
```
然后直接使用前端界面

### 场景 2: 对比新旧架构
1. 启用 Benchmark Mode
2. Path A: 选择 Testing
3. Path B: 选择 Original/Staging
4. 上传相同图片，对比结果

### 场景 3: 日常开发
- 早上启动: `./start_testing.sh`
- 工作中: 正常使用前端
- 下班前: `./stop_testing.sh`

---

## 🐛 已知问题和限制

### 1. SSH 隧道需要保持运行
- ⚠️ 关闭终端会断开连接
- 💡 使用 `start_testing.sh` 在后台运行

### 2. 仅支持本地访问
- ⚠️ 只能在运行 SSH 隧道的机器上访问
- 💡 每台开发机器需要独立建立隧道

### 3. Windows 用户注意
- ⚠️ 需要安装 OpenSSH 客户端
- 💡 设置 → 应用 → 可选功能 → OpenSSH 客户端

---

## 🔍 验证更新

运行以下命令确认所有文件都已正确设置：

```bash
# 检查所有脚本文件
ls -la *.sh

# 应该看到以下文件都有执行权限 (x):
# -rwxr-xr-x  setup_ssh_tunnel.sh
# -rwxr-xr-x  start_testing.sh
# -rwxr-xr-x  stop_testing.sh
# -rwxr-xr-x  test_testing_backend.sh

# 检查文档文件
ls -la *.md

# 应该看到:
# SETUP_SUMMARY.md
# QUICKSTART_TESTING.md
# README_TESTING_BACKEND.md
# WHATS_NEW.md
```

---

## 📊 技术变更摘要

### HTML 代码变更

1. **新增 Testing Provider 配置**
   ```javascript
   'testing': {
       name: 'Testing (New Architecture)',
       baseUrl: 'http://localhost:9580',
       apiKey: 'test-api-key-123456',
       versions: { ... }
   }
   ```

2. **修改请求逻辑**
   - Testing: 直连 `localhost:9580`
   - 其他: 通过代理服务器

3. **修改查询逻辑**
   - Testing: `/api/v1/generate/v0/videos/{id}`
   - 其他: `/videos/{id}?provider=xxx`

---

## 🎓 学习资源

### 入门级
1. 阅读 `QUICKSTART_TESTING.md`
2. 运行 `./start_testing.sh`
3. 开始使用

### 进阶级
1. 阅读 `README_TESTING_BACKEND.md`
2. 了解 SSH 隧道原理
3. 学习 API 差异

### 专家级
1. 阅读 `SETUP_SUMMARY.md`
2. 查看 HTML 源代码中的注释
3. 自定义配置

---

## 💬 反馈和支持

### 遇到问题？

1. **查看文档**
   - `QUICKSTART_TESTING.md` - 快速问题
   - `README_TESTING_BACKEND.md` - 详细问题

2. **运行诊断**
   ```bash
   ./test_testing_backend.sh
   ```

3. **检查日志**
   - 浏览器控制台 (F12)
   - 终端输出

### 报告 Bug

提供以下信息：
- 操作系统版本
- 错误信息截图
- `./test_testing_backend.sh` 输出
- 浏览器控制台日志

---

## 🗺️ 未来计划

- [ ] Windows 版本的一键启动脚本
- [ ] 自动重连机制
- [ ] 连接状态实时监控
- [ ] 多服务器支持
- [ ] 配置文件管理

---

## 🙏 致谢

感谢所有参与测试和反馈的团队成员！

---

**版本**: v1.0.0  
**最后更新**: 2025-10-15  
**状态**: ✅ 稳定可用

---

<div align="center">

**🎉 祝测试愉快！🎉**

[快速入门](QUICKSTART_TESTING.md) | [完整文档](README_TESTING_BACKEND.md) | [配置总结](SETUP_SUMMARY.md)

</div>

