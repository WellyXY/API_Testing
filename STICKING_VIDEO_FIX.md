# 🔧 Sticking Video 功能修复说明

## ❌ 遇到的问题

使用 Sticking Video 功能时出现错误：
```
{"error":"No module named 'PIL'"}
```

这是因为缺少必要的 Python 依赖包。

---

## ✅ 解决方案

### 问题原因
Sticking Video 功能需要以下 Python 包：
- **Pillow** - 图像处理库
- **google-cloud-aiplatform** - Google Vertex AI SDK（用于 Gemini API）

### 已完成的修复

1. ✅ **更新了 `requirements.txt`**
   ```
   Flask
   Flask-CORS
   requests
   zipfile36
   Pillow              ← 新增
   google-cloud-aiplatform  ← 新增
   ```

2. ✅ **创建了虚拟环境并安装依赖**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. ✅ **创建了自动启动脚本**
   - `start_server.sh` - 自动激活虚拟环境并启动服务器

---

## 🚀 现在怎么使用？

### 方法 1: 使用启动脚本（推荐）

```bash
./start_server.sh
```

脚本会自动：
- 检查/创建虚拟环境
- 激活虚拟环境
- 安装/更新依赖
- 启动服务器

### 方法 2: 手动启动

```bash
# 1. 激活虚拟环境
source venv/bin/activate

# 2. 启动服务器
python parrot_proxy_server.py
# 或
python parrot_batch_server.py
```

---

## 📋 验证修复

### 1. 启动服务器
```bash
./start_server.sh
```

### 2. 打开前端
在浏览器中打开 `parrot_api_frontend.html`

### 3. 测试 Sticking Video
1. 启用 **🎬 Sticking Video (AI Prompt Generation)** 开关
2. 上传一张图片
3. 输入视频提示词（Video Prompt）
4. 点击 **🎬 Generate Sticking Videos (3x)**

### 4. 预期结果
- ✅ 不再出现 "No module named 'PIL'" 错误
- ✅ AI 自动生成 3 个图片变体
- ✅ 每个变体生成对应的视频
- ✅ 最终得到 3 个视频

---

## 🔍 Sticking Video 功能说明

### 什么是 Sticking Video？

Sticking Video 是一个 AI 增强的视频生成功能：

1. **输入**：
   - 一张参考图片
   - 一个视频提示词

2. **AI 处理**：
   - Gemini AI 分析参考图片
   - 生成 3 个不同的图片变体提示词（Image Prompts）
   - 生成 3 个对应的视频提示词（Video Prompts）

3. **视频生成**：
   - 对每个图片提示词，生成图片变体（i2i）
   - 对每个图片变体，生成视频（i2v）
   - 最终输出 3 个视频

4. **输出**：
   - 3 个不同风格的视频
   - 可以合并下载（带转场效果）

### 工作流程

```
参考图片 + 视频提示词
    ↓
[Gemini AI 分析]
    ↓
3个图片提示词 + 3个视频提示词
    ↓
[Seedream i2i] → 图片变体 1 → [i2v] → 视频 1
                → 图片变体 2 → [i2v] → 视频 2
                → 图片变体 3 → [i2v] → 视频 3
    ↓
合并下载（可选）
```

---

## 🛠️ 技术依赖

### Python 包
- **Pillow (PIL)**: 图像处理和格式转换
- **google-cloud-aiplatform**: Google Vertex AI SDK
- **vertexai**: Gemini API 访问

### API 服务
- **Gemini 2.5 Flash**: 用于图片分析和提示词生成
- **Seedream**: 图片变体生成（i2i）
- **Parrot API**: 视频生成（i2v）

---

## 📊 依赖检查

### 验证 Pillow 安装
```bash
source venv/bin/activate
python -c "from PIL import Image; print('✅ Pillow 已安装')"
```

### 验证 Vertex AI 安装
```bash
source venv/bin/activate
python -c "import vertexai; print('✅ Vertex AI SDK 已安装')"
```

### 查看所有已安装的包
```bash
source venv/bin/activate
pip list
```

---

## ⚠️ 重要提示

### 1. 虚拟环境
- 所有依赖安装在 `venv/` 目录中
- **必须激活虚拟环境**才能运行服务器
- 使用 `./start_server.sh` 会自动激活

### 2. Vertex AI 认证
Sticking Video 需要 Vertex AI 认证文件：
- `vertex-ai.json`（本地）
- 或 `/mnt/nfs/chenlin/dataproc/vertex-ai.json`（集群）

如果没有这些文件，Sticking Video 功能将无法使用。

### 3. 虚拟环境位置
`venv/` 目录已添加到 `.gitignore`，不会提交到代码仓库。

---

## 🆚 与普通 i2v 的区别

| 特性 | 普通 i2v | Sticking Video |
|------|---------|---------------|
| 输入 | 1张图片 + 提示词 | 1张图片 + 提示词 |
| AI 增强 | ❌ | ✅ Gemini AI 分析 |
| 输出数量 | 1个视频 | 3个视频 |
| 图片变体 | ❌ | ✅ 3个 AI 生成的变体 |
| 合并下载 | ❌ | ✅ 支持转场效果 |

---

## 🐛 故障排查

### 1. "No module named 'PIL'"
```bash
# 确认虚拟环境已激活
which python
# 应该显示: /Users/welly/Downloads/API_Testing-main/venv/bin/python

# 重新安装依赖
source venv/bin/activate
pip install Pillow
```

### 2. "No module named 'vertexai'"
```bash
source venv/bin/activate
pip install google-cloud-aiplatform
```

### 3. 服务器无法启动
```bash
# 使用启动脚本（会自动检查环境）
./start_server.sh
```

### 4. Vertex AI 认证失败
确保存在以下文件之一：
- `vertex-ai.json`
- `/mnt/nfs/chenlin/dataproc/vertex-ai.json`

---

## 📝 更新日志

**2025-10-15**
- ✅ 修复了 PIL 缺失问题
- ✅ 添加了 google-cloud-aiplatform 依赖
- ✅ 创建了虚拟环境
- ✅ 添加了自动启动脚本 `start_server.sh`
- ✅ 更新了 `requirements.txt`

---

## 🎉 总结

问题已完全解决！现在你可以：

1. ✅ 使用 `./start_server.sh` 启动服务器
2. ✅ 正常使用 Sticking Video 功能
3. ✅ 生成 3 个 AI 增强的视频变体
4. ✅ 合并下载带转场效果的视频

---

<div align="center">

**🦜 Enjoy Sticking Video! 🎬**

需要帮助？查看控制台日志或联系技术支持

</div>

