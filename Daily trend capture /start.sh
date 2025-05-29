#!/bin/bash

# 確保腳本以終止狀態失敗
set -e

echo "準備啟動Google趨勢數據查詢服務..."

# 檢查是否安裝了Node.js
if ! command -v node &> /dev/null; then
    echo "錯誤: 需要安裝Node.js才能運行此服務。"
    echo "請訪問 https://nodejs.org/ 下載並安裝Node.js"
    exit 1
fi

# 安裝依賴
echo "正在安裝API服務器的依賴..."
npm install

# 啟動服務器
echo "啟動API服務器..."
echo "API服務器運行在 http://localhost:3001"

# 在新窗口中打開瀏覽器
echo "正在打開網頁..."
sleep 2

# 檢測操作系統並打開瀏覽器
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open ../index.html
    node server.js
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open ../index.html
    node server.js
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    start ../index.html
    node server.js
else
    echo "請手動打開瀏覽器訪問 index.html 文件"
    node server.js
fi 