# ✅ Testing Backend 使用检查列表

## 🎯 首次设置检查

### 环境检查
- [ ] macOS/Linux 系统或已安装 OpenSSH 的 Windows
- [ ] `ssh_key` 文件存在于项目目录
- [ ] 有网络连接到 52.54.232.223

### 文件检查
```bash
# 运行此命令检查所有文件
ls -la *.sh *.md ssh_key

# 应该看到:
# ✅ setup_ssh_tunnel.sh (可执行)
# ✅ start_testing.sh (可执行)
# ✅ stop_testing.sh (可执行)
# ✅ test_testing_backend.sh (可执行)
# ✅ ssh_key (权限 600 或 -rw-------)
# ✅ 各种 .md 文档文件
```

---

## 🚀 每次使用前检查

### 启动前
- [ ] 端口 9580 未被占用
  ```bash
  lsof -i :9580
  # 应该没有输出，或只有之前的 SSH 隧道
  ```

- [ ] SSH 密钥权限正确
  ```bash
  ls -la ssh_key
  # 应该显示: -rw------- 或类似 (600)
  ```

### 启动步骤
- [ ] 运行 `./start_testing.sh`
- [ ] 看到 "✅ SSH 隧道已启动"
- [ ] 看到 "✅ API 服务可访问"
- [ ] 看到 "🎉 设置完成！"

### 可选：测试连接
- [ ] 运行 `./test_testing_backend.sh`
- [ ] 看到 "✅ 测试成功！"

---

## 🌐 使用前端检查

### 打开前端
- [ ] 在浏览器中打开 `parrot_api_frontend.html`
- [ ] 看到界面正常加载

### Provider 配置
- [ ] Provider 下拉菜单显示 "🧪 Testing (New Architecture)"
- [ ] Version 自动显示 "Testing v1"
- [ ] API Key 自动填充为 `test-api-key-123456`

### 连接测试（可选）
- [ ] 点击 "🔍 Test" 按钮
- [ ] 看到绿色成功消息
- [ ] 或看到响应状态（200/201/404/401 都说明连接正常）

---

## 🎬 生成视频检查

### 上传图片
- [ ] 点击上传区域或拖拽图片
- [ ] 看到图片预览
- [ ] 图片数量显示正确

### 生成过程
- [ ] 点击 "🚀 Generate Videos" 按钮
- [ ] 看到 "Processing Progress" 区域
- [ ] 看到任务卡片出现
- [ ] 任务状态从 "submitting" → "waiting" → "processing" → "completed"

### 结果验证
- [ ] 视频能够在任务卡片中播放
- [ ] 可以下载视频
- [ ] 视频质量正常

---

## 🐛 故障排查检查

### 如果显示 "Connection refused"
- [ ] SSH 隧道是否在运行？
  ```bash
  lsof -i :9580
  ```
- [ ] 如果没有，运行 `./start_testing.sh`

### 如果 SSH 隧道无法建立
- [ ] 检查 SSH 密钥权限
  ```bash
  chmod 600 ssh_key
  ```
- [ ] 检查网络连接
  ```bash
  ping 52.54.232.223
  ```
- [ ] 查看 SSH 详细输出
  ```bash
  ssh -i ssh_key -v ec2-user@52.54.232.223
  ```

### 如果前端显示错误
- [ ] 打开浏览器控制台 (F12)
- [ ] 查看 Console 标签的错误
- [ ] 查看 Network 标签的请求状态
- [ ] 确认 Provider 选择正确

---

## 🔄 切换 Provider 检查

### 切换到其他 Provider
- [ ] 在 Provider 下拉菜单选择其他选项
- [ ] API Key 自动更新
- [ ] Version 选项正确显示
- [ ] 功能正常工作

### 切换回 Testing Provider
- [ ] 选择 "🧪 Testing (New Architecture)"
- [ ] 确认 SSH 隧道仍在运行
- [ ] 测试连接正常

---

## 📊 Benchmark 模式检查

### 启用 Benchmark
- [ ] 切换 "Benchmark Mode" 开关
- [ ] 看到 Path A 和 Path B 配置区域

### 配置对比
- [ ] Path A: 选择 Testing
- [ ] Path B: 选择其他 Provider
- [ ] 分别输入不同的 Prompt（可选）

### 查看结果
- [ ] 上传相同的图片
- [ ] 看到两个视频并排显示
- [ ] 可以对比播放效果

---

## 🛑 使用结束检查

### 清理步骤
- [ ] 关闭浏览器（可选）
- [ ] 运行 `./stop_testing.sh`
- [ ] 确认 SSH 隧道已停止
  ```bash
  lsof -i :9580
  # 应该没有输出
  ```

### 下次使用
- [ ] 记住只需运行 `./start_testing.sh` 即可

---

## 📝 定期检查（可选）

### 每周
- [ ] 检查是否有新的文档更新
- [ ] 清理 output_audio 目录（如果太大）
- [ ] 备份重要的测试结果

### 每月
- [ ] 确认 API Key 是否仍然有效
- [ ] 检查 SSH 密钥是否需要更新
- [ ] 查看是否有新版本

---

## 🎓 学习进度检查

### 初级（必须）
- [ ] 阅读 `QUICKSTART_TESTING.md`
- [ ] 成功运行 `./start_testing.sh`
- [ ] 成功生成一个视频

### 中级（推荐）
- [ ] 阅读 `README_TESTING_BACKEND.md`
- [ ] 理解 SSH 隧道的作用
- [ ] 成功使用 Benchmark 模式

### 高级（可选）
- [ ] 阅读 `SETUP_SUMMARY.md`
- [ ] 理解前端代码的修改
- [ ] 能够自己诊断和解决问题

---

## 🆘 需要帮助？

如果任何检查项失败：

1. **查阅文档**
   - 问题简单？→ `QUICKSTART_TESTING.md`
   - 问题复杂？→ `README_TESTING_BACKEND.md`

2. **运行诊断**
   ```bash
   ./test_testing_backend.sh
   ```

3. **查看日志**
   - 浏览器控制台 (F12)
   - 终端输出

4. **获取支持**
   - 提供以上诊断信息
   - 包含错误截图

---

## ✨ 高级用户检查列表

### 自定义配置
- [ ] 修改 API Key（如需要）
- [ ] 调整并发数量
- [ ] 自定义 Prompt

### 性能优化
- [ ] 监控网络延迟
- [ ] 测试不同图片大小的影响
- [ ] 比较不同 Provider 的速度

### 开发调试
- [ ] 使用浏览器开发者工具
- [ ] 查看详细的 API 请求/响应
- [ ] 分析任务执行时间

---

<div align="center">

**📋 使用此检查列表确保每次都能顺利运行！**

建议：打印或保存此文件以便随时参考

</div>

