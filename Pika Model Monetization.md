# Pika 模型收费策略 - 产品需求文档
# Pika Model Monetization Strategy - Product Requirements Document

## 背景介绍 (Background)

在对比市场上的AI视频生成产品后，我们发现当前的收费策略可能无法最大化用户体验和商业价值。大多数竞品（如Kling、Runway、PixVerse、Hailuo等）采用不同的收费模式，主要集中在分辨率、无水印、生成速度等方面，而非功能或模型本身的限制。

After comparing AI video generation products in the market, we found that our current monetization strategy may not maximize user experience and business value. Most competitors (such as Kling, Runway, PixVerse, Hailuo, etc.) adopt different pricing models, focusing on resolution, watermark removal, generation speed, etc., rather than restricting features or models themselves.

## 问题分析 (Problem Analysis)

### 当前收费策略的不足 (Limitations of Current Strategy)

1. **功能收费限制**：目前我们对特定功能（如Pikascenes, Pikadditions等）设置了收费墙，这可能阻碍了用户探索和体验完整产品价值。
2. **模型访问限制**：将高级模型（如Turbo, 2.1, 2.2）设为付费专属，降低了产品对新用户的吸引力。
3. **付费功能不够完善**：缺少一些竞品已有的付费价值点，如批量生成、多输出等。

1. **Feature Paywall**: Currently, we charge for specific features (like Pikascenes, Pikadditions, etc.), which may prevent users from exploring and experiencing the full product value.
2. **Model Access Restrictions**: Making advanced models (such as Turbo, 2.1, 2.2) paid-only reduces the product's attractiveness to new users.
3. **Incomplete Premium Features**: Missing some paid value points that competitors already offer, such as batch generation, multiple outputs, etc.

## 策略目标 (Strategy Objectives)

1. 提高用户转化率和留存率
2. 增加付费用户数量和ARPU值
3. 保持产品竞争力并提升用户满意度

1. Increase user conversion and retention rates
2. Increase number of paying users and ARPU value
3. Maintain product competitiveness and improve user satisfaction

## 新收费策略提案 (New Monetization Strategy Proposal)

### 1. 功能免费化 (Free Features)

所有核心功能对所有用户开放，包括：
- Pikascenes（场景生成）
- Pikadditions（添加元素）
- Pikaswaps（替换元素）
- Pikatwists（特效）
- Pikaframes（帧控制）

All core features open to all users, including:
- Pikascenes (scene generation)
- Pikadditions (element addition)
- Pikaswaps (element replacement)
- Pikatwists (effects)
- Pikaframes (frame control)

### 2. 模型开放策略 (Model Access Strategy)

#### 基础模型开放 (Basic Models)
基础模型完全免费使用：
- 1.5（完全免费）

Basic models completely free to use:
- 1.5 (completely free)

#### 高级模型有限试用 (Advanced Models Limited Trial)
高级模型提供有限免费试用：
- Turbo（每个功能可免费使用3次）
- 2.1（每个功能可免费使用3次）
- 2.2（每个功能可免费使用3次）
- Pro系列（每个功能可免费使用3次）

Advanced models with limited free trial:
- Turbo (3 free uses per feature)
- 2.1 (3 free uses per feature)
- 2.2 (3 free uses per feature)
- Pro series (3 free uses per feature)

### 3. 积分系统保持不变 (Credits System Remains Unchanged)

维持当前的积分配置和消耗方式：
- 保持现有各模型和功能的积分消耗设计
- 保持现有会员等级的积分分配方案
- 保持积分购买和使用的现有规则

Maintain the current credit configuration and consumption method:
- Keep existing credit consumption design for various models and features
- Maintain credit allocation plans for existing membership levels
- Keep existing rules for credit purchase and usage

### 4. 付费价值点 (Paid Value Points)

#### 免费用户限制 (Free User Limitations)
- 低分辨率输出（360p）
- 包含水印
- 生成速度较慢（低优先级队列）
- 高级模型每个功能限制3次免费使用
- 每日积分限制（80点）

- Low resolution output (360p)
- Watermarked content
- Slower generation speed (low priority queue)
- Advanced models limited to 3 free uses per feature
- Daily credit limit (80 points)

#### 付费用户权益 (Paid User Benefits)
- **无使用次数限制**：无限制使用所有模型和功能
- **分辨率提升**：最高1080p/4K输出
- **无水印**：下载无品牌标记的视频
- **优先生成**：高优先级队列，更快速获得结果
- **更多积分**：更高的每月生成配额

- **No Usage Limits**: Unlimited use of all models and features
- **Resolution Upgrade**: Up to 1080p/4K output
- **No Watermark**: Download videos without brand marks
- **Priority Generation**: High-priority queue for faster results
- **More Credits**: Higher monthly generation quota

## 会员等级设计 (Membership Tier Design)

