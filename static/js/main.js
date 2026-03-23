document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyze-btn');
    const loadingEl = document.getElementById('loading');
    const reportContentEl = document.getElementById('report-content');
    const timestampEl = document.getElementById('timestamp');

    // 設定 marked.js 的選項，確保安全與換行處理
    marked.setOptions({
        breaks: true,
        gfm: true
    });

    analyzeBtn.addEventListener('click', async () => {
        // UI 狀態切換：防呆、顯示載入中
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> 處理中...';
        loadingEl.classList.remove('hidden');
        
        // 若為第一次點擊，清除空狀態
        if(reportContentEl.querySelector('.empty-state')) {
            reportContentEl.innerHTML = '<p style="color: var(--text-secondary); text-align: center; margin-top: 2rem;">正在透過 API 擷取全球新聞數據，並進行 LLM 模型推論階段...</p>';
        }

        try {
            // 向後端 Flask 發送 API 請求
            const response = await fetch('/api/analyze');
            const data = await response.json();

            if (data.status === 'success') {
                // 成功取得報告，使用 markdown 渲染
                reportContentEl.innerHTML = marked.parse(data.report);
                
                // 更新時間戳記
                const now = new Date();
                timestampEl.textContent = `最新更新：${now.toLocaleTimeString()}`;
                timestampEl.classList.remove('hidden');
            } else {
                // 回報錯誤
                reportContentEl.innerHTML = `<div style="color: var(--accent);"><i class="fa-solid fa-triangle-exclamation"></i> 錯誤：${data.message}</div>`;
            }

        } catch (error) {
            console.error('API 請求失敗:', error);
            reportContentEl.innerHTML = `<div style="color: var(--accent);"><i class="fa-solid fa-triangle-exclamation"></i> 無法連接分析伺服器，請確認伺服器與網路狀態。</div>`;
        } finally {
            // UI 狀態復原
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = '<i class="fa-solid fa-bolt"></i> 啟動即時分析';
            loadingEl.classList.add('hidden');
        }
    });
});
