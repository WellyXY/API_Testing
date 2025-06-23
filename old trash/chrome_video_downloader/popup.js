document.addEventListener('DOMContentLoaded', function() {
  const scanBtn = document.getElementById('scanBtn');
  const videoList = document.getElementById('videoList');
  const noVideos = document.getElementById('noVideos');
  const loading = document.getElementById('loading');
  const downloadAll = document.getElementById('downloadAll');
  const downloadInfo = document.getElementById('downloadInfo');
  const downloadOptions = document.getElementById('downloadOptions');
  const folderNameInput = document.getElementById('folderName');
  
  let videos = [];
  let settings = {
    showSaveDialog: false,
    lastFolderName: 'VideoDownloads'
  };
  
  // 加载设置
  chrome.storage.sync.get(['showSaveDialog', 'lastFolderName'], function(result) {
    if (result.showSaveDialog !== undefined) {
      settings.showSaveDialog = result.showSaveDialog;
    }
    if (result.lastFolderName) {
      settings.lastFolderName = result.lastFolderName;
      folderNameInput.value = result.lastFolderName;
    }
  });
  
  // 保存文件夹设置
  folderNameInput.addEventListener('input', function() {
    const folderName = folderNameInput.value.trim();
    if (folderName) {
      chrome.storage.sync.set({ 'lastFolderName': folderName });
      settings.lastFolderName = folderName;
    }
  });
  
  // 扫描按钮点击事件
  scanBtn.addEventListener('click', function() {
    loading.style.display = 'block';
    videoList.innerHTML = '';
    noVideos.style.display = 'none';
    downloadAll.style.display = 'none';
    downloadInfo.style.display = 'none';
    downloadOptions.style.display = 'none';
    
    // 向当前激活的标签页注入内容脚本
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      chrome.tabs.sendMessage(tabs[0].id, {action: "scanVideos"}, function(response) {
        loading.style.display = 'none';
        
        if (response && response.videos && response.videos.length > 0) {
          videos = response.videos;
          displayVideos(videos);
          downloadAll.style.display = 'block';
          downloadInfo.style.display = 'block';
          downloadOptions.style.display = 'block';
        } else {
          noVideos.style.display = 'block';
        }
      });
    });
  });
  
  // 下载所有按钮点击事件
  downloadAll.addEventListener('click', function() {
    // 获取自定义文件夹名称
    const folderName = folderNameInput.value.trim() || 'VideoDownloads';
    
    // 保存最后使用的文件夹名称
    chrome.storage.sync.set({ 'lastFolderName': folderName });
    
    // 准备批量下载数据
    const downloadVideos = videos.map(video => {
      const filename = sanitizeFilename(video.title || 'video_' + Date.now());
      const extension = getFileExtension(video.url, video.type);
      return {
        url: video.url,
        filename: `${folderName}/${filename}${extension}`
      };
    });
    
    // 使用批量下载API
    chrome.runtime.sendMessage({
      action: "batchDownload",
      videos: downloadVideos
    }, function(response) {
      if (response && response.success) {
        // 显示下载开始的通知
        const notificationElement = document.createElement('div');
        notificationElement.className = 'notification success';
        notificationElement.textContent = `开始下载 ${response.count} 个视频文件到 "${folderName}" 文件夹`;
        document.body.appendChild(notificationElement);
        
        // 禁用下载按钮，防止重复点击
        downloadAll.disabled = true;
        downloadAll.textContent = '下载中...';
        
        // 3秒后自动关闭通知并恢复按钮
        setTimeout(() => {
          notificationElement.style.opacity = '0';
          setTimeout(() => {
            notificationElement.remove();
            downloadAll.disabled = false;
            downloadAll.textContent = '一键下载所有视频';
          }, 500);
        }, 3000);
      }
    });
  });
  
  // 显示视频列表
  function displayVideos(videos) {
    videoList.innerHTML = '';
    
    videos.forEach((video, index) => {
      const videoItem = document.createElement('div');
      videoItem.className = 'video-item';
      
      const videoInfoContainer = document.createElement('div');
      videoInfoContainer.className = 'video-info';
      
      const videoTitle = document.createElement('div');
      videoTitle.textContent = video.title || `视频 ${index + 1}`;
      
      const videoType = document.createElement('div');
      videoType.className = 'video-type';
      videoType.textContent = `类型: ${video.type || '未知'} | 大小: ${formatFileSize(video.size)}`;
      
      videoInfoContainer.appendChild(videoTitle);
      videoInfoContainer.appendChild(videoType);
      
      const downloadBtn = document.createElement('button');
      downloadBtn.className = 'download-btn';
      downloadBtn.textContent = '下载';
      downloadBtn.addEventListener('click', function() {
        // 获取自定义文件夹名称
        const folderName = folderNameInput.value.trim() || 'VideoDownloads';
        
        // 下载单个视频
        downloadVideo(video.url, video.title || 'video_' + Date.now(), video.type, folderName);
        
        // 显示下载开始的通知
        showNotification(`下载已开始: ${video.title || `视频 ${index + 1}`} → ${folderName}文件夹`);
      });
      
      videoItem.appendChild(videoInfoContainer);
      videoItem.appendChild(downloadBtn);
      videoList.appendChild(videoItem);
    });
  }
  
  // 显示通知
  function showNotification(message, type = 'success') {
    const notificationElement = document.createElement('div');
    notificationElement.className = `notification ${type}`;
    notificationElement.textContent = message;
    document.body.appendChild(notificationElement);
    
    // 3秒后自动关闭通知
    setTimeout(() => {
      notificationElement.style.opacity = '0';
      setTimeout(() => {
        notificationElement.remove();
      }, 500);
    }, 3000);
  }
  
  // 格式化文件大小
  function formatFileSize(bytes) {
    if (!bytes || bytes === 0) return '未知';
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return (bytes / Math.pow(1024, i)).toFixed(2) + ' ' + sizes[i];
  }
  
  // 获取文件扩展名
  function getFileExtension(url, type) {
    // 确定文件扩展名
    let extension = '.mp4';  // 默认为mp4
    if (type) {
      if (type.includes('m3u8') || url.includes('.m3u8')) {
        extension = '.m3u8';
      } else if (type.includes('webm')) {
        extension = '.webm';
      } else if (type.includes('ogg')) {
        extension = '.ogg';
      } else if (type.includes('mp4')) {
        extension = '.mp4';
      }
    } else {
      // 从URL尝试获取扩展名
      const urlExtMatch = url.match(/\.(mp4|webm|ogg|m3u8)($|\?)/i);
      if (urlExtMatch) {
        extension = '.' + urlExtMatch[1].toLowerCase();
      }
    }
    return extension;
  }
  
  // 下载视频函数
  function downloadVideo(url, filename, type, folderName = 'VideoDownloads') {
    const extension = getFileExtension(url, type);
    
    chrome.runtime.sendMessage({
      action: "downloadVideo",
      url: url,
      filename: `${folderName}/${sanitizeFilename(filename)}${extension}`,
      saveAs: settings.showSaveDialog
    });
  }
  
  // 文件名清理
  function sanitizeFilename(name) {
    return name.replace(/[/\\?%*:|"<>]/g, '-').substring(0, 100);  // 限制长度为100字符
  }
  
  // 自动扫描页面
  scanBtn.click();
}); 