### 免费会员 (Free Tier)
- 所有功能的基础访问权限
- 高级模型每个功能限制3次免费使用
- 360p视频输出
- 包含Pika水印
- 每日积分限制：80点
- 标准生成队列

- Basic access to all features
- Advanced models limited to 3 free uses per feature
- 360p video output
- Includes Pika watermark
- Daily credit limit: 80 points
- Standard generation queue

### 标准会员 (Standard Tier) - $8/月
- 所有功能和模型的完整访问权限（无使用次数限制）
- 720p视频输出
- 无水印视频
- 每月积分：700点
- 优先生成队列

- Full access to all features and models (no usage limits)
- 720p video output
- Watermark-free videos
- Monthly credits: 700 points
- Priority generation queue

### 专业会员 (Pro Tier) - $28/月
- 所有功能和模型的完整访问权限（无使用次数限制）
- 1080p视频输出
- 无水印视频
- 每月积分：2300点
- 高优先级生成队列

- Full access to all features and models (no usage limits)
- 1080p video output
- Watermark-free videos
- Monthly credits: 2300 points
- High-priority generation queue

### 至尊会员 (Premium Tier) - $76/月
- 所有功能和模型的完整访问权限（无使用次数限制）
- 4K视频输出（支持的模型）
- 无水印视频
- 每月积分：6000点
- 最高优先级生成队列
- 优先客户支持

- Full access to all features and models (no usage limits)
- 4K video output (for supported models)
- Watermark-free videos
- Monthly credits: 6000 points
- Highest priority generation queue
- Priority customer support

## 实施路线图 (Implementation Roadmap)

### 第一阶段：准备工作 (Phase 1: Preparation)
- 开发模型试用次数限制功能
- 设计新的UI流程和提示
- 更新计费系统

- Develop model trial usage limit functionality
- Design new UI flows and prompts
- Update billing system

### 第二阶段：内部测试 (Phase 2: Internal Testing)
- 进行A/B测试评估免费试用次数的效果
- 收集和分析用户反馈
- 优化具体参数（试用次数、限制方式等）

- Conduct A/B testing to evaluate the effectiveness of free trial counts
- Collect and analyze user feedback
- Optimize specific parameters (trial count, limitation methods, etc.)

### 第三阶段：正式推出 (Phase 3: Official Launch)
- 向现有用户宣传新的收费策略
- 为现有付费用户提供过渡方案
- 启动营销活动推广新的价值主张

- Announce new pricing strategy to existing users
- Provide transition plan for existing paying users
- Launch marketing campaigns to promote new value propositions

## 衡量指标 (Metrics)

1. **试用转化率**：试用高级模型后转为付费用户的比例
2. **ARPU**：每用户平均收入
3. **留存率**：不同会员等级的留存率比较
4. **模型使用量**：各模型使用频率及试用后的持续使用情况
5. **用户满意度**：NPS和客户反馈指标

1. **Trial Conversion Rate**: Proportion of users converting to paid after trying advanced models
2. **ARPU**: Average Revenue Per User
3. **Retention Rate**: Retention rates comparison across different membership tiers
4. **Model Usage**: Frequency of model usage and continued use after trial
5. **User Satisfaction**: NPS and customer feedback metrics

## 潜在风险和缓解措施 (Potential Risks and Mitigation)

### 风险 (Risks)
1. 3次免费试用可能不足以展示模型价值
2. 用户可能创建多个账号规避使用限制
3. 现有付费用户可能对变化不满
4. 收入可能短期下降

1. 3 free trials may not be enough to demonstrate model value
2. Users may create multiple accounts to circumvent usage restrictions
3. Existing paying users may be dissatisfied with changes
4. Potential short-term revenue decline

### 缓解措施 (Mitigation)
1. 基于数据调整试用次数，确保用户体验最佳价值
2. 实施账号验证机制和IP限制
3. 为现有付费用户提供额外福利或折扣
4. 通过提高转化率和留存率抵消短期收入下降

1. Adjust trial count based on data to ensure users experience optimal value
2. Implement account verification mechanisms and IP restrictions
3. Provide additional benefits or discounts to existing paying users
4. Offset short-term revenue declines through improved conversion and retention rates

## 结论 (Conclusion)

通过重构收费策略，开放所有功能并提供高级模型的有限试用，我们希望能够提高用户体验和付费转化率。维持现有的积分系统同时将重点从"功能/模型完全收费"转向"高级模型有限试用+使用价值收费"，这一策略更好地平衡了用户体验与商业可持续性，有望在竞争激烈的AI视频生成市场中保持优势地位。

By restructuring our pricing strategy, opening all features, and providing limited trials of advanced models, we aim to improve user experience and paid conversion rates. Maintaining the existing credit system while shifting focus from "complete feature/model charging" to "limited trial of advanced models + usage value charging" better balances user experience with business sustainability, promising to maintain a competitive position in the fierce AI video generation market. 