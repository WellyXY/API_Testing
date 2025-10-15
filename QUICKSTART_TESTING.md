# 🚀 Testing Backend 快速入门

只需 3 步即可开始使用新的测试后端！

## 步骤 1: 建立 SSH 隧道 🔐

### macOS/Linux:
```bash
./setup_ssh_tunnel.sh
```

### Windows:
双击运行 `setup_ssh_tunnel.bat`

**保持这个窗口开启！** 关闭会断开连接。

---

## 步骤 2: 测试连接（可选）✅

在**新的**终端窗口中运行：

```bash
./test_testing_backend.sh
```

如果看到 "✅ 测试成功！"，说明一切正常！

---

## 步骤 3: 使用前端界面 🎨

1. 打开浏览器，访问 `parrot_api_frontend.html`

2. 在 **Provider** 下拉菜单中选择：
   ```
   🧪 Testing (New Architecture)
   ```

3. API Key 会自动填充（`test-api-key-123456`）

4. 上传图片，点击"生成视频"！

---

## 🔥 一键启动（仅 macOS/Linux）

如果你想一键完成所有测试：

```bash
# 在一个终端窗口运行（保持开启）
./setup_ssh_tunnel.sh

# 在另一个终端窗口测试
./test_testing_backend.sh
```

---

## ❓ 常见问题

### "Connection refused" 错误？
➡️ SSH 隧道可能没启动，运行 `./setup_ssh_tunnel.sh`

### "Permission denied" 错误？
➡️ 运行：`chmod 600 ssh_key`

### 端口 9580 被占用？
```bash
# macOS/Linux
lsof -ti:9580 | xargs kill -9

# Windows
netstat -ano | findstr :9580
taskkill /PID [进程ID] /F
```

---

## 📚 需要更多帮助？

查看详细文档：[README_TESTING_BACKEND.md](./README_TESTING_BACKEND.md)

---

**提示**: 使用完毕记得按 `Ctrl+C` 关闭 SSH 隧道！

