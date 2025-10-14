# 图片质量说明

## 📊 当前图片质量情况

### 🔍 为什么图片看起来模糊？

1. **API 限制**
   - Seedream 4.0 API 目前最大支持 `1024x1024` 分辨率
   - 这是 BytePlus ModelArk 平台的限制
   - 文件大小通常在 200-300KB 左右

2. **压缩和水印**
   - 平台会自动添加水印（"AI generated"）
   - 图片经过压缩以减少传输大小
   - JPEG 格式会有一定的质量损失

## ✅ 已做的优化

### 脚本自动添加的质量关键词：
```
ultra high quality
8K resolution
highly detailed
sharp focus
professional photography
masterpiece
best quality
high resolution
```

这些关键词会引导模型生成更高质量的图像，但仍受限于 API 的最大分辨率。

## 🎯 提升质量的方法

### 方法1: 使用质量关键词（已实现）
脚本已自动添加高质量关键词到您的 prompt 中。

### 方法2: 后期处理
下载图片后，可以使用图片放大工具：
- **Topaz Gigapixel AI** - 专业 AI 图片放大
- **waifu2x** - 开源图片放大工具
- **Real-ESRGAN** - AI 超分辨率放大

### 方法3: 调整 prompt
在您的 prompt 中明确要求：
- "high resolution"
- "4K quality"
- "extremely detailed"
- "professional photography"

### 方法4: 联系 BytePlus
如果需要更高分辨率，可能需要：
- 联系 BytePlus 技术支持
- 询问是否有高分辨率 API 选项
- 或使用其他支持更高分辨率的 API 服务

## 📋 当前配置

- **模型**: Seedream 4.0 (`ep-20250921042133-t769x`)
- **最大分辨率**: 1024x1024
- **输出格式**: JPEG with watermark
- **质量增强**: 自动添加高质量关键词

## 💡 建议

1. **先生成后放大**: 使用脚本生成图片，然后用专业工具放大
2. **优化 prompt**: 在 prompt 中详细描述质量要求
3. **批次管理**: 使用批次文件夹功能方便管理不同版本

---
**注意**: 图片模糊主要是由于 API 分辨率限制，而非生成质量问题。生成的图像在 1024x1024 分辨率下通常是清晰的，但在大屏幕或放大查看时会显得模糊。
