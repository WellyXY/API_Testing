# SDK vs REST API 对比分析

## 你同事的代码使用 Ark SDK

```python
from byteplussdkarkruntime import Ark

client = Ark(api_key=self.ark_api_key)

args = {
    "model": "ep-20250921042133-t769x",
    "prompt": prompt,
    "response_format": "url",
    "size": "1440x2560",
    "watermark": False
}

if len(input_list) > 0:
    if len(input_list) == 1:
        args["image"] = input_list[0]
    else:
        args["image"] = input_list

# SDK 调用
imagesResponse = self.client.images.generate(**args)
```

## 我们的代码直接调用 REST API

```python
import requests

api_data = {
    "model": "ep-20250921042133-t769x",
    "prompt": prompt,
    "response_format": "url",
    "size": "1440x2560",
    "watermark": False
}

# REST API 调用
response = requests.post(
    "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    },
    json=api_data
)
```

## 主要区别

### 1. ✅ **我们现在已经一致的部分**
- ✅ 图片格式：都使用 `data:image/png;base64,...`
- ✅ 参数完全相同
- ✅ 同样的 model、size、watermark 设置

### 2. ⚠️ **SDK 可能的额外处理**

SDK 通常会做这些事情（但不一定影响结果）：

#### a) **请求重试机制**
```python
# SDK 可能内置
- 自动重试失败的请求
- 指数退避策略
- 超时处理
```

#### b) **参数验证**
```python
# SDK 可能会验证
- 模型 ID 格式
- 图片大小限制
- Base64 格式检查
```

#### c) **请求头优化**
```python
# SDK 可能添加额外的头
- User-Agent: byteplussdkarkruntime/x.x.x
- SDK-Version
- Request-Id
```

#### d) **错误处理**
```python
# SDK 可能提供更友好的错误
- 自定义异常类型
- 详细的错误信息
```

### 3. 🎯 **对图片质量的影响：理论上没有！**

**关键结论：**
- SDK 和 REST API 最终都是发送 HTTP POST 请求到同一个端点
- **只要参数相同、图片格式相同，结果应该一致**
- SDK 主要是方便性和健壮性的提升，不会改变图片生成算法

### 4. 🔍 **导致畸变的真正原因**

不是 SDK vs REST API 的问题，而是：

#### ❌ **之前的问题**
```javascript
// 浏览器直接读取文件
const reader = new FileReader();
reader.readAsDataURL(file);  // 可能是 JPEG、PNG、WEBP...

// 直接传给 API，格式不统一
data.image = reader.result;  // data:image/jpeg;base64,... 或其他
```

#### ✅ **现在的解决方案**
```python
# 服务器端统一处理
pil_image = base64_to_pil(image_data)  # 任何格式
png_base64 = pil_to_base64_png(pil_image)  # 统一转为 PNG

# 确保格式一致
return "data:image/png;base64,{base64_string}"
```

## 测试建议

### 用同样的参考图片测试：

1. **之前的方法**（直接传文件 base64）
   - 如果是 JPEG → 可能有压缩损失
   - 如果是 WEBP → 可能有兼容性问题
   - 结果：**畸变**

2. **现在的方法**（统一转 PNG）
   - 统一格式
   - RGB 颜色模式
   - 结果：**应该改善**

3. **如果还是有畸变**
   - 可能是 API 本身的特性
   - 可以尝试调整 prompt
   - 可以尝试不同的 size 参数

## 总结

| 方面 | SDK | REST API（我们的V2） | 影响 |
|------|-----|---------------------|------|
| 便捷性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 开发体验 |
| 灵活性 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 自定义能力 |
| 依赖 | 需要安装 SDK | 仅需 requests | 部署复杂度 |
| **图片质量** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **相同！** |
| 错误处理 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 健壮性 |
| 调试 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 可见性 |

**结论：图片格式统一后，SDK vs REST API 对生成质量没有影响！**


