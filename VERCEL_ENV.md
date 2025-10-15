# Vercel 环境变量配置

## 配置 Vertex AI 认证（必需）

要在 Vercel 部署的应用中使用 Sticking Video 功能，必须配置 `VERTEX_AI_JSON` 环境变量。

### 步骤

1. 登录 [Vercel Dashboard](https://vercel.com/dashboard)
2. 选择你的项目
3. 进入 **Settings** → **Environment Variables**
4. 添加新的环境变量：
   - **Name**: `VERTEX_AI_JSON`
   - **Value**: 将本地 `vertex-ai.json` 文件的完整内容复制粘贴进去（整个 JSON 对象）
   - **Environment**: 勾选 `Production`, `Preview`, `Development`

5. 点击 **Save**
6. 重新部署应用（在 Deployments 页面点击 Redeploy）

### 获取 vertex-ai.json 内容

```bash
cat vertex-ai.json
```

复制输出的完整 JSON 内容到 Vercel 环境变量。

### 本地开发

本地开发时，代码会自动使用项目根目录下的 `vertex-ai.json` 文件，无需配置环境变量。

### 认证优先级

1. **环境变量 `VERTEX_AI_JSON`**（Vercel 线上环境）
2. **本地文件 `./vertex-ai.json`**（本地开发）
3. **集群文件** `/mnt/nfs/chenlin/dataproc/vertex-ai.json`（服务器）

### 故障排除

如果遇到 "找不到认证文件" 错误：

1. **检查环境变量是否设置**
   - 在 Vercel 项目设置中确认 `VERTEX_AI_JSON` 已添加
   - 确认变量值是完整的 JSON 对象（以 `{` 开头，`}` 结尾）

2. **验证 JSON 格式**
   - 不要有额外的引号包裹整个 JSON
   - 保持原始的换行和缩进（或者压缩成一行也可以）

3. **重新部署**
   - 添加或修改环境变量后必须重新部署才能生效
   - 在 Deployments 页面找到最新部署，点击右侧的 "..." → "Redeploy"

4. **查看部署日志**
   - 在部署日志中查找认证相关的输出
   - 应该看到 "✅ 使用环境变量认证 (VERTEX_AI_JSON)"

### 安全说明

⚠️ **vertex-ai.json 不能提交到 Git！**

- 该文件包含敏感的 Google Cloud 服务账号密钥
- GitHub 会自动阻止包含密钥的推送
- 始终使用环境变量在线上环境中配置

