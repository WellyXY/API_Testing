# Vercel 部署指南

## 🚀 快速部署

### 方法一：通过 Vercel Dashboard（推荐）

1. **访问 [Vercel Dashboard](https://vercel.com/dashboard)**

2. **导入 GitHub 仓库**
   - 点击 "Add New Project" 或 "Import Project"
   - 选择 `WellyXY/seadream` 仓库
   - 如果没看到，点击 "Adjust GitHub App Permissions"

3. **配置项目**
   - **Framework Preset**: 选择 `Other`（不需要选择特定框架）
   - **Root Directory**: 保持为 `./`（根目录）
   - **Build Command**: 留空
   - **Output Directory**: 留空

4. **设置环境变量**
   - 点击 "Environment Variables"
   - 添加变量：
     - **Name**: `SEEDREAM_API_KEY`
     - **Value**: `你的 API Key`（例如：`70f23192-0f0c-47d2-9bbf-961f70a17a92`）
   - 确保选择了所有环境（Production, Preview, Development）

5. **部署**
   - 点击 "Deploy" 按钮
   - 等待 1-2 分钟完成部署
   - 部署成功后会显示访问链接

6. **访问你的应用**
   - 点击 "Visit" 或复制链接
   - 现在可以在线使用了！🎉

### 3. 通过 CLI 部署

```bash
# 登录
vercel login

# 部署
vercel

# 设置环境变量
vercel env add SEEDREAM_API_KEY

# 生产部署
vercel --prod
```

## 环境变量

需要在 Vercel Dashboard 中设置以下环境变量：

- `SEEDREAM_API_KEY`: 你的 Seedream API 密钥

## 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务器
python3 seedream_server_v2.py

# 访问
open http://localhost:8888
```

## 注意事项

1. **API Key 安全**：不要在代码中硬编码 API Key，使用环境变量
2. **文件大小限制**：Vercel Serverless Functions 有 10MB 的请求大小限制
3. **超时限制**：Serverless Functions 有执行时间限制（Hobby: 10s, Pro: 60s）

## 项目结构

```
.
├── api/
│   └── generate.py          # Vercel Serverless Function
├── scripts/                 # Shell 脚本工具
├── seedream_web_local.html  # 主页面
├── vercel.json              # Vercel 配置
├── requirements.txt         # Python 依赖
└── README.md                # 项目说明
```

## 故障排查

### 1. CORS 错误
确保 API 响应中包含了正确的 CORS 头：
```python
'Access-Control-Allow-Origin': '*'
```

### 2. 超时错误
图像生成可能需要较长时间，建议：
- 升级到 Vercel Pro 计划
- 或者使用异步处理 + Webhook 回调

### 3. 文件大小错误
如果图片太大：
- 前端压缩图片
- 调整 `max_dimension` 参数
- 降低 JPEG 质量

