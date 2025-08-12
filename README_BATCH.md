# 🎬 Snax Batch Video Generator

A batch video generation tool for Snax with multi-image upload and one-click download.

## ✨ Highlights

### 1. Batch generation
- Upload multiple images (drag & drop, multi-select)
- Apply a single prompt to all images
- Parallel processing for faster throughput
- Real-time progress

### 2. One-click download
- Auto-zip all videos after completion
- One-click download
- Filenames include original image names

### 3. Task management
- Live status (pending, processing, completed)
- Detailed progress (success/failure counts)
- Error logs
- Task delete and cleanup

## 🚀 Getting Started

### Option A: Launcher (recommended)
```bash
python start_batch_server.py
```

### Option B: Manual start
1) Install dependencies:
```bash
pip install -r requirements.txt
```

2) Run server:
```bash
python pika_batch_server.py
```

3) Open in browser:
```
http://localhost:5004
```

## 📖 Usage

### Step 1: Configure API Key
Enter your Snax API Key on the webpage

### Step 2: Enter prompt
Write the desired video effect; applied to all images

### Step 3: Upload images
- Click or drag to upload multiple images
- JPG/PNG supported
- Recommended < 10MB each

### Step 4: Start batch generation
Click "🚀 Start Batch Generation" — the system will:
1. Create a batch task
2. Process all images in parallel (thread pool)
3. Update progress in real-time

### Step 5: Monitor progress
- See task list with live progress
- Track success/failure counts
- Review error logs (if any)

### Step 6: Download videos
After completion, click "📦 Download all videos" to:
1. Auto-zip all videos
2. Download the ZIP
3. Filename format: `batch_videos_{task_id}.zip`

## 🔧 Technical features

### Backend
- ThreadPoolExecutor parallel processing
- Full task lifecycle management
- File management (upload, store, download, cleanup)
- Robust error handling and logging
- API proxy

### Frontend
- Drag-and-drop upload
- Auto-refresh every 5 seconds
- Visual progress and stats
- Responsive layout

## 📁 Structure

```
├── pika_batch_server.py      # Batch processing server
├── batch_frontend.html       # Frontend
├── start_batch_server.py     # Launcher
├── requirements.txt          # Dependencies
├── uploads/                  # Temp uploads
├── generated_videos/         # Output videos
└── downloads/               # Zipped downloads
```

## 🎯 API Endpoints

- `POST /batch/generate` - Start batch
- `GET /batch/tasks` - List tasks
- `GET /batch/status/{task_id}` - Task status
- `GET /batch/download/{task_id}` - Download all videos
- `DELETE /batch/delete/{task_id}` - Delete task and files

## ⚠️ Notes

1. **API Key**: Ensure a valid Snax API Key
2. **Network**: Stable connection recommended
3. **Storage**: Enough disk space for videos
4. **Concurrency**: Defaults to max 3 in parallel
5. **Timeout**: Max wait for a single video is 5 minutes

## 🔄 Changelog

### v1.0.0
- ✅ Multi-image upload
- ✅ Parallel video generation
- ✅ Real-time progress
- ✅ One-click download
- ✅ Task management
- ✅ Error handling and logs

## 🤝 Support

If you encounter issues, please check:
1. API Key validity
2. Network stability
3. Supported image formats
4. Browser console errors

---

Enjoy fast batch video generation! 🎉