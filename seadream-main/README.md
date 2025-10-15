# 🎨 Seedream 图像生成器

一个基于 Seedream API 的图像生成工具，提供 Web 界面和命令行工具。支持本地运行和 Vercel 云端部署。

## ✨ 特性

- 🌐 **现代化 Web 界面** - 美观的任务队列管理
- 🖼️ **多图片支持** - 支持上传多张参考图片
- 🚀 **快速部署** - 一键部署到 Vercel
- 🔧 **命令行工具** - 丰富的 Shell 脚本工具集
- 📱 **响应式设计** - 完美适配桌面和移动端

## 🚀 快速开始

### Web 界面（推荐）

#### 本地运行
```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务器
python3 seedream_server_v2.py

# 在浏览器中打开
open http://localhost:8888
```

#### Vercel 部署
查看详细的部署指南：[DEPLOY.md](DEPLOY.md)

简要步骤：
1. Fork 本仓库到你的 GitHub
2. 在 [Vercel](https://vercel.com) 导入项目
3. 配置环境变量 `SEEDREAM_API_KEY`
4. 一键部署 🎉

### 命令行工具

## 📁 文件夹说明

### 🖼️ `images/` - 图像文件
- **`ref/`** - 参考图片
  - `elegant_woman_portrait.jpeg` - 原始参考女性肖像
  
- **`generated/`** - AI生成的图片
  - `quick_gen_*.jpeg` - 使用快速生成脚本创建的图片
  - `woman_bikini_portrait.jpeg` - 比基尼风格图片
  - `seededit_sim_*.jpeg` - 模拟SeedEdit生成的图片
  - `seedream_4_i2i_result.jpeg` - Seedream 4.0 i2i编辑结果

### 🛠️ `scripts/` - 脚本工具
- **图像生成脚本**
  - `quick_generate.sh` - 快速图像生成工具
  - `seedream_i2i.sh` - Seedream 4.0 图像编辑工具 ⭐
  - `interactive_i2i.sh` - 交互式图像生成工具
  
- **测试脚本**
  - `test_seedream.py` - Python测试脚本
  - `test_seedream_curl.sh` - Curl测试脚本
  - `complete_api_test.sh` - 完整API测试
  - `seededit_test.sh` - SeedEdit测试脚本
  
- **其他工具**
  - `simulate_seededit.sh` - 模拟SeedEdit功能
  - `reference_based_generate.sh` - 基于参考图像生成

### 📚 `docs/` - 文档文件
- **定价文档**
  - `Character_Training_Pricing_Plan.md` - 中文版定价计划
  - `Character_Training_Pricing_Plan_EN.md` - 英文版定价计划
  
- **流程文档**
  - `Model_Release_Pipeline_CN.md` - 中文版模型上线流程
  - `Model_Release_Pipeline_EN.md` - 英文版模型上线流程
  
- **会议文档**
  - `会议讨论要点_CN.md` - 中文会议要点
  - `Meeting_Discussion_Points_EN.md` - 英文会议要点

## 🎯 推荐使用的工具

### 图像生成
```bash
# 快速生成图像
./scripts/quick_generate.sh "your prompt here"

# 图像编辑 (i2i) - 推荐！
./scripts/seedream_i2i.sh
```

### API配置
- **API Key**: `70f23192-0f0c-47d2-9bbf-961f70a17a92`
- **Seedream 4.0 模型**: `ep-20250921042133-t769x`
- **Base URL**: `https://ark.ap-southeast.bytepluses.com/api/v3`

## ⚠️ 注意事项

1. **AI水印**: 所有生成的图片都会有"AI generated"水印，这是平台默认设置
2. **文件权限**: 脚本文件已设置为可执行权限
3. **图像格式**: 支持JPEG、PNG等常见格式

## 🔧 维护说明

- 新的参考图片请放入 `images/ref/`
- AI生成的图片会自动保存到 `images/generated/`
- 新脚本请放入 `scripts/` 并添加执行权限
- 文档更新请放入 `docs/`

---
**最后更新**: 2025年9月30日
