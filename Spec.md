# Pika积分系统需求说明 (Pika Credits System Requirements)

## 1. 新用户注册奖励 (New User Registration Bonus)

- 为新注册用户一次性发放20 Credits，永久有效
  (One-time 20 Credits reward for newly registered users, never expires)
- 用户完成注册流程后立即发放
  (Credits are distributed immediately after user completes registration)
- 通过弹窗告知用户已获得积分奖励
  (Users are notified via pop-up message about the credits reward)

## 2. 每日登录奖励 (Daily Login Bonus)

- 用户每日首次登录或注册时发放10 Credits
  (10 Credits reward for first login or registration each day)
- 每日积分在UTC+0 00:00过期
  (Daily credits expire at UTC+0 00:00)
- 判断逻辑：检查用户当日是否已领取，如已领取则不再发放
  (Logic: Check if user has already received daily credits, if yes, no additional credits will be given)
- 付费会员同样适用此规则
  (Paid members are also subject to this rule)

## 3. 产品界面修改 (UI/UX Modifications)

### 3.1 会员页面更新 (Member Page Update)
- 显示用户当前积分，区分"永久积分"和"每日积分"
  (Display current credits, distinguish between "permanent credits" and "daily credits")
- 会员页面增加"积分明细"区块
  (Add "Credits Details" section to member page)
- 增加积分获取渠道的说明文案
  (Add explanatory text about credit acquisition channels)

### 3.2 首次进入提示 (First-time User Notification)
- 新用户首次进入应用时，弹窗告知积分规则
  (Pop-up notification explaining credit rules when new users first enter the app)
- 重点说明每日登录奖励机制
  (Emphasize the daily login reward mechanism)

### 3.3 每日登录提示 (Daily Login Notification)
- 用户每日首次登录时，轻量级提示已获得当日积分奖励
  (Lightweight notification when users log in for the first time each day)
- 采用Toast或轻量级通知形式，不打断用户操作流程
  (Use Toast or lightweight notification that doesn't interrupt user workflow)

## 4. 推送通知功能 (Push Notification)

- 针对24小时未登录的用户发送推送通知
  (Send push notifications to users who haven't logged in for 24 hours)
- 提醒用户领取每日积分，提高回访率
  (Remind users to claim daily credits to increase revisit rate)
- 推送频率：最多每3天一次，避免打扰用户
  (Push frequency: Maximum once every 3 days to avoid disturbing users)
- 推送时间：用户所在时区的上午10:00-12:00之间
  (Push time: Between 10:00-12:00 AM in the user's timezone) 