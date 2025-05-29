const fs = require('fs');
const path = require('path');
const https = require('https');
const { execSync } = require('child_process');

// 创建保存目录
const downloadDir = path.join(__dirname, 'download', 'Benchmark');
if (!fs.existsSync(downloadDir)) {
  fs.mkdirSync(downloadDir, { recursive: true });
}

// 提取的视频链接
const videoLinks = [
  { name: "Video-3_Brianne", url: "https://pika-git-feat-model-25-pika-labs.vercel.app/video/b655b0b8-3837-4e63-8053-341c4035a68f" },
  { name: "Video-4", url: "https://pika-git-feat-model-25-pika-labs.vercel.app/video/55393631-da99-40c7-8c41-cffc0469aa2f" },
  { name: "Video-5", url: "https://pika-git-feat-model-25-pika-labs.vercel.app/video/a0c7942a-bdb9-4687-a743-5dd54b9e41ed" },
  { name: "Video-7", url: "https://pika-git-feat-model-25-pika-labs.vercel.app/video/d44a5a2b-7d9a-4e2c-9b45-2358bb505bcf" },
  { name: "Video-8", url: "https://pika-git-feat-model-25-pika-labs.vercel.app/video/3c34515d-cd6a-44f5-b3f4-142738181b4a" },
  { name: "Video-9", url: "https://pika-git-feat-model-25-pika-labs.vercel.app/video/94e676d4-6ca8-4784-b78b-b0726806ac69" },
  { name: "Video-10", url: "https://pika-git-feat-model-25-pika-labs.vercel.app/video/1edc97df-23d5-4b4b-96df-ab2c6e3b3e43" },
  { name: "Video-11", url: "https://pika-git-feat-model-25-pika-labs.vercel.app/video/a18c5da5-9580-43fc-a6d3-25464bc4eaf0" },
  { name: "Video-12", url: "https://pika-git-feat-model-25-pika-labs.vercel.app/video/c7ac14c6-5242-4c14-97f3-eb108979aab7" },
  { name: "Video-13", url: "https://pika-git-feat-model-25-pika-labs.vercel.app/video/afb323f3-e9d4-46c7-8b0a-54aa121102c2" },
  { name: "Video-14", url: "https://pika-git-feat-model-25-pika-labs.vercel.app/video/0817f8b5-e43c-4672-b0cd-69483bb07f11" },
  { name: "Video-15", url: "https://pika-git-feat-model-25-pika-labs.vercel.app/video/25023c0e-651f-46c5-bd7a-2b6089158372" },
  { name: "Video-16", url: "https://pika-git-feat-model-25-pika-labs.vercel.app/video/fad77112-2af1-4863-9851-789d1affff70" },
  { name: "Video-17", url: "https://pika-git-feat-model-25-pika-labs.vercel.app/video/19b002ee-5c25-4e9b-9039-70b77b0fd5c0" },
  { name: "Video-18", url: "https://pika-git-feat-model-25-pika-labs.vercel.app/video/c93a0737-2af7-49bf-85e3-b01c1bfaf409" },
  { name: "Video-19", url: "https://pika-git-feat-model-25-pika-labs.vercel.app/video/d5ada7b4-6394-4e2d-9e66-0fcdd6d60ad8" },
  { name: "Video-20", url: "https://pika-git-feat-model-25-pika-labs.vercel.app/video/9588f8eb-b091-4592-9d48-c5b0b2a5bce8" },
  { name: "Video-21", url: "https://pika-git-feat-model-25-pika-labs.vercel.app/video/c7ac14c6-5242-4c14-97f3-eb108979aab7" },
  { name: "Video-22", url: "https://pika-git-feat-model-25-pika-labs.vercel.app/video/07b2da58-327d-42a4-b5ff-b46f8ffa588c" },
  { name: "Video-23", url: "https://pika-git-feat-model-25-pika-labs.vercel.app/video/b9f39d28-75dd-4625-855c-effd9f29a5d2" },
  { name: "Video-24", url: "https://pika-git-feat-model-25-pika-labs.vercel.app/video/bd60ef28-f6bb-42ee-a772-621cab940b97" },
];

