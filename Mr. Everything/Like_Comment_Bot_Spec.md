# Like / Comment Bot 技術規格文檔
# Like / Comment Bot Technical Specification

## 🇹🇼 中文版本

### 1. 概述
本規格文檔定義了一個自動化的點讚和評論機器人系統，用於在用戶發佈內容後自動進行互動。

### 2. 功能需求

#### 2.1 核心功能
- **自動點讚**：當用戶發佈新內容時，系統自動派發 Bot 進行點讚
- **自動評論**：系統自動生成並發佈相關評論
- **智能分配**：根據用戶活躍度和內容質量智能分配 Bot 互動

#### 2.2 限制條件
- 每個用戶每日最多獲得 1,000 次 Bot 互動（點讚 + 評論）
- Bot 互動需要模擬真實用戶行為，避免被檢測
- 支援多種內容類型（文字、圖片、視頻）

### 3. 技術架構

#### 3.1 系統組件
- **內容監聽器**：監聽新發佈的內容
- **Bot 管理器**：管理 Bot 帳號池
- **互動引擎**：執行點讚和評論邏輯
- **限制管理器**：追蹤用戶互動配額
- **評論生成器**：生成合適的評論內容

#### 3.2 數據結構

```json
{
  "user": {
    "id": "string",
    "username": "string",
    "daily_engagement_count": "number",
    "daily_limit": 1000,
    "last_reset": "timestamp"
  },
  "content": {
    "id": "string",
    "user_id": "string",
    "type": "text|image|video",
    "content": "string",
    "timestamp": "timestamp",
    "engagement_received": "number"
  },
  "bot_engagement": {
    "id": "string",
    "bot_id": "string",
    "content_id": "string",
    "user_id": "string",
    "type": "like|comment",
    "timestamp": "timestamp",
    "comment_text": "string (optional)"
  }
}
```

### 4. 業務邏輯

#### 4.1 觸發機制
1. 用戶發佈新內容
2. 系統檢查該用戶當日剩餘互動配額
3. 如果配額充足，觸發 Bot 互動流程

#### 4.2 互動分配策略
- **即時互動**：內容發佈後 1-5 分鐘內進行點讚
- **延遲評論**：內容發佈後 10-30 分鐘內進行評論
- **隨機化**：所有時間間隔都有隨機變化，避免被檢測

#### 4.3 評論生成規則
- 基於內容關鍵詞生成相關評論
- 評論庫包含多種情感色彩（正面、中性、鼓勵）
- 避免重複評論，每個內容最多 3 個 Bot 評論

### 5. API 設計

#### 5.1 內容監聽 API
```
POST /api/v1/content/published
{
  "user_id": "string",
  "content_id": "string",
  "content_type": "string",
  "content": "string"
}
```

#### 5.2 查詢用戶配額 API
```
GET /api/v1/user/{user_id}/engagement-quota
Response: {
  "daily_limit": 1000,
  "used_today": 250,
  "remaining": 750,
  "reset_time": "2024-01-01T00:00:00Z"
}
```

#### 5.3 手動觸發 Bot 互動 API
```
POST /api/v1/bot/engage
{
  "content_id": "string",
  "engagement_types": ["like", "comment"],
  "priority": "high|normal|low"
}
```

### 6. 安全與合規

#### 6.1 檢測避免
- 使用多個 Bot 帳號輪換
- 模擬真實用戶的行為模式
- 隨機化互動時間和頻率

#### 6.2 數據保護
- 所有用戶數據加密存儲
- 定期清理過期的互動記錄
- 遵循相關隱私法規

### 7. 監控與分析

#### 7.1 關鍵指標
- 每日總互動次數
- 用戶滿意度評分
- Bot 檢測率
- 系統響應時間

#### 7.2 報告功能
- 用戶互動統計報告
- Bot 性能分析報告
- 異常檢測報告

---

## 🇺🇸 English Version

### 1. Overview
This specification defines an automated like and comment bot system that automatically engages with user content after publication.

### 2. Functional Requirements

