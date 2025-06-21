<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>José, Andrés, Juacko Investing | Simulación de Trading</title>
    
    <!-- Librería de Gráficos: Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns"></script>

    <!-- Iconos: Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <!-- Estilos CSS -->
    <style>
        :root {
            --bg-dark: #101419;
            --bg-light: #1a2027;
            --text-primary: #e2e8f0;
            --text-secondary: #a0aec0;
            --accent-blue: #3182ce;
            --accent-green: #38a169;
            --accent-red: #e53e3e;
            --accent-purple: #805ad5;
            --border-color: #2d3748;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-primary);
            margin: 0;
            display: flex;
            height: 100vh;
            overflow: hidden;
        }

        /* --- Barra Lateral de Navegación --- */
        .sidebar {
            width: 250px;
            background-color: var(--bg-light);
            border-right: 1px solid var(--border-color);
            padding: 20px;
            display: flex;
            flex-direction: column;
        }
        .sidebar-header {
            text-align: center;
            margin-bottom: 30px;
        }
        .sidebar-header h1 {
            font-size: 1.5em;
            color: var(--text-primary);
            margin: 0;
        }
        .sidebar-header h1 .fa-robot { color: var(--accent-blue); }
        .sidebar-header p {
            font-size: 0.9em;
            color: var(--text-secondary);
        }
        .nav-menu {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        .nav-item a {
            display: flex;
            align-items: center;
            padding: 15px;
            color: var(--text-secondary);
            text-decoration: none;
            border-radius: 8px;
            margin-bottom: 10px;
            transition: background-color 0.2s, color 0.2s;
        }
        .nav-item a:hover {
            background-color: #2d3748;
            color: var(--text-primary);
        }
        .nav-item a.active {
            background-color: var(--accent-blue);
            color: white;
            font-weight: bold;
        }
        .nav-item a i {
            width: 25px;
            margin-right: 15px;
        }

        /* --- Contenido Principal --- */
        .main-content {
            flex-grow: 1;
            padding: 25px;
            overflow-y: auto;
        }
        .view {
            display: none;
        }
        .view.active {
            display: block;
        }

        /* --- Estilos de Componentes Comunes --- */
        .grid-container {
            display: grid;
            gap: 20px;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        }
        .card {
            background-color: var(--bg-light);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
        }
        .card-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }
        .card-header i { margin-right: 10px; color: var(--accent-blue); }
        .card-title { font-size: 1.1em; font-weight: bold; margin: 0; }
        
        /* --- VISTA: DASHBOARD --- */
        #dashboard-view .kpi-card {
            text-align: center;
        }
        .kpi-value {
            font-size: 2em;
            font-weight: bold;
            margin: 5px 0;
        }
        .kpi-value.green { color: var(--accent-green); }
        .kpi-value.red { color: var(--accent-red); }
        .kpi-label { color: var(--text-secondary); font-size: 0.9em; }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background-color: var(--accent-green);
            margin-left: 10px;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(56, 161, 105, 0.7); }
            70% { box-shadow: 0 0 0 10px rgba(56, 161, 105, 0); }
            100% { box-shadow: 0 0 0 0 rgba(56, 161, 105, 0); }
        }

        /* --- VISTA: LIVE BOT --- */
        .flowchart { list-style: none; padding: 0; }
        .flow-step {
            display: flex;
            align-items: center;
            padding: 15px;
            background-color: #2d3748;
            border-radius: 8px;
            margin-bottom: 15px;
            position: relative;
        }
        .flow-step:not(:last-child)::after {
            content: '\f063';
            font-family: 'Font Awesome 6 Free';
            font-weight: 900;
            position: absolute;
            left: 50%;
            bottom: -20px;
            transform: translateX(-50%);
            color: var(--text-secondary);
        }
        .flow-icon { width: 40px; text-align: center; font-size: 1.5em; }
        .flow-text { flex-grow: 1; }
        .flow-status {
            font-weight: bold;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.8em;
        }
        .status-pending { background-color: #4a5568; color: var(--text-primary); }
        .status-running { background-color: var(--accent-blue); color: white; animation: blink 1.5s infinite; }
        .status-complete { background-color: var(--accent-green); color: white; }
        @keyframes blink { 50% { opacity: 0.5; } }
        
        .log-console {
            background-color: #0d0f12;
            height: 250px;
            overflow-y: auto;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', Courier, monospace;
            font-size: 0.9em;
        }
        .log-line { margin-bottom: 5px; }
        .log-time { color: #63b3ed; }
        .log-info { color: var(--text-primary); }
        .log-signal-buy { color: var(--accent-green); font-weight: bold; }
        .log-signal-sell { color: var(--accent-red); font-weight: bold; }
        .log-signal-hold { color: var(--text-secondary); }

        /* --- VISTA: BACKTESTING --- */
        .backtest-form {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            align-items: flex-end;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-size: 0.9em;
            color: var(--text-secondary);
        }
        .form-group select, .form-group input {
            width: 100%;
            padding: 10px;
            background-color: #2d3748;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: var(--text-primary);
        }
        .run-button {
            background-color: var(--accent-green);
            color: white;
            border: none;
            padding: 10px;
            border-radius: 6px;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.2s;
            height: 41px;
        }
        .run-button:hover { background-color: #2f855a; }
        
        .results-container { display: none; margin-top: 20px; }
        .loader {
            text-align: center;
            padding: 50px;
            font-size: 1.2em;
            display: none;
        }
        .loader .fa-spinner {
            font-size: 2em;
            margin-bottom: 15px;
        }

        /* --- VISTA: MODEL HUB --- */
        .model-card {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .model-card p {
            color: var(--text-secondary);
            font-size: 0.9em;
        }

        /* --- TABLAS --- */
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }
        th { font-size: 0.9em; color: var(--text-secondary); }
        td { font-size: 0.95em; }
        .buy-row { border-left: 3px solid var(--accent-green); }
        .sell-row { border-left: 3px solid var(--accent-red); }

    </style>
</head>
<body>

    <!-- ==================== BARRA LATERAL ==================== -->
    <nav class="sidebar">
        <div class="sidebar-header">
            <h1><i class="fas fa-robot"></i> José, Andrés, Juacko Investing AI</h1>
            <p>Panel de Simulación</p>
        </div>
        <ul class="nav-menu">
            <li class="nav-item"><a href="#" class="nav-link active" data-view="dashboard-view"><i class="fas fa-chart-pie"></i> Dashboard</a></li>
            <li class="nav-item"><a href="#" class="nav-link" data-view="live-view"><i class="fas fa-cogs"></i> Ejecución del Bot</a></li>
            <li class="nav-item"><a href="#" class="nav-link" data-view="backtest-view"><i class="fas fa-history"></i> Backtesting</a></li>
            <li class="nav-item"><a href="#" class="nav-link" data-view="models-view"><i class="fas fa-brain"></i> Centro de Modelos</a></li>
        </ul>
    </nav>

    <!-- ==================== CONTENIDO PRINCIPAL ==================== -->
    <main class="main-content">
        
        <!-- ==================== VISTA 1: DASHBOARD ==================== -->
        <div id="dashboard-view" class="view active">
            <h2>Dashboard General</h2>
            <div class="grid-container" style="grid-template-columns: repeat(4, 1fr);">
                <div class="card kpi-card">
                    <p class="kpi-label">Estado del Bot</p>
                    <p class="kpi-value green">OPERACIONAL <span class="status-indicator"></span></p>
                </div>
                <div class="card kpi-card">
                    <p class="kpi-label">Sharpe Ratio (30d)</p>
                    <p class="kpi-value green" id="kpi-sharpe">2.15</p>
                </div>
                <div class="card kpi-card">
                    <p class="kpi-label">Win Rate (30d)</p>
                    <p class="kpi-value green" id="kpi-winrate">68%</p>
                </div>
                <div class="card kpi-card">
                    <p class="kpi-label">PnL (24h)</p>
                    <p class="kpi-value red" id="kpi-pnl">-$245.80</p>
                </div>
            </div>
            
            <div class="card" style="margin-top: 20px;">
                <div class="card-header">
                    <i class="fas fa-chart-line"></i>
                    <h3 class="card-title">Evolución del Capital vs. BTC/USDT (Simulado)</h3>
                </div>
                <canvas id="equityChart"></canvas>
            </div>
            
            <div class="card" style="margin-top: 20px;">
                <div class="card-header">
                     <i class="fas fa-exchange-alt"></i>
                     <h3 class="card-title">Últimas 5 Operaciones (Simuladas)</h3>
                </div>
                <table>
                    <thead>
                        <tr><th>Activo</th><th>Tipo</th><th>Precio Entrada</th><th>Cantidad</th><th>PnL</th><th>Fecha</th></tr>
                    </thead>
                    <tbody>
                        <tr class="buy-row"><td>BTC/USDT</td><td>COMPRA</td><td>$68,540.12</td><td>0.05</td><td class="green">+$120.30</td><td>...hace 2 horas</td></tr>
                        <tr class="sell-row"><td>ETH/USDT</td><td>VENTA</td><td>$3,805.50</td><td>0.5</td><td class="green">+$95.10</td><td>...hace 8 horas</td></tr>
                        <tr class="sell-row"><td>BTC/USDT</td><td>VENTA</td><td>$69,110.00</td><td>0.1</td><td class="red">-$250.00</td><td>...hace 15 horas</td></tr>
                        <tr class="buy-row"><td>SOL/USDT</td><td>COMPRA</td><td>$165.20</td><td>10</td><td class="green">+$35.70</td><td>...hace 1 día</td></tr>
                        <tr class="buy-row"><td>BTC/USDT</td><td>COMPRA</td><td>$67,800.00</td><td>0.1</td><td class="green">+$87.55</td><td>...hace 1 día</td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- ==================== VISTA 2: EJECUCIÓN DEL BOT ==================== -->
        <div id="live-view" class="view">
            <h2>Flujo de Ejecución del Bot en Tiempo Real (Simulado)</h2>
            <div class="grid-container" style="grid-template-columns: 1fr 1.5fr;">
                <div class="card">
                     <div class="card-header">
                        <i class="fas fa-project-diagram"></i>
                        <h3 class="card-title">Paso a Paso del Ciclo de Decisión</h3>
                    </div>
                    <ul class="flowchart">
                        <li id="flow-step-1" class="flow-step">
                            <i class="fas fa-download flow-icon"></i>
                            <div class="flow-text">1. Ingesta de Datos (Binance API)</div>
                            <div class="flow-status status-pending">PENDIENTE</div>
                        </li>
                         <li id="flow-step-2" class="flow-step">
                            <i class="fas fa-calculator flow-icon"></i>
                            <div class="flow-text">2. Feature Engineering</div>
                            <div class="flow-status status-pending">PENDIENTE</div>
                        </li>
                         <li id="flow-step-3" class="flow-step">
                            <i class="fas fa-brain flow-icon"></i>
                            <div class="flow-text">3. Inferencia del Modelo (LSTM)</div>
                            <div class="flow-status status-pending">PENDIENTE</div>
                        </li>
                         <li id="flow-step-4" class="flow-step">
                            <i class="fas fa-shield-alt flow-icon"></i>
                            <div class="flow-text">4. Chequeo de Gestión de Riesgo</div>
                            <div class="flow-status status-pending">PENDIENTE</div>
                        </li>
                        <li id="flow-step-5" class="flow-step">
                            <i class="fas fa-flag-checkered flow-icon"></i>
                            <div class="flow-text">5. Ejecución de Orden</div>
                            <div class="flow-status status-pending">PENDIENTE</div>
                        </li>
                    </ul>
                </div>
                <div class="card">
                    <div class="card-header">
                        <i class="fas fa-terminal"></i>
                        <h3 class="card-title">Consola de Decisión en Vivo</h3>
                    </div>
                    <div id="log-console" class="log-console">
                        <div class="log-line"><span class="log-time">[--:--:--]</span> <span class="log-info">Iniciando simulación de ciclo de decisión...</span></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ==================== VISTA 3: BACKTESTING ==================== -->
        <div id="backtest-view" class="view">
            <h2>Simulador de Backtesting</h2>
            <div class="card">
                <div class="card-header">
                    <i class="fas fa-sliders-h"></i>
                    <h3 class="card-title">Configurar Simulación</h3>
                </div>
                <div class="backtest-form">
                    <div class="form-group">
                        <label for="asset">Activo</label>
                        <select id="asset">
                            <option>BTC/USDT</option>
                            <option>ETH/USDT</option>
                            <option>SOL/USDT</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="model">Modelo</label>
                        <select id="model">
                            <option>LSTM (Equilibrado)</option>
                            <option>Transformer (Largo Plazo)</option>
                            <option>XGBoost (Alta Frecuencia)</option>
                        </select>
                    </div>
                     <div class="form-group">
                        <label for="start-date">Fecha Inicio</label>
                        <input type="date" id="start-date" value="2023-01-01">
                    </div>
                     <div class="form-group">
                        <label for="end-date">Fecha Fin</label>
                        <input type="date" id="end-date" value="2023-12-31">
                    </div>
                    <button id="run-backtest-btn" class="run-button"><i class="fas fa-play"></i> Ejecutar</button>
                </div>
            </div>
            
            <div id="backtest-loader" class="loader">
                <i class="fas fa-spinner fa-spin"></i>
                <p>Ejecutando backtest... Esto puede tomar un momento.</p>
            </div>

            <div id="backtest-results" class="results-container">
                 <div class="card" style="margin-top: 20px;">
                    <div class="card-header">
                        <i class="fas fa-poll"></i>
                        <h3 class="card-title">Resultados del Backtest</h3>
                    </div>
                    <div class="grid-container" style="grid-template-columns: repeat(5, 1fr);">
                        <div class="kpi-card"><p class="kpi-label">Retorno Total</p><p id="res-return" class="kpi-value green">+124.5%</p></div>
                        <div class="kpi-card"><p class="kpi-label">Sharpe Ratio</p><p id="res-sharpe" class="kpi-value green">2.31</p></div>
                        <div class="kpi-card"><p class="kpi-label">Max Drawdown</p><p id="res-drawdown" class="kpi-value red">-11.8%</p></div>
                        <div class="kpi-card"><p class="kpi-label">Win Rate</p><p id="res-winrate" class="kpi-value green">71%</p></div>
                        <div class="kpi-card"><p class="kpi-label">Nº de Trades</p><p id="res-trades" class="kpi-value">258</p></div>
                    </div>
                    <canvas id="backtestChart" style="margin-top: 20px;"></canvas>
                </div>
            </div>
        </div>
        
        <!-- ==================== VISTA 4: CENTRO DE MODELOS ==================== -->
        <div id="models-view" class="view">
            <h2>Centro de Modelos Predictivos</h2>
            <div class="grid-container" style="grid-template-columns: repeat(3, 1fr);">
                <!-- Card XGBoost -->
                <div class="card model-card">
                    <div>
                        <div class="card-header">
                            <i class="fas fa-table" style="color:#38a169;"></i>
                            <h3 class="card-title">XGBoost</h3>
                        </div>
                        <p>Ideal para datos tabulares y alta frecuencia. Captura interacciones complejas entre cientos de indicadores. Rápido de entrenar.</p>
                        <ul>
                            <li><strong>Precisión:</strong> 75%</li>
                            <li><strong>Mejor Uso:</strong> Scalping (1m-5m)</li>
                        </ul>
                    </div>
                    <canvas id="xgboostChart"></canvas>
                </div>
                <!-- Card LSTM -->
                <div class="card model-card">
                    <div>
                        <div class="card-header">
                            <i class="fas fa-memory" style="color:#805ad5;"></i>
                            <h3 class="card-title">LSTM</h3>
                        </div>
                        <p>Red neuronal recurrente con memoria. Excelente para aprender patrones en secuencias de tiempo (ej. tendencias, reversiones a la media).</p>
                        <ul>
                            <li><strong>Precisión:</strong> 82%</li>
                            <li><strong>Mejor Uso:</strong> Swing Trading (1h-4h)</li>
                        </ul>
                    </div>
                    <canvas id="lstmChart"></canvas>
                </div>
                <!-- Card Transformer -->
                <div class="card model-card">
                    <div>
                        <div class="card-header">
                            <i class="fas fa-atom" style="color:#e53e3e;"></i>
                            <h3 class="card-title">Transformer</h3>
                        </div>
                        <p>Arquitectura de vanguardia. Analiza la relación entre todos los puntos de la secuencia a la vez, ideal para dependencias a largo plazo.</p>
                         <ul>
                            <li><strong>Precisión:</strong> 78%</li>
                            <li><strong>Mejor Uso:</strong> Position Trading (1d+)</li>
                        </ul>
                    </div>
                    <canvas id="transformerChart"></canvas>
                </div>
            </div>
        </div>

    </main>

    <!-- ==================== JAVASCRIPT para la Dinámica ==================== -->
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const navLinks = document.querySelectorAll('.nav-link');
        const views = document.querySelectorAll('.view');

        // --- NAVEGACIÓN ENTRE VISTAS ---
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                
                navLinks.forEach(l => l.classList.remove('active'));
                views.forEach(v => v.classList.remove('active'));

                link.classList.add('active');
                const viewId = link.getAttribute('data-view');
                document.getElementById(viewId).classList.add('active');
            });
        });

        // --- SIMULACIÓN VISTA DASHBOARD ---
        const equityCtx = document.getElementById('equityChart').getContext('2d');
        const equityChart = new Chart(equityCtx, {
            type: 'line',
            data: {
                labels: Array.from({length: 50}, (_, i) => new Date().getTime() - (50-i)*3600*1000),
                datasets: [{
                    label: 'Capital del Bot',
                    data: Array.from({length: 50}, () => 10000 + Math.random() * 2000),
                    borderColor: 'var(--accent-blue)',
                    backgroundColor: 'rgba(49, 130, 206, 0.1)',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 0,
                }, {
                    label: 'Precio BTC/USDT',
                    data: Array.from({length: 50}, () => 65000 + Math.random() * 5000),
                    borderColor: 'var(--text-secondary)',
                    borderDash: [5, 5],
                    fill: false,
                    tension: 0.3,
                    pointRadius: 0,
                }]
            },
            options: {
                scales: {
                    x: { type: 'time', time: { unit: 'hour' }, grid: { color: 'rgba(255,255,255,0.1)' } },
                    y: { grid: { color: 'rgba(255,255,255,0.1)' } }
                }
            }
        });
        // Simular actualización del gráfico
        setInterval(() => {
            equityChart.data.labels.push(new Date().getTime());
            equityChart.data.labels.shift();
            equityChart.data.datasets[0].data.push(equityChart.data.datasets[0].data[49] + (Math.random()-0.48) * 100);
            equityChart.data.datasets[0].data.shift();
             equityChart.data.datasets[1].data.push(equityChart.data.datasets[1].data[49] + (Math.random()-0.5) * 500);
            equityChart.data.datasets[1].data.shift();
            equityChart.update('quiet');
            
            // Actualizar KPIs
            document.getElementById('kpi-pnl').textContent = `${(Math.random() > 0.5 ? '+' : '-')}${(Math.random()*300).toFixed(2)}`;
            document.getElementById('kpi-pnl').classList.toggle('green', document.getElementById('kpi-pnl').textContent.startsWith('+'));
            document.getElementById('kpi-pnl').classList.toggle('red', !document.getElementById('kpi-pnl').textContent.startsWith('+'));

        }, 2000);


        // --- SIMULACIÓN VISTA LIVE BOT ---
        const flowSteps = document.querySelectorAll('.flow-step .flow-status');
        const logConsole = document.getElementById('log-console');
        let currentStep = 0;
        const logMessages = [
            "Consultando API de Binance para nuevos datos OHLCV...",
            "Calculando 78 features (ATR, RSI, CMF, Skew...)",
            "Enviando tensor [1, 60, 78] al modelo LSTM...",
            "Predicción: SUBIDA (Confianza: 87%). Volatilidad: MEDIA.",
            "Riesgo aceptado. Enviando orden de COMPRA para 0.05 BTC."
        ];
        
        function runBotCycle() {
            if (currentStep >= flowSteps.length) {
                currentStep = 0;
                flowSteps.forEach(s => s.className = 'flow-status status-pending');
                logConsole.innerHTML += `<div class="log-line"><span class="log-time">[${new Date().toLocaleTimeString()}]</span> <span class="log-info" style="color:var(--accent-blue)">--- CICLO COMPLETADO. ESPERANDO PRÓXIMA VELA ---</span></div>`;
                logConsole.scrollTop = logConsole.scrollHeight;
                setTimeout(runBotCycle, 5000);
                return;
            }

            if(currentStep > 0) flowSteps[currentStep-1].className = 'flow-status status-complete';
            flowSteps[currentStep].className = 'flow-status status-running';
            
            let signalClass = 'log-info';
            if(currentStep === 4){
                const signals = ['log-signal-buy', 'log-signal-sell', 'log-signal-hold'];
                signalClass = signals[Math.floor(Math.random()*signals.length)];
            }
            
            logConsole.innerHTML += `<div class="log-line"><span class="log-time">[${new Date().toLocaleTimeString()}]</span> <span class="${signalClass}">${logMessages[currentStep]}</span></div>`;
            logConsole.scrollTop = logConsole.scrollHeight;


            currentStep++;
            setTimeout(runBotCycle, 1500 + Math.random()*500);
        }
        setTimeout(runBotCycle, 1000);

        // --- SIMULACIÓN VISTA BACKTESTING ---
        const runBtn = document.getElementById('run-backtest-btn');
        const loader = document.getElementById('backtest-loader');
        const resultsContainer = document.getElementById('backtest-results');

        let backtestChartInstance;

        runBtn.addEventListener('click', () => {
            resultsContainer.style.display = 'none';
            loader.style.display = 'block';

            setTimeout(() => {
                loader.style.display = 'none';
                resultsContainer.style.display = 'block';

                // Simular resultados
                document.getElementById('res-return').textContent = `+${(Math.random()*150 + 20).toFixed(1)}%`;
                document.getElementById('res-sharpe').textContent = (Math.random()*1.5 + 1).toFixed(2);
                document.getElementById('res-drawdown').textContent = `-${(Math.random()*10 + 8).toFixed(1)}%`;
                document.getElementById('res-winrate').textContent = `${Math.floor(Math.random()*20 + 55)}%`;
                document.getElementById('res-trades').textContent = Math.floor(Math.random()*200 + 100);

                // Actualizar gráfico de backtest
                const backtestCtx = document.getElementById('backtestChart').getContext('2d');
                if(backtestChartInstance) backtestChartInstance.destroy();
                backtestChartInstance = new Chart(backtestCtx, {
                    type: 'line',
                    data: {
                        labels: Array.from({length: 100}, (_, i) => `Day ${i}`),
                        datasets: [{
                            label: 'Equity Curve',
                            data: Array.from({length: 100}, (_, i) => 10000 * Math.pow(1.01, i) + (Math.random()-0.5)*i*150),
                            borderColor: 'var(--accent-green)',
                            fill: false
                        }]
                    },
                     options: { scales: { y: { beginAtZero: false } } }
                });

            }, 2500);
        });

        // --- GRÁFICOS VISTA MODEL HUB ---
        // Chart XGBoost
        new Chart(document.getElementById('xgboostChart').getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['ATR', 'Volume', 'CMF', 'RSI', 'Momentum'],
                datasets: [{
                    label: 'Importancia de Features',
                    data: [35, 28, 22, 18, 15],
                    backgroundColor: 'var(--accent-green)'
                }]
            },
            options: { indexAxis: 'y', responsive: true, plugins: { legend: { display: false } } }
        });

        // Chart LSTM
        new Chart(document.getElementById('lstmChart').getContext('2d'), {
            type: 'line',
            data: {
                labels: Array.from({length: 20}, (_, i) => `t-${20-i}`),
                datasets: [
                    { label: 'Precio Real', data: Array.from({length: 20}, () => 100 + Math.random()*5), borderColor: 'var(--text-secondary)' },
                    { label: 'Predicción LSTM', data: Array.from({length: 20}, () => 100 + Math.random()*5), borderColor: 'var(--accent-purple)' }
                ]
            },
            options: { responsive: true, plugins: { legend: { position: 'bottom' } } }
        });
        
        // Chart Transformer
         new Chart(document.getElementById('transformerChart').getContext('2d'), {
            type: 'line',
            data: {
                labels: Array.from({length: 20}, (_, i) => `t-${20-i}`),
                datasets: [
                    { label: 'Precio Real', data: Array.from({length: 20}, () => 100 + Math.random()*5), borderColor: 'var(--text-secondary)' },
                    { label: 'Predicción Transformer', data: Array.from({length: 20}, () => 100 + Math.random()*5), borderColor: 'var(--accent-red)' }
                ]
            },
            options: { responsive: true, plugins: { legend: { position: 'bottom' } } }
        });


    });
    </script>
</body>
</html>
