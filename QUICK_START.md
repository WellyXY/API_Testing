# 🚀 快速启动指南

## 一键启动服务器

```bash
./start_server.sh
```

就这么简单！脚本会自动处理所有事情。

---

## 启动后

1. **服务器运行在**: `http://localhost:8000`

2. **打开前端**: 在浏览器中打开 `parrot_api_frontend.html`

3. **开始测试**！

---

## 功能列表

### ✅ 基础功能
- 图片转视频 (i2v)
- 多图片批量处理
- 不同 Provider 切换

### ✅ 高级功能
- 参考图片模式 (i2i → i2v)
- **Sticking Video** - AI 生成 3 个变体
- Benchmark 对比模式

### ✅ Testing Backend
- 新架构测试（需要 SSH 隧道）
- 运行 `./start_testing.sh`

---

## 常用命令

```bash
# 启动服务器
./start_server.sh

# 启动 Testing Backend（SSH 隧道）
./start_testing.sh

# 停止 Testing Backend
./stop_testing.sh

# 测试 Testing Backend 连接
./test_testing_backend.sh
```

---

## ⚠️ 遇到问题？

### "No module named 'PIL'" 错误
```bash
./start_server.sh
```
脚本会自动安装依赖

### "Connection refused" （Testing Backend）
```bash
./start_testing.sh
```

### 查看详细文档
- Sticking Video 问题: `STICKING_VIDEO_FIX.md`
- Testing Backend: `QUICKSTART_TESTING.md`
- 完整检查列表: `CHECKLIST.md`

---

<div align="center">

**🎬 开始创作精彩视频吧！**

</div>

