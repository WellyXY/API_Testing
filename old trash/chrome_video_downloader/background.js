// 监听下载请求
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === "downloadVideo") {
    // 确保文件夹名称有效
    let filename = request.filename;
    if (!filename) {
      filename = `VideoDownloads/video_${Date.now()}.mp4`;
    }
    
    chrome.downloads.download({
      url: request.url,
      filename: filename,
      saveAs: request.saveAs === undefined ? false : request.saveAs // 默认不显示保存对话框
    }, function(downloadId) {
      if (chrome.runtime.lastError) {
        console.error("下载错误:", chrome.runtime.lastError);
        if (sendResponse) {
          sendResponse({success: false, error: chrome.runtime.lastError.message});
        }
      } else {
        if (sendResponse) {
          sendResponse({success: true, downloadId: downloadId});
        }
      }
    });
    
    // 如果有反馈请求，发送成功消息
    if (sendResponse) {
      return true; // 保持消息通道打开，等待异步响应
    }
  } else if (request.action === "batchDownload") {
    // 批量下载视频
    const videos = request.videos;
    let successCount = 0;
    let errorCount = 0;
    
    if (videos && videos.length > 0) {
      videos.forEach((video, index) => {
        // 确保文件夹名称有效
        let filename = video.filename;
        if (!filename) {
          filename = `VideoDownloads/video_${Date.now()}_${index}.mp4`;
        }
        
        // 延迟每个下载以避免浏览器阻止过多同时下载
        setTimeout(() => {
          chrome.downloads.download({
            url: video.url,
            filename: filename,
            saveAs: false // 批量下载不显示保存对话框
          }, function(downloadId) {
            if (chrome.runtime.lastError) {
              console.error("下载错误:", chrome.runtime.lastError);
              errorCount++;
            } else {
              successCount++;
            }
            
            // 当所有下载都处理完毕后发送响应
            if (successCount + errorCount === videos.length) {
              if (sendResponse) {
                sendResponse({
                  success: true,
                  count: videos.length,
                  successCount: successCount,
                  errorCount: errorCount
                });
              }
            }
          });
        }, index * 300); // 每个下载间隔300毫秒
      });
      
      return true; // 保持消息通道打开，等待异步响应
    }
    
    if (sendResponse) {
      sendResponse({success: true, count: videos.length});
      return true;
    }
  }
  return true;
});

// 安装扩展时的处理
chrome.runtime.onInstalled.addListener(function(details) {
  if (details.reason === "install") {
    // 初始化设置
    chrome.storage.sync.set({
      lastFolderName: 'VideoDownloads',
      autoDownloadAll: false,
      showSaveDialog: false
    });
    
    // 打开欢迎页面或设置页面
    chrome.tabs.create({
      url: "https://github.com/your-username/chrome-video-downloader"
    });
  }
}); 