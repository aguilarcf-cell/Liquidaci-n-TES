<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Crypto Calc</title>
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="CryptoCalc">
    
    <style>
        :root {
            --bg-color: #0d1117;
            --card-bg: #161b22;
            --text-color: #c9d1d9;
            --accent-green: #238636;
            --accent-red: #da3633;
            --input-bg: #21262d;
            --border-color: #30363d;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 90vh;
        }

        .app-container {
            width: 100%;
            max-width: 375px;
            background-color: var(--card-bg);
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.5);
            border: 1px solid var(--border-color);
            box-sizing: border-box;
        }

        h2 {
            text-align: center;
            margin-top: 0;
            color: #fff;
            font-size: 24px;
        }

        .input-group {
            margin-bottom: 18px;
        }

        label {
            display: block;
            margin-bottom: 6px;
            font-size: 14px;
            color: #8b949e;
        }

        input {
            width: 100%;
            padding: 12px;
            background-color: var(--input-bg);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            color: #fff;
            font-size: 16px;
            box-sizing: border-box;
            -webkit-appearance: none;
        }

        input:focus {
            outline: none;
            border-color: #58a6ff;
        }

        .result-box {
            margin-top: 25px;
            padding: 15px;
            background-color: var(--input-bg);
            border-radius: 12px;
            text-align: center;
            border: 1px solid var(--border-color);
        }

        .result-title {
            font-size: 14px;
            color: #8b949e;
            margin-bottom: 5px;
        }

        .result-value {
            font-size: 28px;
            font-weight: bold;
            transition: color 0.3s ease;
        }

        .result-roi {
            font-size: 16px;
            margin-top: 5px;
            font-weight: 500;
        }
    </style>
</head>
<body>

    <div class="app-container">
        <h2>Crypto Calc 🪙</h2>
        
        <div class="input-group">
            <label for="precioEntrada">Precio de Entrada (USD)</label>
            <input type="number" id="precioEntrada" placeholder="Ej: 2.50" step="any" oninput="calcular()">
        </div>

        <div class="input-group">
            <label for="cantidadTokens">Cantidad de Tokens</label>
            <input type="number" id="cantidadTokens" placeholder="Ej: 50" step="any" oninput="calcular()">
        </div>

        <div class="input-group">
            <label for="precioActual">Precio Actual (USD)</label>
            <input type="number" id="precioActual" placeholder="Ej: 4.00" step="any" oninput="calcular()">
        </div>

        <div class="result-box">
            <div class="result-title">Balance de Utilidad / Pérdida</div>
            <div id="resultado" class="result-value">$0.00</div>
            <div id="roi" class="result-roi">0.00%</div>
        </div>
    </div>

    <script>
        function calcular() {
            const E = parseFloat(document.getElementById('precioEntrada').value);
            const Q = parseFloat(document.getElementById('cantidadTokens').value);
            const A = parseFloat(document.getElementById('precioActual').value);

            const resultadoDiv = document.getElementById('resultado');
            const roiDiv = document.getElementById('roi');

            if (isNaN(E) || isNaN(Q) || isNaN(A) || E <= 0 || Q <= 0) {
                resultadoDiv.innerText = "$0.00";
                resultadoDiv.style.color = "var(--text-color)";
                roiDiv.innerText = "0.00%";
                roiDiv.style.color = "var(--text-color)";
                return;
            }

            // Aquí estaba el error (corregido a una sola palabra unida):
            const utilidadPerdida = Q * (A - E);
            const roi = ((A - E) / E) * 100;

            const formatoMoneda = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(utilidadPerdida);
            const formatoROI = roi.toFixed(2) + "%";

            if (utilidadPerdida >= 0) {
                resultadoDiv.innerText = "+" + formatoMoneda;
                resultadoDiv.style.color = "#34d399"; 
                roiDiv.innerText = "+" + formatoROI;
                roiDiv.style.color = "#34d399";
            } else {
                resultadoDiv.innerText = formatoMoneda;
                resultadoDiv.style.color = "#f87171"; 
                roiDiv.innerText = formatoROI;
                roiDiv.style.color = "#f87171";
            }
        }
    </script>
</body>
</html>
