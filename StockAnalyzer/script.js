// Stock Financial Dashboard Web Application
class StockDashboard {
    constructor() {
        this.currentStock = null;
        this.historicalData = [];
        this.financialMetrics = {};
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupTabs();
    }

    setupEventListeners() {
        // Search functionality
        const searchBtn = document.getElementById('searchBtn');
        const stockInput = document.getElementById('stockSymbol');
        
        searchBtn.addEventListener('click', () => this.searchStock());
        stockInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.searchStock();
        });

        // Popular symbol buttons
        document.querySelectorAll('.symbol-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const symbol = btn.dataset.symbol;
                document.getElementById('stockSymbol').value = symbol;
                this.searchStock();
            });
        });

        // Chart type controls
        document.querySelectorAll('input[name="chartType"]').forEach(radio => {
            radio.addEventListener('change', () => this.updateCharts());
        });

        // Time period selector
        document.getElementById('timePeriod').addEventListener('change', () => {
            if (this.currentStock) {
                this.loadStockData(this.currentStock);
            }
        });

        // Export buttons
        document.getElementById('exportCsv').addEventListener('click', () => this.exportData('csv'));
        document.getElementById('exportJson').addEventListener('click', () => this.exportData('json'));
    }

    setupTabs() {
        const tabBtns = document.querySelectorAll('.tab-btn');
        const tabPanels = document.querySelectorAll('.tab-panel');

        tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const tabId = btn.dataset.tab;
                
                // Remove active class from all tabs and panels
                tabBtns.forEach(b => b.classList.remove('active'));
                tabPanels.forEach(p => p.classList.remove('active'));
                
                // Add active class to clicked tab and corresponding panel
                btn.classList.add('active');
                document.getElementById(tabId).classList.add('active');
            });
        });
    }

    async searchStock() {
        const symbol = document.getElementById('stockSymbol').value.trim().toUpperCase();
        if (!symbol) {
            this.showError('Por favor ingresa un símbolo de stock válido');
            return;
        }

        this.showLoading(true);
        this.hideError();
        
        try {
            await this.loadStockData(symbol);
            this.currentStock = symbol;
            this.showContent();
        } catch (error) {
            this.showError(`Error cargando datos para ${symbol}: ${error.message}`);
        } finally {
            this.showLoading(false);
        }
    }

    async loadStockData(symbol) {
        const period = document.getElementById('timePeriod').value;
        
        // Simulate Yahoo Finance API call (replace with actual API)
        const data = await this.fetchStockData(symbol, period);
        
        this.historicalData = data.historical;
        this.financialMetrics = data.metrics;
        
        this.updateStockInfo(symbol, data.info);
        this.updateCharts();
        this.updateMetrics();
        this.updateAnalysis();
        this.updateHistoricalTable();
    }

    async fetchStockData(symbol, period) {
        // This is a simulation - replace with actual Yahoo Finance API call
        // For demo purposes, generating realistic looking data
        
        const basePrice = Math.random() * 200 + 50; // $50-$250 range
        const change = (Math.random() - 0.5) * 10; // -5 to +5 change
        const changePercent = (change / basePrice) * 100;
        
        // Generate historical data
        const days = this.getPeriodDays(period);
        const historical = this.generateHistoricalData(basePrice, days);
        
        // Generate financial metrics
        const metrics = this.generateFinancialMetrics(basePrice);
        
        return {
            info: {
                name: `${symbol} Inc.`,
                price: basePrice,
                change: change,
                changePercent: changePercent,
                volume: Math.floor(Math.random() * 50000000 + 1000000),
                marketCap: Math.floor(Math.random() * 500000000000 + 10000000000)
            },
            historical: historical,
            metrics: metrics
        };
    }

    getPeriodDays(period) {
        const periodMap = {
            '1mo': 30,
            '3mo': 90,
            '6mo': 180,
            '1y': 365,
            '2y': 730,
            '5y': 1825
        };
        return periodMap[period] || 180;
    }

    generateHistoricalData(basePrice, days) {
        const data = [];
        let price = basePrice;
        const startDate = new Date();
        startDate.setDate(startDate.getDate() - days);

        for (let i = 0; i < days; i++) {
            const date = new Date(startDate);
            date.setDate(date.getDate() + i);
            
            const volatility = 0.02; // 2% daily volatility
            const change = (Math.random() - 0.5) * volatility * price;
            price += change;
            
            const open = price + (Math.random() - 0.5) * volatility * price * 0.5;
            const high = Math.max(open, price) + Math.random() * volatility * price * 0.5;
            const low = Math.min(open, price) - Math.random() * volatility * price * 0.5;
            const volume = Math.floor(Math.random() * 10000000 + 100000);

            data.push({
                date: date.toISOString().split('T')[0],
                open: Number(open.toFixed(2)),
                high: Number(high.toFixed(2)),
                low: Number(low.toFixed(2)),
                close: Number(price.toFixed(2)),
                volume: volume
            });
        }

        return data;
    }

    generateFinancialMetrics(basePrice) {
        return {
            'Current Price': basePrice.toFixed(2),
            'Day Low': (basePrice * 0.98).toFixed(2),
            'Day High': (basePrice * 1.02).toFixed(2),
            '52 Week Low': (basePrice * 0.8).toFixed(2),
            '52 Week High': (basePrice * 1.2).toFixed(2),
            'P/E Ratio': (15 + Math.random() * 20).toFixed(2),
            'Market Cap': this.formatNumber(Math.floor(Math.random() * 500000000000 + 10000000000)),
            'Beta': (0.5 + Math.random() * 1.5).toFixed(2),
            'EPS': (Math.random() * 10).toFixed(2),
            'Dividend Yield': (Math.random() * 5).toFixed(2) + '%',
            'Debt to Equity': (Math.random() * 2).toFixed(2),
            'ROE': (5 + Math.random() * 20).toFixed(2) + '%',
            'ROA': (2 + Math.random() * 15).toFixed(2) + '%',
            'Profit Margin': (5 + Math.random() * 25).toFixed(2) + '%'
        };
    }

    updateStockInfo(symbol, info) {
        document.getElementById('stockName').textContent = info.name;
        document.getElementById('currentPrice').textContent = `$${info.price.toFixed(2)}`;
        
        const priceChangeEl = document.getElementById('priceChange');
        const changeSymbol = info.change >= 0 ? '+' : '';
        priceChangeEl.textContent = `${changeSymbol}${info.change.toFixed(2)} (${changeSymbol}${info.changePercent.toFixed(2)}%)`;
        priceChangeEl.className = `price-change ${info.change >= 0 ? 'positive' : 'negative'}`;
        
        document.getElementById('volume').textContent = this.formatNumber(info.volume);
        document.getElementById('marketCap').textContent = `$${this.formatNumber(info.marketCap)}`;
    }

    updateCharts() {
        if (!this.historicalData.length) return;

        const chartType = document.querySelector('input[name="chartType"]:checked').value;
        this.createMainChart(chartType);
        this.createVolumeChart();
    }

    createMainChart(type) {
        const data = this.historicalData;
        const container = document.getElementById('mainChart');
        
        let trace;
        if (type === 'candlestick') {
            trace = {
                type: 'candlestick',
                x: data.map(d => d.date),
                open: data.map(d => d.open),
                high: data.map(d => d.high),
                low: data.map(d => d.low),
                close: data.map(d => d.close),
                increasing: { line: { color: '#00cc44' } },
                decreasing: { line: { color: '#ff4444' } },
                name: 'Price'
            };
        } else {
            trace = {
                type: 'scatter',
                mode: 'lines',
                x: data.map(d => d.date),
                y: data.map(d => d.close),
                line: { color: '#2962ff', width: 2 },
                name: 'Price'
            };
        }

        // Add moving averages
        const traces = [trace];
        const maColors = ['#ff9500', '#9c27b0', '#00bcd4'];
        const maPeriods = [20, 50, 200];

        maPeriods.forEach((period, index) => {
            if (data.length >= period) {
                const maData = this.calculateMovingAverage(data.map(d => d.close), period);
                traces.push({
                    type: 'scatter',
                    mode: 'lines',
                    x: data.slice(period - 1).map(d => d.date),
                    y: maData,
                    line: { color: maColors[index], width: 1 },
                    name: `MA${period}`
                });
            }
        });

        const layout = {
            title: `${this.currentStock} Price Chart`,
            xaxis: { title: 'Date' },
            yaxis: { title: 'Price ($)' },
            template: 'plotly_dark',
            paper_bgcolor: '#1e222d',
            plot_bgcolor: '#1e222d',
            font: { color: '#d1d4dc' }
        };

        Plotly.newPlot(container, traces, layout, { responsive: true });
    }

    createVolumeChart() {
        const data = this.historicalData;
        const container = document.getElementById('volumeChart');

        const colors = data.map((d, i) => {
            if (i === 0) return '#00cc44';
            return d.close >= data[i-1].close ? '#00cc44' : '#ff4444';
        });

        const trace = {
            type: 'bar',
            x: data.map(d => d.date),
            y: data.map(d => d.volume),
            marker: { color: colors },
            name: 'Volume'
        };

        const layout = {
            title: 'Volume Chart',
            xaxis: { title: 'Date' },
            yaxis: { title: 'Volume' },
            template: 'plotly_dark',
            paper_bgcolor: '#1e222d',
            plot_bgcolor: '#1e222d',
            font: { color: '#d1d4dc' }
        };

        Plotly.newPlot(container, [trace], layout, { responsive: true });
    }

    calculateMovingAverage(prices, period) {
        const ma = [];
        for (let i = period - 1; i < prices.length; i++) {
            const sum = prices.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0);
            ma.push(sum / period);
        }
        return ma;
    }

    updateMetrics() {
        const container = document.getElementById('metricsTable');
        
        const table = document.createElement('table');
        table.innerHTML = `
            <thead>
                <tr>
                    <th>Métrica</th>
                    <th>Valor</th>
                </tr>
            </thead>
            <tbody>
                ${Object.entries(this.financialMetrics).map(([key, value]) => `
                    <tr>
                        <td>${key}</td>
                        <td>${value}</td>
                    </tr>
                `).join('')}
            </tbody>
        `;
        
        container.innerHTML = '';
        container.appendChild(table);
    }

    updateAnalysis() {
        this.updatePriceRange();
        this.updateTechnicalAnalysis();
        this.updateAnalystOpinion();
        this.updateInvestmentSummary();
        this.updateCompanyHealth();
        this.updateMarketSentiment();
    }

    updatePriceRange() {
        const current = parseFloat(this.financialMetrics['Current Price']);
        const dayLow = parseFloat(this.financialMetrics['Day Low']);
        const dayHigh = parseFloat(this.financialMetrics['Day High']);
        const week52Low = parseFloat(this.financialMetrics['52 Week Low']);
        const week52High = parseFloat(this.financialMetrics['52 Week High']);

        const dayProgress = ((current - dayLow) / (dayHigh - dayLow)) * 100;
        const yearProgress = ((current - week52Low) / (week52High - week52Low)) * 100;

        document.getElementById('priceRangeContent').innerHTML = `
            <h4>Rango del Día</h4>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>$${dayLow.toFixed(2)}</span>
                <span>$${dayHigh.toFixed(2)}</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${dayProgress}%; background: var(--primary-blue);"></div>
            </div>
            
            <h4>Rango de 52 Semanas</h4>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>$${week52Low.toFixed(2)}</span>
                <span>$${week52High.toFixed(2)}</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${yearProgress}%; background: var(--primary-blue);"></div>
            </div>
        `;
    }

    updateTechnicalAnalysis() {
        const score = Math.floor(Math.random() * 40) + 60; // 60-100 range for demo
        
        let recommendation, color;
        if (score >= 70) {
            recommendation = "Compra fuerte";
            color = "#00cc44";
        } else if (score >= 50) {
            recommendation = "Compra";
            color = "#ffaa00";
        } else {
            recommendation = "Precaución";
            color = "#ff4444";
        }

        // Create gauge using Plotly
        const gaugeData = [{
            type: "indicator",
            mode: "gauge+number+delta",
            value: score,
            domain: { x: [0, 1], y: [0, 1] },
            title: { text: "Análisis Técnico" },
            delta: { reference: 50 },
            gauge: {
                axis: { range: [null, 100] },
                bar: { color: "#262730" },
                steps: [
                    { range: [0, 30], color: "#ff4444" },
                    { range: [30, 70], color: "#ffaa00" },
                    { range: [70, 100], color: "#00cc44" }
                ],
                threshold: {
                    line: { color: "white", width: 4 },
                    thickness: 0.75,
                    value: score
                }
            }
        }];

        const layout = {
            width: 280,
            height: 200,
            margin: { t: 30, r: 10, l: 10, b: 10 },
            template: 'plotly_dark',
            paper_bgcolor: 'transparent',
            font: { color: "white", family: "Arial", size: 12 }
        };

        Plotly.newPlot('technicalGauge', gaugeData, layout, { displayModeBar: true });

        // Add recommendation text
        const gaugeContainer = document.getElementById('technicalGauge');
        const infoDiv = document.createElement('div');
        infoDiv.innerHTML = `
            <h4>Señal Técnica</h4>
            <div class="status-badge" style="color: ${color}; border-color: ${color};">
                ${recommendation}
            </div>
            <div style="margin-top: 1rem;">
                <strong>Puntuación:</strong> ${score}/100
            </div>
        `;
        gaugeContainer.appendChild(infoDiv);
    }

    updateAnalystOpinion() {
        const current = parseFloat(this.financialMetrics['Current Price']);
        const targetPrice = current * (1.05 + Math.random() * 0.1);
        const upside = ((targetPrice - current) / current) * 100;
        
        const recommendations = ["Compra fuerte", "Compra", "Mantener", "Venta", "Venta fuerte"];
        const weights = [0.3, 0.4, 0.2, 0.08, 0.02];
        const recommendation = this.weightedRandomChoice(recommendations, weights);

        let badgeClass = 'status-positive';
        if (recommendation === 'Mantener') badgeClass = 'status-neutral';
        if (recommendation.includes('Venta')) badgeClass = 'status-negative';

        document.getElementById('analystContent').innerHTML = `
            <div class="status-badge ${badgeClass}">
                ${recommendation}
            </div>
            <h4>Precio Objetivo</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                <div>
                    <strong>Precio objetivo:</strong><br>
                    $${targetPrice.toFixed(2)}
                </div>
                <div>
                    <strong>Al alza:</strong><br>
                    <span style="color: ${upside >= 0 ? '#00cc44' : '#ff4444'}">
                        ${upside >= 0 ? '+' : ''}${upside.toFixed(2)}%
                    </span>
                </div>
            </div>
        `;
    }

    updateInvestmentSummary() {
        const current = parseFloat(this.financialMetrics['Current Price']);
        const fairValue = current * (0.95 + Math.random() * 0.1);
        const percentageDiff = ((current - fairValue) / fairValue) * 100;
        
        let status, recommendation, color;
        if (percentageDiff < -10) {
            status = "Subvalorado";
            recommendation = "Compra fuerte";
            color = "#00cc44";
        } else if (percentageDiff < -5) {
            status = "Algo subvalorado";
            recommendation = "Compra";
            color = "#00cc44";
        } else if (percentageDiff < 5) {
            status = "Valor razonable";
            recommendation = "Mantener";
            color = "#ffaa00";
        } else if (percentageDiff < 10) {
            status = "Algo sobrevalorado";
            recommendation = "Precaución";
            color = "#ff4444";
        } else {
            status = "Sobrevalorado";
            recommendation = "Venta";
            color = "#ff4444";
        }

        document.getElementById('summaryContent').innerHTML = `
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                <div>
                    <strong>Precio Actual:</strong><br>
                    $${current.toFixed(2)}
                </div>
                <div>
                    <strong>Valor Razonable:</strong><br>
                    $${fairValue.toFixed(2)}
                </div>
            </div>
            <div class="status-badge" style="color: ${color}; border-color: ${color};">
                ${recommendation}
            </div>
            <div style="margin-top: 1rem;">
                <strong>Estado:</strong> ${status}
            </div>
            <div style="margin-top: 0.5rem;">
                ${percentageDiff > 0 ? '🔴' : '🟢'} 
                ${percentageDiff > 0 ? 'Sobrevalorado' : 'Subvalorado'} por ${Math.abs(percentageDiff).toFixed(1)}%
            </div>
        `;
    }

    updateCompanyHealth() {
        // Calculate health score based on financial metrics
        let healthScore = Math.floor(Math.random() * 40) + 60; // 60-100 for demo
        
        let status, color;
        if (healthScore >= 80) {
            status = "Excelente";
            color = "#00cc44";
        } else if (healthScore >= 60) {
            status = "Buena";
            color = "#ffaa00";
        } else if (healthScore >= 40) {
            status = "Regular";
            color = "#ff9500";
        } else {
            status = "Preocupante";
            color = "#ff4444";
        }

        document.getElementById('healthContent').innerHTML = `
            <div style="display: grid; grid-template-columns: 3fr 1fr; gap: 1rem; align-items: center; margin-bottom: 1rem;">
                <div>
                    <strong>Estado de Salud de la Empresa</strong>
                    <div class="progress-bar" style="margin-top: 0.5rem;">
                        <div class="progress-fill health" style="width: ${healthScore}%;"></div>
                    </div>
                </div>
                <div>
                    <strong>Salud:</strong><br>
                    ${healthScore}/100
                </div>
            </div>
            <div class="status-badge" style="color: ${color}; border-color: ${color};">
                ${status}
            </div>
        `;
    }

    updateMarketSentiment() {
        const sentiments = ["Bajista", "Neutral", "Alcista"];
        const currentSentiment = sentiments[Math.floor(Math.random() * sentiments.length)];

        document.getElementById('sentimentContent').innerHTML = `
            <div class="sentiment-indicators">
                <div class="sentiment-item ${currentSentiment === 'Bajista' ? 'active bearish' : ''}">
                    <div style="font-size: 2rem;">🐻</div>
                    <div>${currentSentiment === 'Bajista' ? '<strong>Bajista</strong>' : 'Bajista'}</div>
                </div>
                <div class="sentiment-item ${currentSentiment === 'Alcista' ? 'active bullish' : ''}">
                    <div style="font-size: 2rem;">🐂</div>
                    <div>${currentSentiment === 'Alcista' ? '<strong>Alcista</strong>' : 'Alcista'}</div>
                </div>
            </div>
            <div class="status-badge ${currentSentiment === 'Alcista' ? 'status-positive' : currentSentiment === 'Bajista' ? 'status-negative' : 'status-neutral'}" 
                 style="display: block; text-align: center; margin-top: 1rem;">
                ⚖️ Sentimiento actual: <strong>${currentSentiment}</strong>
            </div>
        `;
    }

    updateHistoricalTable() {
        const container = document.getElementById('historicalTable');
        const data = this.historicalData.slice(-50); // Show last 50 days
        
        const table = document.createElement('table');
        table.innerHTML = `
            <thead>
                <tr>
                    <th>Fecha</th>
                    <th>Apertura</th>
                    <th>Máximo</th>
                    <th>Mínimo</th>
                    <th>Cierre</th>
                    <th>Volumen</th>
                </tr>
            </thead>
            <tbody>
                ${data.reverse().map(row => `
                    <tr>
                        <td>${row.date}</td>
                        <td>$${row.open.toFixed(2)}</td>
                        <td>$${row.high.toFixed(2)}</td>
                        <td>$${row.low.toFixed(2)}</td>
                        <td>$${row.close.toFixed(2)}</td>
                        <td>${this.formatNumber(row.volume)}</td>
                    </tr>
                `).join('')}
            </tbody>
        `;
        
        container.innerHTML = '';
        container.appendChild(table);
    }

    exportData(format) {
        const statusEl = document.getElementById('exportStatus');
        
        try {
            let data, filename, mimeType;
            
            if (format === 'csv') {
                data = this.convertToCSV(this.historicalData);
                filename = `${this.currentStock}_data.csv`;
                mimeType = 'text/csv';
            } else {
                data = JSON.stringify({
                    symbol: this.currentStock,
                    metrics: this.financialMetrics,
                    historical: this.historicalData
                }, null, 2);
                filename = `${this.currentStock}_data.json`;
                mimeType = 'application/json';
            }
            
            const blob = new Blob([data], { type: mimeType });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            a.click();
            window.URL.revokeObjectURL(url);
            
            statusEl.className = 'export-status success';
            statusEl.textContent = `✅ Datos exportados exitosamente como ${filename}`;
            
            setTimeout(() => {
                statusEl.textContent = '';
                statusEl.className = 'export-status';
            }, 3000);
            
        } catch (error) {
            statusEl.className = 'export-status error';
            statusEl.textContent = `❌ Error exportando datos: ${error.message}`;
        }
    }

    convertToCSV(data) {
        const headers = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume'];
        const csvContent = [
            headers.join(','),
            ...data.map(row => [
                row.date,
                row.open,
                row.high,
                row.low,
                row.close,
                row.volume
            ].join(','))
        ].join('\n');
        
        return csvContent;
    }

    formatNumber(num) {
        if (num >= 1e12) return (num / 1e12).toFixed(1) + 'T';
        if (num >= 1e9) return (num / 1e9).toFixed(1) + 'B';
        if (num >= 1e6) return (num / 1e6).toFixed(1) + 'M';
        if (num >= 1e3) return (num / 1e3).toFixed(1) + 'K';
        return num.toString();
    }

    weightedRandomChoice(items, weights) {
        const total = weights.reduce((sum, weight) => sum + weight, 0);
        let random = Math.random() * total;
        
        for (let i = 0; i < items.length; i++) {
            if (random < weights[i]) {
                return items[i];
            }
            random -= weights[i];
        }
        
        return items[items.length - 1];
    }

    showLoading(show) {
        const loader = document.getElementById('loadingIndicator');
        loader.classList.toggle('hidden', !show);
    }

    showContent() {
        document.getElementById('contentArea').classList.remove('hidden');
        document.getElementById('stockInfo').classList.remove('hidden');
    }

    showError(message) {
        const errorEl = document.getElementById('errorMessage');
        errorEl.textContent = message;
        errorEl.classList.remove('hidden');
    }

    hideError() {
        document.getElementById('errorMessage').classList.add('hidden');
    }
}

// Initialize the dashboard when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new StockDashboard();
});