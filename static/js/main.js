document.addEventListener('DOMContentLoaded', () => {
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

    async function fetchDailyReport() {
        loadingEl.classList.remove('hidden');
        
        if(reportContentEl.querySelector('.empty-state')) {
            reportContentEl.innerHTML = '<p style="color: var(--text-secondary); text-align: center; margin-top: 2rem;">正在自動加載今天的 AI 生成新聞報...</p>';
        }

        try {
            // 直接抓取由 GitHub Actions 每天在根目錄產生的 .md 檔案
            // 加入時間隨機碼防止瀏覽器快取舊資料
            const response = await fetch(`./latest_report.md?t=${new Date().getTime()}`);
            
            if (response.ok) {
                const markdownText = await response.text();
                // 成功取得報告，使用 markdown 渲染
                reportContentEl.innerHTML = marked.parse(markdownText);
                
                // 更新時間戳記
                const now = new Date();
                timestampEl.textContent = `閱覽時間：${now.toLocaleTimeString()}`;
                timestampEl.classList.remove('hidden');
            } else {
                // 如果找不到檔案
                reportContentEl.innerHTML = `<div style="color: var(--accent); text-align: center; margin-top:2rem;"><i class="fa-solid fa-triangle-exclamation"></i> <strong>哎呀！尚未找到今日的新聞編譯檔。</strong><br><br>請確認 GitHub Actions 的腳本已經成功運作，並產生了 \`latest_report.md\`。</div>`;
            }

        } catch (error) {
            console.error('抓取失敗:', error);
            reportContentEl.innerHTML = `<div style="color: var(--accent); text-align: center; margin-top:2rem;"><i class="fa-solid fa-triangle-exclamation"></i> 無法取得快照，請確認網路連線。</div>`;
        } finally {
            loadingEl.classList.add('hidden');
        }
    }
});
