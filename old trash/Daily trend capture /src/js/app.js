document.addEventListener('DOMContentLoaded', () => {
    // 获取DOM元素
    const keywordInput = document.getElementById('keyword-input');
    const searchBtn = document.getElementById('search-btn');
    const trendChartCanvas = document.getElementById('trend-chart');
    const countryChartCanvas = document.getElementById('country-chart');
    const hotKeywordsList = document.getElementById('hot-keywords-list');
    const dataSourceIndicator = document.getElementById('data-source-indicator');
    
    // API基础URL - 本地开发服务器
    const API_BASE_URL = 'http://localhost:3001/api';
    
    // 初始化Chart.js实例
    let trendChart = null;
    let countryChart = null;
    
    // 重试设置
    const MAX_RETRIES = 3;
    const RETRY_DELAY = 2000; // 2秒
    
    // 初始化页面数据
    loadData(keywordInput.value);
    
    // 搜索按钮点击事件
    searchBtn.addEventListener('click', () => {
        loadData(keywordInput.value);
    });
    
    // 输入框回车事件
    keywordInput.addEventListener('keyup', (event) => {
        if (event.key === 'Enter') {
            loadData(keywordInput.value);
        }
    });
    
    // 设置数据源指示器
    function setDataSourceIndicator(isLoading = false, isError = false) {
        if (isLoading) {
            dataSourceIndicator.className = 'loading-data';
            dataSourceIndicator.querySelector('.indicator-text').textContent = '正在获取数据...';
        } else if (isError) {
            dataSourceIndicator.className = 'error-data';
            dataSourceIndicator.querySelector('.indicator-text').textContent = '获取数据失败';
        } else {
            dataSourceIndicator.className = 'real-data';
            dataSourceIndicator.querySelector('.indicator-text').textContent = '使用真实数据';
        }
    }
    
    // 加载数据函数
    async function loadData(keyword) {
        try {
            // 显示载入中的状态
            displayLoadingState();
            setDataSourceIndicator(true, false);
            
            // 并行请求所有API，带有重试机制
            const [trendData, relatedData, countryData] = await Promise.all([
                fetchWithRetry(() => fetchTrendData(keyword), MAX_RETRIES, RETRY_DELAY),
                fetchWithRetry(() => fetchRelatedQueries(keyword), MAX_RETRIES, RETRY_DELAY),
                fetchWithRetry(() => fetchCountryData(keyword), MAX_RETRIES, RETRY_DELAY)
            ]);
            
            // 更新UI
            updateTrendChart(keyword, trendData);
            updateHotKeywords(relatedData);
            updateCountryChart(keyword, countryData);
            
            // 设置为真实数据指示器
            setDataSourceIndicator(false, false);
            
            // 移除载入中状态
            removeLoadingState();
        } catch (error) {
            console.error('数据载入错误:', error);
            
            // 清空图表和列表
            clearAllData();
            
            // 设置为错误状态
            setDataSourceIndicator(false, true);
            
            // 移除载入中状态
            removeLoadingState();
            
            // 显示详细错误信息
            showErrorMessage(error.message || '无法获取真实数据，请稍后再试');
        }
    }
    
    // 使用重试机制的API请求
    async function fetchWithRetry(fetchFunc, maxRetries, delay) {
        let lastError;
        
        for (let attempt = 0; attempt < maxRetries; attempt++) {
            try {
                // 尝试获取数据
                return await fetchFunc();
            } catch (error) {
                lastError = error;
                console.log(`第 ${attempt + 1} 次尝试失败，${maxRetries - attempt - 1} 次重试机会剩余`);
                
                // 最后一次尝试失败，抛出错误
                if (attempt === maxRetries - 1) {
                    throw error;
                }
                
                // 等待一段时间再重试
                await new Promise(resolve => setTimeout(resolve, delay));
            }
        }
        
        throw lastError;
    }
    
    // 显示错误信息
    function showErrorMessage(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.innerHTML = `
            <h3>无法获取真实数据</h3>
            <p>${message}</p>
            <p>可能原因：</p>
            <ul>
                <li>网络连接问题</li>
                <li>Google API 限制或超时</li>
                <li>服务器未正确运行</li>
            </ul>
            <p>建议：检查网络连接并稍后再试</p>
        `;
        
        // 添加到页面中
        document.querySelector('main').prepend(errorDiv);
    }
    
    // 清空所有数据
    function clearAllData() {
        // 清空趋势图表
        if (trendChart) {
            trendChart.destroy();
            trendChart = null;
        }
        
        // 清空国家图表
        if (countryChart) {
            countryChart.destroy();
            countryChart = null;
        }
        
        // 清空热门关键词列表
        hotKeywordsList.innerHTML = '';
        
        // 移除之前的错误消息
        const prevError = document.querySelector('.error-message');
        if (prevError) prevError.remove();
    }
    
    // 显示加载中状态
    function displayLoadingState() {
        // 清空之前的所有数据
        clearAllData();
        
        document.querySelectorAll('.chart-container').forEach(container => {
            container.classList.add('loading');
            container.innerHTML = '<canvas></canvas><div class="loading-indicator">数据加载中...</div>';
        });
        
        hotKeywordsList.innerHTML = '<li class="loading-item">数据加载中...</li>';
    }
    
    // 移除加载中状态
    function removeLoadingState() {
        document.querySelectorAll('.chart-container').forEach(container => {
            container.classList.remove('loading');
            const indicator = container.querySelector('.loading-indicator');
            if (indicator) indicator.remove();
        });
    }
    
    // 获取趋势数据
    async function fetchTrendData(keyword) {
        const response = await fetch(`${API_BASE_URL}/trends?keyword=${encodeURIComponent(keyword)}`);
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`趋势数据请求失败: ${response.status} ${errorText}`);
        }
        return await response.json();
    }
    
    // 获取相关查询数据
    async function fetchRelatedQueries(keyword) {
        const response = await fetch(`${API_BASE_URL}/related-queries?keyword=${encodeURIComponent(keyword)}`);
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`相关查询数据请求失败: ${response.status} ${errorText}`);
        }
        return await response.json();
    }
    
    // 获取国家数据
    async function fetchCountryData(keyword) {
        const response = await fetch(`${API_BASE_URL}/countries?keyword=${encodeURIComponent(keyword)}`);
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`国家数据请求失败: ${response.status} ${errorText}`);
        }
        return await response.json();
    }
    
    // 更新趋势图表
    function updateTrendChart(keyword, data) {
        // 处理API返回数据
        const timelineData = data.default.timelineData;
        const dates = timelineData.map(item => new Date(parseInt(item.time) * 1000).toLocaleDateString('zh-CN', {month: 'short', day: 'numeric'}));
        const values = timelineData.map(item => parseInt(item.value[0]));
        
        // 更新或创建图表
        if (trendChart) {
            trendChart.destroy();
        }
        
        trendChart = new Chart(document.getElementById('trend-chart'), {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: `"${keyword}" 搜索趋势指数`,
                    data: values,
                    borderColor: '#1a73e8',
                    backgroundColor: 'rgba(26, 115, 232, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    },
                    legend: {
                        position: 'top',
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    // 更新热门关键词
    function updateHotKeywords(data) {
        // 处理API返回数据
        const relatedQueries = data.default.rankedList[0].rankedKeyword || [];
        const topQueries = relatedQueries.slice(0, 5);
        
        // 更新DOM
        hotKeywordsList.innerHTML = '';
        if (topQueries.length === 0) {
            hotKeywordsList.innerHTML = '<li>没有找到相关关键词数据</li>';
            return;
        }
        
        topQueries.forEach(item => {
            const li = document.createElement('li');
            li.innerHTML = `
                <span>${item.query}</span>
                <span class="score">${item.value}</span>
            `;
            hotKeywordsList.appendChild(li);
        });
    }
    
    // 更新国家图表
    function updateCountryChart(keyword, data) {
        // 处理API返回数据
        const geoData = data.default.geoMapData || [];
        
        // 按搜索量排序
        const sortedData = [...geoData].sort((a, b) => b.value[0] - a.value[0]).slice(0, 5);
        
        // 提取排序后的国家名和数值
        const countryNames = sortedData.map(item => item.geoName);
        const countryValues = sortedData.map(item => item.value[0]);
        
        // 更新或创建图表
        if (countryChart) {
            countryChart.destroy();
        }
        
        if (countryNames.length === 0) {
            document.querySelector('.top-countries .chart-container').innerHTML = '<div class="no-data">没有足够的数据</div>';
            return;
        }
        
        countryChart = new Chart(document.getElementById('country-chart'), {
            type: 'bar',
            data: {
                labels: countryNames,
                datasets: [{
                    label: `"${keyword}" 搜索热度`,
                    data: countryValues,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(153, 102, 255, 0.7)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y',
                plugins: {
                    legend: {
                        position: 'top',
                    }
                }
            }
        });
    }
}); 