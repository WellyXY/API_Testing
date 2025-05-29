const express = require('express');
const cors = require('cors');
const googleTrends = require('google-trends-api');
const https = require('https');

const app = express();
const PORT = 3001;

// 配置更長時間的超時時間
const agent = new https.Agent({
  timeout: 30000, // 30秒
  keepAlive: true
});

// 啟用 CORS
app.use(cors());

// 解析JSON請求體
app.use(express.json());

// 全域錯誤處理
app.use((err, req, res, next) => {
  console.error('全域錯誤:', err);
  res.status(500).json({ 
    error: '服務器錯誤', 
    message: err.message 
  });
});

// 獲取過去7天的趨勢數據
app.get('/api/trends', async (req, res) => {
  try {
    const keyword = req.query.keyword || 'PixVerse';
    console.log(`正在獲取關鍵詞 "${keyword}" 的趨勢數據...`);
    
    // 獲取過去7天的數據
    const dateNow = new Date();
    const date7DaysAgo = new Date(dateNow.getTime() - (7 * 24 * 60 * 60 * 1000));
    
    console.log(`時間範圍: ${date7DaysAgo.toISOString()} 到 ${dateNow.toISOString()}`);
    
    // 添加超時處理
    const timeoutPromise = new Promise((_, reject) => {
      setTimeout(() => reject(new Error('趨勢數據請求超時')), 25000);
    });
    
    // 實際API請求
    const apiPromise = googleTrends.interestOverTime({
      keyword: keyword,
      startTime: date7DaysAgo,
      endTime: dateNow,
      granularTimeResolution: true,
      hl: 'zh-CN' // 設置語言為中文
    });
    
    // 使用Promise.race來實現超時處理
    const results = await Promise.race([apiPromise, timeoutPromise]);
    
    const data = JSON.parse(results);
    console.log('趨勢數據獲取成功');
    
    res.json(data);
  } catch (error) {
    console.error('趨勢數據獲取錯誤:', error.toString());
    res.status(503).json({ 
      error: '獲取Google趨勢數據時出錯', 
      message: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// 獲取相關熱門搜索關鍵詞
app.get('/api/related-queries', async (req, res) => {
  try {
    const keyword = req.query.keyword || 'PixVerse';
    console.log(`正在獲取關鍵詞 "${keyword}" 的相關查詢...`);
    
    // 添加超時處理
    const timeoutPromise = new Promise((_, reject) => {
      setTimeout(() => reject(new Error('相關查詢請求超時')), 25000);
    });
    
    // 實際API請求
    const apiPromise = googleTrends.relatedQueries({
      keyword: keyword,
      geo: '',
      hl: 'zh-CN' // 設置語言為中文
    });
    
    // 使用Promise.race來實現超時處理
    const results = await Promise.race([apiPromise, timeoutPromise]);
    
    const data = JSON.parse(results);
    console.log('相關查詢獲取成功');
    
    res.json(data);
  } catch (error) {
    console.error('相關查詢獲取錯誤:', error.toString());
    res.status(503).json({ 
      error: '獲取相關查詢時出錯', 
      message: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// 獲取國家排名數據
app.get('/api/countries', async (req, res) => {
  try {
    const keyword = req.query.keyword || 'PixVerse';
    console.log(`正在獲取關鍵詞 "${keyword}" 的國家數據...`);
    
    // 添加超時處理
    const timeoutPromise = new Promise((_, reject) => {
      setTimeout(() => reject(new Error('國家數據請求超時')), 25000);
    });
    
    // 實際API請求
    const apiPromise = googleTrends.interestByRegion({
      keyword: keyword,
      resolution: 'COUNTRY',
      geo: '',
      hl: 'zh-CN' // 設置語言為中文
    });
    
    // 使用Promise.race來實現超時處理
    const results = await Promise.race([apiPromise, timeoutPromise]);
    
    const data = JSON.parse(results);
    console.log('國家數據獲取成功');
    
    res.json(data);
  } catch (error) {
    console.error('國家數據獲取錯誤:', error.toString());
    res.status(503).json({ 
      error: '獲取國家數據時出錯', 
      message: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// 健康檢查端點
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    timestamp: new Date().toISOString(),
    version: '1.0.0'
  });
});

// 啟動服務器
app.listen(PORT, () => {
  console.log(`服務器運行在 http://localhost:${PORT}`);
  console.log('提示：如果出現查詢失敗，可能是Google API限制或網絡問題');
}); 