/**
 * 从Pika页面提取视频直链
 * @param {string} url - Pika视频页面URL
 * @returns {Promise<string>} - 返回视频直链URL
 */
async function getVideoDirectUrl(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        try {
          // 使用正则表达式查找视频链接
          const videoMatch = data.match(/"url":"(https:\/\/[^"]+\.mp4)"/);
          if (videoMatch && videoMatch[1]) {
            // 替换转义的URL
            const videoUrl = videoMatch[1].replace(/\\u002F/g, '/');
            resolve(videoUrl);
          } else {
            reject(new Error('未能找到视频直链'));
          }
        } catch (error) {
          reject(error);
        }
      });
    }).on('error', (error) => {
      reject(error);
    });
  });
}

/**
 * 下载视频文件
 * @param {string} url - 视频直链URL
 * @param {string} filepath - 保存路径
 * @returns {Promise<void>}
 */
async function downloadVideo(url, filepath) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      // 检查响应状态码
      if (res.statusCode !== 200) {
        reject(new Error(`Failed to download video: ${res.statusCode}`));
        return;
      }
      
      const fileStream = fs.createWriteStream(filepath);
      res.pipe(fileStream);
      
      fileStream.on('finish', () => {
        fileStream.close();
        resolve();
      });
      
      fileStream.on('error', (error) => {
        fs.unlink(filepath, () => {}); // 删除不完整的文件
        reject(error);
      });
    }).on('error', (error) => {
      fs.unlink(filepath, () => {}); // 删除不完整的文件
      reject(error);
    });
  });
}

/**
 * 使用curl下载视频（备选方法）
 * @param {string} url - 视频直链URL
 * @param {string} filepath - 保存路径
 */
function downloadWithCurl(url, filepath) {
  try {
    console.log(`正在使用curl下载: ${filepath}`);
    execSync(`curl -L "${url}" -o "${filepath}"`, { stdio: 'inherit' });
    return true;
  } catch (error) {
    console.error(`curl下载失败: ${error.message}`);
    return false;
  }
}

/**
 * 主下载函数
 */
async function downloadAllVideos() {
  console.log(`开始下载 ${videoLinks.length} 个视频到 ${downloadDir}`);
  
  let successCount = 0;
  let failCount = 0;
  
  for (let i = 0; i < videoLinks.length; i++) {
    const { name, url } = videoLinks[i];
    const filename = `${name}.mp4`;
    const filepath = path.join(downloadDir, filename);
    
    console.log(`\n[${i+1}/${videoLinks.length}] 正在处理: ${name}`);
    console.log(`页面URL: ${url}`);
    
    try {
      // 获取视频直链
      console.log('正在获取视频直链...');
      const directUrl = await getVideoDirectUrl(url);
      console.log(`获取成功: ${directUrl}`);
      
      // 下载视频
      console.log(`正在下载视频到: ${filepath}`);
      try {
        await downloadVideo(directUrl, filepath);
        console.log('✅ 下载成功!');
        successCount++;
      } catch (downloadError) {
        console.log('使用Node.js下载失败，尝试使用curl...');
        if (downloadWithCurl(directUrl, filepath)) {
          console.log('✅ curl下载成功!');
          successCount++;
        } else {
          console.error('❌ 两种方法均下载失败');
          failCount++;
        }
      }
    } catch (error) {
      console.error(`❌ 处理失败: ${error.message}`);
      failCount++;
    }
  }
  
  console.log(`\n下载完成! 成功: ${successCount}, 失败: ${failCount}`);
}

// 开始执行下载
downloadAllVideos().catch(error => {
  console.error('程序执行错误:', error);
}); 