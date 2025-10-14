# i2i + i2v 工作流功能说明

## 🎨 功能概述

这个功能允许你先通过 Seedream API 对上传的图片进行 i2i (image-to-image) 处理，生成新的图片，然后再使用 Pika API 进行 i2v (image-to-video) 转换。

## 📋 工作流程

```
原始图片 → [i2i: Seedream] → 生成的图片 → [i2v: Pika] → 视频
```

## 🚀 使用步骤

### 1. 启动服务器

```bash
cd "/Users/welly/Downloads/API_Testing-main 3"
python3 parrot_proxy_server.py
```

服务器将在 `http://localhost:5003` 启动

### 2. 打开前端页面

在浏览器中访问：`http://localhost:5003`

### 3. 上传图片

- 拖拽或点击上传区域选择图片
- 支持多张图片批量处理

### 4. 启用 i2i 模式

在 "Step 3: Prompt & Generate" 区域：

1. **打开 i2i 开关**
   - 点击 "Enable i2i (Image-to-Image)" 右侧的开关
   - 开关变为蓝色表示已启用

2. **输入 i2i Prompt**
   - 在 "i2i Prompt" 文本框中输入图片生成的描述
   - 例如：`a beautiful woman in a red dress, elegant pose, professional photography, high quality`
   - 这个 prompt 用于 Seedream 生成新图片

3. **输入 Video Prompt**
   - 在 "Video Prompt" 文本框中输入视频效果描述
   - 例如：`gentle movement, cinematic lighting, smooth transition`
   - 这个 prompt 用于 Pika 生成视频

### 5. 开始生成

点击 **"🎨 Generate Images → Videos (i2i + i2v)"** 按钮

## 📊 处理过程

系统会显示以下进度：

1. **🎨 Processing i2i...** - 正在通过 Seedream 处理图片
2. **✅ i2i completed** - 图片生成完成
3. **🚀 Generating video...** - 正在通过 Pika 生成视频
4. **✅ Video ready** - 视频生成完成

## 🔧 API 配置

### Seedream API
- **Base URL**: `https://ark.ap-southeast.bytepluses.com/api/v3`
- **Model**: `ep-20250921042133-t769x`
- **Output Size**: `1440x2560`
- **API Key**: 已配置在服务器端

### Pika API
- 使用前端页面中选择的 API 提供商和版本
- 支持 Original 和 Staging 两个环境

## 📝 示例

### 示例 1：人物风格转换 + 视频
```
原始图片：一张普通的人物照片

i2i Prompt：
elegant woman in traditional Chinese dress, professional photography, 
soft lighting, high quality, detailed

Video Prompt：
gentle head turn, soft smile, cinematic lighting, smooth camera movement

结果：生成穿着传统中式服装的人物视频
```

### 示例 2：场景重建 + 动画
```
原始图片：一张风景照片

i2i Prompt：
fantasy landscape with magical elements, vibrant colors, 
anime style, detailed artwork

Video Prompt：
magical particles floating, camera pan, dynamic lighting effects

结果：生成具有幻想风格的动态场景视频
```

## ⚠️ 注意事项

1. **处理时间**
   - i2i 处理通常需要 30-60 秒
   - i2v 处理需要额外的时间（视 Pika API 状态而定）
   - 总处理时间可能需要 2-5 分钟

2. **图片要求**
   - Seedream API 最大支持 10MB 的图片
   - 系统会自动压缩和优化图片

3. **Prompt 质量**
   - i2i Prompt 越详细，生成的图片质量越好
   - Video Prompt 建议描述动作和效果，而非静态内容

4. **错误处理**
   - 如果 i2i 失败，不会进行 i2v 步骤
   - 错误信息会显示在页面上
   - 可以在浏览器控制台查看详细日志

## 🎯 高级功能

### 批量处理
- 上传多张图片
- 系统会依次处理每张图片的 i2i + i2v
- 所有任务会显示在任务列表中

### 任务标识
- 使用 i2i 模式生成的任务会显示 `[i2i]` 标签
- 可以在任务卡片中查看 i2i prompt 信息

### 日志下载
- 点击 "📥 Logs" 按钮下载处理日志
- 包含所有 API 调用的详细信息

## 🔍 故障排查

### i2i 处理失败
1. 检查 Seedream API 是否正常
2. 确认图片大小是否超过限制
3. 检查 i2i Prompt 是否有效

### i2v 处理失败
1. 检查 Pika API 配置
2. 确认 API Key 是否有效
3. 查看服务器日志获取详细错误信息

### 图片无法下载
1. 检查网络连接
2. 确认生成的图片 URL 是否有效
3. 可能需要使用代理或 VPN

## 📚 相关文档

- [Seedream API 文档](../seadream-main/README.md)
- [Pika API 配置](./README.md)
- [批量处理指南](./README_BATCH.md)

## 🆘 支持

如遇问题，请：
1. 检查浏览器控制台错误
2. 查看服务器终端日志
3. 确认所有依赖已正确安装

