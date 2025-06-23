# Pika Credits System Requirements

## 1. New User Registration Bonus

- One-time 20 Credits reward for newly registered users, never expires
- Credits are distributed immediately after user completes registration
- Users are notified via pop-up message about the credits reward

## 2. Daily Login Bonus

- 10 Credits reward for first login or registration each day
- Daily credits expire at UTC+0 00:00
- Logic: Check if user has already received daily credits, if yes, no additional credits will be given
- Paid members are also subject to this rule

## 3. UI/UX Modifications

### 3.1 Member Page Update
- Display current credits, distinguish between "permanent credits" and "daily credits"
- Add "Credits Details" section to member page
- Add explanatory text about credit acquisition channels

### 3.2 First-time User Notification
- Pop-up notification explaining credit rules when new users first enter the app
- Emphasize the daily login reward mechanism

### 3.3 Daily Login Notification
- Lightweight notification when users log in for the first time each day
- Use Toast or lightweight notification that doesn't interrupt user workflow

## 4. Push Notification

- Send push notifications to users who haven't logged in for 24 hours
- Remind users to claim daily credits to increase revisit rate
- Push frequency: Maximum once every 3 days to avoid disturbing users
- Push time: Between 10:00-12:00 AM in the user's timezone 