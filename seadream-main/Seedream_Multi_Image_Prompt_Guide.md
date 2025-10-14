# Seedream 多图参考 Prompt 指南

## 🎯 目标：图1的角色 + 图2的动作

### 📋 基本原则

当使用多张参考图片时，Seedream 会**自动融合**所有图片的特征。关键是通过 **Prompt 明确指示**哪些元素来自哪张图。

---

## 🎨 Prompt 撰写策略

### ✅ **方法 1: 明确指示（推荐）**

```
Use the character/person from the first reference image, 
but replicate the pose/action from the second reference image.
[Your detailed scene description here]
```

**中文版本：**
```
参考第一张图片中的角色/人物特征，
但模仿第二张图片中的姿势/动作。
[你的详细场景描述]
```

### ✅ **方法 2: 详细描述法**

```
A [character description from image 1], 
performing [action/pose from image 2],
in [scene/environment],
[style, lighting, mood details]
```

**示例：**
```
A young woman with long black hair and elegant features (from reference 1),
sitting in a yoga meditation pose with crossed legs and hands in prayer position (from reference 2),
in a modern minimalist studio with soft natural lighting,
photorealistic style, serene atmosphere, 8K quality
```

---

## 📝 实际应用示例

### 场景 1: 角色换动作

**参考图片：**
- 图1: 一个穿红色裙子的女性站立照
- 图2: 一个人做瑜伽动作

**Prompt：**
```
The woman in the red dress from the first image, 
performing the yoga tree pose shown in the second image,
in a bright yoga studio with wooden floors,
natural lighting, peaceful atmosphere, high resolution
```

**中文：**
```
第一张图片中穿红裙子的女性，
做出第二张图片中展示的瑜伽树式动作，
在明亮的瑜伽工作室，木地板，
自然光线，宁静氛围，高分辨率
```

---

### 场景 2: 保持角色，改变姿势和场景

**参考图片：**
- 图1: 特定角色的脸部和身材特征
- 图2: 优雅的舞蹈姿势

**Prompt：**
```
Take the facial features and body type from reference image 1,
apply the graceful dance pose from reference image 2,
place the character in an elegant ballroom with chandelier lighting,
cinematic photography, 1440x2560, dramatic lighting
```

---

### 场景 3: 多图融合（3+ 张图）

**参考图片：**
- 图1: 角色A的脸部特征
- 图2: 想要的动作姿势
- 图3: 服装风格参考
- 图4: 场景环境参考

**Prompt：**
```
Character with facial features from image 1,
wearing the outfit style shown in image 3,
performing the pose from image 2,
in the environment setting of image 4,
photorealistic, high detail, professional photography
```

---

## 💡 高级技巧

### 1. **权重控制（通过描述详细度）**

如果想让某张图的影响更强：
```
PRIMARILY use the character from image 1 (detailed description),
subtly incorporate the pose from image 2
```

### 2. **特征拆分描述**

```
Character appearance (face, hair, body type): from reference image 1
Body pose and hand position: from reference image 2
Clothing and accessories: keep minimalist
Environment: plain white background
```

### 3. **避免冲突的关键词**

❌ 不好的 Prompt：
```
Beautiful woman dancing  (没有指明参考哪张图)
```

✅ 好的 Prompt：
```
The specific woman shown in reference 1, performing the dance move from reference 2
```

---

## 🎭 针对你的需求

### 如果你想："图1的角色做图2的动作"

**英文模板：**
```
The [describe character basics] from reference image 1,
replicating the exact [pose/action description] shown in reference image 2,
[add environment, style, lighting details],
maintain character's distinctive features, high quality, detailed
```

**中文模板：**
```
参考图1中的[角色基本描述]，
完全模仿图2中展示的[姿势/动作描述]，
[环境、风格、光线细节]，
保持角色的显著特征，高质量，细节丰富
```

**具体示例：**
```
The elegant woman with shoulder-length brown hair from the first reference image,
performing the seated meditation pose with crossed legs from the second reference image,
in a serene zen garden with soft morning light,
keep her facial features and body proportions consistent,
photorealistic, 1440x2560, professional photography
```

---

## 🔧 在我们的界面中使用

### 步骤：

1. **上传图片顺序很重要**
   - 第一张上传 → 图1（角色来源）
   - 第二张上传 → 图2（动作来源）

2. **在 Prompt 框中输入**
   ```
   The person from the first reference image,
   performing the pose shown in the second reference image,
   [你的场景描述]
   ```

3. **选择合适的分辨率**
   - 1440x2560（竖屏高清）- 适合人物全身照
   - 2560x1440（横屏高清）- 适合横向构图

4. **提交任务并观察结果**

---

## ⚠️ 常见问题

### Q1: 为什么生成的图不像图1的角色？

**可能原因：**
- Prompt 中没有明确指出"第一张图"
- 图1的角色特征不够明显
- 多张图的风格差异太大

**解决方案：**
- 在 Prompt 中详细描述图1角色的特征
- 使用 "maintain facial features from image 1"
- 确保参考图片质量高

### Q2: 为什么动作不像图2？

**可能原因：**
- Prompt 中动作描述不够具体
- 图2的姿势不够清晰

**解决方案：**
- 详细描述姿势："crossed legs, hands in prayer position, back straight"
- 使用 "exact pose from image 2"

### Q3: 可以用几张参考图？

- **单图**：角色一致性 i2i
- **2-3张**：效果最好，角色+动作组合
- **4-6张**：可以融合更多元素，但可能混乱
- **建议**：2-3张图 + 清晰的 Prompt

---

## 📚 实战 Prompt 模板库

### 模板 1: 角色动作转移
```
The [gender] with [distinctive features] from reference 1,
adopting the [specific pose] from reference 2,
[environment], [style], [lighting]
```

### 模板 2: 保持角色换场景动作
```
Character from image 1 maintaining their appearance,
in the pose shown in image 2,
background and setting: [detailed description],
keep character recognizable, [quality keywords]
```

### 模板 3: 精确特征控制
```
Person with: face from ref 1, pose from ref 2,
clothing: [describe],
location: [describe],
style: photorealistic, lighting: [describe]
```

---

## 🎯 最佳实践总结

1. ✅ **明确指示**图片顺序和用途
2. ✅ **详细描述**想要保留的特征
3. ✅ **使用关键词**："from image 1", "pose from image 2"
4. ✅ **保持一致**的风格描述
5. ✅ **高质量**参考图片（清晰、光线好）
6. ✅ **多次尝试**并调整 Prompt

---

## 🔗 相关资源

- Seedream 4.0 官方文档
- 我们的 Web 界面：`http://localhost:8080`
- 本地服务器支持多图上传和实时预览

试试看，有问题随时调整 Prompt！🎨


