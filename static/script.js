let currentData = null;
function getColorClass(value, limit) {
    if (limit === undefined || limit === null) return 'default';
    if (value > limit) return 'warning';
    return 'normal';}
function formatValue(value, unit = '%') {
    if (typeof value === 'number') {
        return value.toFixed(1) + unit;}
    return value;}
function displayMetrics(data) {
    let html = '';
    if (data.CPU && data.CPU.rep.percentage !== undefined) {
        const value = data.CPU.rep.percentage;
        const limit = data.CPU.lim?.percentage;
        const colorClass = getColorClass(value, limit);
        html += `
            <div class="metric">
                <div class="metric-name">CPU:</div>
                <div class="value ${colorClass}">${formatValue(value)}</div>
                ${limit ? `<div style="margin-left: 20px; font-size: 0.8em; color: #888;">лимит: ${limit}%</div>` : ''}
            </div>
        `;}
    if (data.MEM && data.MEM.rep.percentage !== undefined) {
        const value = data.MEM.rep.percentage;
        const limit = data.MEM.lim?.percentage;
        const colorClass = getColorClass(value, limit);
        html += `
            <div class="metric">
                <div class="metric-name">MEM (RAM):</div>
                <div class="value ${colorClass}">${formatValue(value)}</div>
                ${limit ? `<div style="margin-left: 20px; font-size: 0.8em; color: #888;">лимит: ${limit}%</div>` : ''}
            </div>
        `;}
    if (data.NWS) {
        if (data.NWS.rep.download_percent !== undefined) {
            const downValue = data.NWS.rep.download_percent;
            const downLimit = data.NWS.lim?.download_percent;
            const downColorClass = getColorClass(downValue, downLimit);
            html += `
                <div class="metric">
                    <div class="metric-name">NWS (загрузка):</div>
                    <div class="value ${downColorClass}">${formatValue(downValue)}</div>
                    ${downLimit ? `<div style="margin-left: 20px; font-size: 0.8em; color: #888;">лимит: ${downLimit}%</div>` : ''}
                </div>
            `;}
        if (data.NWS.rep.upload_percent !== undefined) {
            const upValue = data.NWS.rep.upload_percent;
            const upLimit = data.NWS.lim?.upload_percent;
            const upColorClass = getColorClass(upValue, upLimit);
            html += `
                <div class="metric">
                    <div class="metric-name">NWS (отдача):</div>
                    <div class="value ${upColorClass}">${formatValue(upValue)}</div>
                    ${upLimit ? `<div style="margin-left: 20px; font-size: 0.8em; color: #888;">лимит: ${upLimit}%</div>` : ''}
                </div>
            `;}}
    if (data.TIME) {
        html += `
            <div class="metric">
                <div class="metric-name">TIME:</div>
                <div class="value white">${data.TIME.rep.date} ${data.TIME.rep.time}</div>
            </div>
        `;}
    html += `<hr><div class="raw">Raw JSON:<br><pre>${JSON.stringify(data, null, 2)}</pre></div>`;

    document.getElementById('content').innerHTML = html;
}
async function updateData() {
    try {
        const response = await fetch('/api/data');
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const text = await response.text();
        const data = JSON.parse(text);
        currentData = data;
        displayMetrics(data);
    } catch (error) {
        document.getElementById('content').innerHTML = `
            <div style="color: #f48771;">Ошибка: ${error.message}</div>
            ${currentData ? '<div>Показываю последние данные...</div>' : ''}
        `;
        if (currentData) displayMetrics(currentData);}}
updateData();
setInterval(updateData, 2000);