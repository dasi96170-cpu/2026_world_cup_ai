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

    // 初次載入即自動抓取報紙
    fetchDailyReport();

    // 讓按鈕也能重新整理
    analyzeBtn.addEventListener('click', fetchDailyReport);

    async function fetchDailyReport() {
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> 正在載入日報...';
        loadingEl.classList.remove('hidden');
        
        if(reportContentEl.querySelector('.empty-state')) {
            reportContentEl.innerHTML = '<p style="color: var(--text-secondary); text-align: center; margin-top: 2rem;">正在加載最新的 GitHub 自動編譯快照...</p>';
        }

        try {
            // 直接抓取由 GitHub Actions 每天在根目錄產生的 .md 檔案
            // 由於是靜態網站，加上時間戳避免快取
            const response = await fetch(`./latest_report.md?t=${new Date().getTime()}`);
            
            if (response.ok) {
                const markdownText = await response.text();
                // 成功取得報告，使用 markdown 渲染
                reportContentEl.innerHTML = marked.parse(markdownText);
                
                // 更新時間戳記
                const now = new Date();
                timestampEl.textContent = `快取更新時間：${now.toLocaleTimeString()}`;
                timestampEl.classList.remove('hidden');
            } else {
                // 如果找不到檔案（可能剛建立 GitHub Pages 還沒跑完）
                reportContentEl.innerHTML = `<div style="color: var(--accent);"><i class="fa-solid fa-triangle-exclamation"></i> 錯誤：尚未找到今日的新聞編譯檔，請確認 GitHub Actions 是否執行成功。</div>`;
            }

        } catch (error) {
            console.error('抓取失敗:', error);
            reportContentEl.innerHTML = `<div style="color: var(--accent);"><i class="fa-solid fa-triangle-exclamation"></i> 無法取得快照，請確認網路連線。</div>`;
        } finally {
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = '<i class="fa-solid fa-clock-rotate-left"></i> 重新載入日報';
            loadingEl.classList.add('hidden');
        }
    }
});
