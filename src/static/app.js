document.addEventListener("DOMContentLoaded", () => {
    const queryInput = document.getElementById("queryInput");
    const sendBtn = document.getElementById("sendBtn");
    const resultsContainer = document.getElementById("resultsContainer");

    sendBtn.addEventListener("click", handleSearch);
    queryInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") handleSearch();
    });

    async function handleSearch() {
        const query = queryInput.value.trim();
        if (!query) return;

        resultsContainer.innerHTML = `<div class="status-text">Searching Milvus...</div>`;

        try {
            const response = await fetch("/api/search", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    query: query,
                    limit: 5
                })
            });

            const data = await response.json();
            renderResults(query, data.results);
        } catch (err) {
            resultsContainer.innerHTML = `<div class="status-text">Error connecting to search API.</div>`;
        }
    }

    function renderResults(query, results) {
        if (!results || results.length === 0) {
            resultsContainer.innerHTML = `<div class="status-text">No results found for "${escapeHtml(query)}".</div>`;
            return;
        }

        let html = "";
        results.forEach(item => {
            html += `
        <div class="result-card">
          <div class="result-header">
            <span class="result-title">${escapeHtml(item.name)}</span>
            <span class="result-score">${(item.score * 100).toFixed(1)}% match</span>
          </div>
          <div class="result-meta">${escapeHtml(item.category)} • ${escapeHtml(item.location)}</div>
          <div class="result-description">${escapeHtml(item.description)}</div>
        </div>
      `;
        });

        resultsContainer.innerHTML = html;
    }

    function escapeHtml(str) {
        return str.replace(/[&<>"']/g, (m) => ({
            '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
        }[m]));
    }
});