#### 2.1 Core Features
- **Auto-Like**: Automatically deploy bots to like new user content
- **Auto-Comment**: Automatically generate and post relevant comments
- **Smart Allocation**: Intelligently allocate bot interactions based on user activity and content quality

#### 2.2 Constraints
- Maximum 1,000 bot interactions per user per day (likes + comments)
- Bot interactions must simulate real user behavior to avoid detection
- Support for multiple content types (text, images, videos)

### 3. Technical Architecture

#### 3.1 System Components
- **Content Listener**: Monitors newly published content
- **Bot Manager**: Manages bot account pool
- **Engagement Engine**: Executes like and comment logic
- **Quota Manager**: Tracks user interaction quotas
- **Comment Generator**: Generates appropriate comment content

#### 3.2 Data Structure

```json
{
  "user": {
    "id": "string",
    "username": "string",
    "daily_engagement_count": "number",
    "daily_limit": 1000,
    "last_reset": "timestamp"
  },
  "content": {
    "id": "string",
    "user_id": "string",
    "type": "text|image|video",
    "content": "string",
    "timestamp": "timestamp",
    "engagement_received": "number"
  },
  "bot_engagement": {
    "id": "string",
    "bot_id": "string",
    "content_id": "string",
    "user_id": "string",
    "type": "like|comment",
    "timestamp": "timestamp",
    "comment_text": "string (optional)"
  }
}
```

### 4. Business Logic

#### 4.1 Trigger Mechanism
1. User publishes new content
2. System checks user's remaining daily interaction quota
3. If quota is sufficient, trigger bot interaction process

#### 4.2 Interaction Allocation Strategy
- **Immediate Interaction**: Like content within 1-5 minutes after publication
- **Delayed Comments**: Comment on content within 10-30 minutes after publication
- **Randomization**: All time intervals have random variations to avoid detection

#### 4.3 Comment Generation Rules
- Generate relevant comments based on content keywords
- Comment library includes various emotional tones (positive, neutral, encouraging)
- Avoid duplicate comments, maximum 3 bot comments per content

### 5. API Design

#### 5.1 Content Listener API
```
POST /api/v1/content/published
{
  "user_id": "string",
  "content_id": "string",
  "content_type": "string",
  "content": "string"
}
```

#### 5.2 User Quota Query API
```
GET /api/v1/user/{user_id}/engagement-quota
Response: {
  "daily_limit": 1000,
  "used_today": 250,
  "remaining": 750,
  "reset_time": "2024-01-01T00:00:00Z"
}
```

#### 5.3 Manual Bot Engagement API
```
POST /api/v1/bot/engage
{
  "content_id": "string",
  "engagement_types": ["like", "comment"],
  "priority": "high|normal|low"
}
```

### 6. Security & Compliance

#### 6.1 Detection Avoidance
- Use multiple bot accounts in rotation
- Simulate real user behavior patterns
- Randomize interaction timing and frequency

#### 6.2 Data Protection
- Encrypt all user data in storage
- Regularly clean expired interaction records
- Comply with relevant privacy regulations

### 7. Monitoring & Analytics

#### 7.1 Key Metrics
- Daily total interactions
- User satisfaction scores
- Bot detection rate
- System response time

#### 7.2 Reporting Features
- User interaction statistics reports
- Bot performance analysis reports
- Anomaly detection reports

---

## 實施時間線 / Implementation Timeline

### Phase 1: 基礎建設 / Foundation (Week 1-2)
- 設置基本架構 / Set up basic architecture
- 建立數據庫模型 / Create database models
- 實現基本 API / Implement basic APIs

### Phase 2: 核心功能 / Core Features (Week 3-4)
- 實現自動點讚功能 / Implement auto-like functionality
- 實現評論生成器 / Implement comment generator
- 建立配額管理系統 / Build quota management system

### Phase 3: 優化與測試 / Optimization & Testing (Week 5-6)
- 性能優化 / Performance optimization
- 安全測試 / Security testing
- 用戶驗收測試 / User acceptance testing

### Phase 4: 部署與監控 / Deployment & Monitoring (Week 7-8)
- 生產環境部署 / Production deployment
- 監控系統設置 / Monitoring system setup
- 文檔整理 / Documentation finalization 