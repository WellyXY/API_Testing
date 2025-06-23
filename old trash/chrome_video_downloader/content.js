// 监听来自popup的消息
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === "scanVideos") {
    const videos = scanPageForVideos();
    sendResponse({videos: videos});
  }
  return true;
});

// 扫描页面上的所有视频
function scanPageForVideos() {
  const results = [];
  const seenUrls = new Set(); // 用于去重
  
  // 1. 查找所有的video标签
  const videoElements = document.querySelectorAll('video');
  videoElements.forEach(video => {
    // 只获取有效的视频源
    if (video.src && video.src.trim() !== '' && !video.src.startsWith('blob:')) {
      const videoInfo = {
        url: video.src,
        title: extractVideoTitle(video),
        type: getVideoMimeType(video.src),
        size: video.videoWidth && video.videoHeight ? 
          `${video.videoWidth}x${video.videoHeight}` : '未知'
      };
      
      if (!seenUrls.has(videoInfo.url)) {
        results.push(videoInfo);
        seenUrls.add(videoInfo.url);
      }
    }
    
    // 获取video下的source标签
    const sources = video.querySelectorAll('source');
    sources.forEach(source => {
      if (source.src && source.src.trim() !== '' && !source.src.startsWith('blob:')) {
        const videoInfo = {
          url: source.src,
          title: extractVideoTitle(video),
          type: source.type || getVideoMimeType(source.src),
          size: video.videoWidth && video.videoHeight ? 
            `${video.videoWidth}x${video.videoHeight}` : '未知'
        };
        
        if (!seenUrls.has(videoInfo.url)) {
          results.push(videoInfo);
          seenUrls.add(videoInfo.url);
        }
      }
    });
  });
  
  // 2. 查找iframe中的视频（嵌入式视频）
  const iframes = document.querySelectorAll('iframe');
  iframes.forEach(iframe => {
    if (isVideoEmbed(iframe.src)) {
      const videoInfo = {
        url: iframe.src,
        title: iframe.title || getPageTitle(),
        type: '嵌入视频',
        size: '未知'
      };
      
      if (!seenUrls.has(videoInfo.url)) {
        results.push(videoInfo);
        seenUrls.add(videoInfo.url);
      }
    }
  });
  
  // 3. 查找object和embed标签中的视频
  const objects = document.querySelectorAll('object, embed');
  objects.forEach(obj => {
    if (obj.data && isVideoSource(obj.data)) {
      const videoInfo = {
        url: obj.data,
        title: obj.title || getPageTitle(),
        type: getVideoMimeType(obj.data),
        size: '未知'
      };
      
      if (!seenUrls.has(videoInfo.url)) {
        results.push(videoInfo);
        seenUrls.add(videoInfo.url);
      }
    }
  });
  
  // 4. 扫描页面中的m3u8链接
  const m3u8Links = findM3U8LinksInPage();
  m3u8Links.forEach(link => {
    const videoInfo = {
      url: link,
      title: 'HLS_Stream_' + Date.now(),
      type: 'application/x-mpegURL',
      size: '未知'
    };
    
    if (!seenUrls.has(videoInfo.url)) {
      results.push(videoInfo);
      seenUrls.add(videoInfo.url);
    }
  });
  
  // 5. 查找JSON数据中的视频链接
  findVideoLinksInScripts().forEach(link => {
    if (!seenUrls.has(link.url)) {
      results.push(link);
      seenUrls.add(link.url);
    }
  });
  
  return results;
}

// 提取视频标题
function extractVideoTitle(videoElement) {
  // 尝试从不同属性获取标题
  if (videoElement.title) return videoElement.title;
  if (videoElement.getAttribute('aria-label')) return videoElement.getAttribute('aria-label');
  if (videoElement.id) return videoElement.id;
  if (videoElement.dataset.title) return videoElement.dataset.title;
  
  // 尝试从父元素找标题
  let parent = videoElement.parentElement;
  for (let i = 0; i < 3 && parent; i++) { // 最多往上找3层
    if (parent.getAttribute('aria-label')) return parent.getAttribute('aria-label');
    if (parent.getAttribute('title')) return parent.getAttribute('title');
    if (parent.textContent && parent.textContent.trim().length < 100) 
      return parent.textContent.trim();
    parent = parent.parentElement;
  }
  
  // 使用页面标题
  return getPageTitle();
}

// 获取页面标题
function getPageTitle() {
  return document.title || 'Video_' + Date.now();
}

// 检查是否为视频嵌入链接
function isVideoEmbed(url) {
  if (!url) return false;
  const videoDomains = [
    'youtube.com/embed',
    'player.vimeo.com',
    'dailymotion.com/embed',
    'facebook.com/plugins/video',
    'twitch.tv/embed',
    'bilibili.com/blackboard',
    'player.youku.com'
  ];
  
  return videoDomains.some(domain => url.includes(domain));
}

// 检查URL是否为视频源
function isVideoSource(url) {
  if (!url) return false;
  const videoExtensions = ['.mp4', '.webm', '.ogg', '.mov', '.flv', '.avi', '.wmv', '.m3u8', '.mpd', '.ts'];
  return videoExtensions.some(ext => url.toLowerCase().includes(ext));
}

// 根据URL获取视频MIME类型
function getVideoMimeType(url) {
  if (!url) return '未知';
  
  if (url.includes('.mp4')) return 'video/mp4';
  if (url.includes('.webm')) return 'video/webm';
  if (url.includes('.ogg')) return 'video/ogg';
  if (url.includes('.mov')) return 'video/quicktime';
  if (url.includes('.flv')) return 'video/x-flv';
  if (url.includes('.avi')) return 'video/x-msvideo';
  if (url.includes('.wmv')) return 'video/x-ms-wmv';
  if (url.includes('.m3u8')) return 'application/x-mpegURL';
  if (url.includes('.mpd')) return 'application/dash+xml';
  if (url.includes('.ts')) return 'video/MP2T';
  
  return '未知';
}

// 在页面中寻找m3u8链接
function findM3U8LinksInPage() {
  const links = [];
  const pageContent = document.documentElement.innerHTML;
  
  // 使用正则表达式查找m3u8链接
  const m3u8Regex = /https?:\/\/[^"'\s]+\.m3u8/g;
  const matches = pageContent.match(m3u8Regex);
  
  if (matches) {
    // 去重
    return [...new Set(matches)];
  }
  
  return links;
}

// 在script标签中寻找可能的视频链接
function findVideoLinksInScripts() {
  const result = [];
  const scripts = document.querySelectorAll('script');
  
  for (const script of scripts) {
    const content = script.textContent;
    if (!content) continue;
    
    // 尝试找到JSON对象
    try {
      const videoRegex = /"(https?:\/\/[^"]+\.(mp4|webm|m3u8|ts))"/g;
      let match;
      while ((match = videoRegex.exec(content)) !== null) {
        const url = match[1];
        if (isVideoSource(url)) {
          result.push({
            url: url,
            title: `Script_Video_${result.length + 1}`,
            type: getVideoMimeType(url),
            size: '未知'
          });
        }
      }
    } catch (e) {
      // 忽略解析错误
      continue;
    }
  }
  
  return result;
} 