# Stock Financial Dashboard

Un dashboard interactivo para análisis de datos financieros de acciones con integración de Yahoo Finance.

## Características

- 📈 **Entrada de símbolos de acciones**: Ingresa cualquier símbolo bursátil (AAPL, GOOGL, MSFT, etc.)
- 📊 **Datos en tiempo real**: Integración con Yahoo Finance para datos financieros actualizados
- 📋 **Métricas financieras**: Tabla completa con ratios P/E, capitalización de mercado, y más
- 📈 **Gráficos interactivos**: Gráficos de líneas y velas japonesas con promedios móviles
- 📥 **Descarga CSV**: Exporta todos los datos como archivos CSV
- 🌙 **Tema oscuro**: Diseño elegante con tema oscuro y acentos verdes
- 📊 **Gráficos de volumen**: Visualización del volumen de trading con indicadores de movimiento de precios

## Instalación

1. Clona este repositorio:
```bash
git clone <tu-repositorio-url>
cd stock-dashboard
```

2. Instala las dependencias:
```bash
pip install streamlit pandas plotly yfinance numpy
```

## Uso

Ejecuta la aplicación:
```bash
streamlit run app.py
```

La aplicación se abrirá en tu navegador en `http://localhost:8501`

## Estructura del Proyecto

```
├── app.py                 # Aplicación principal de Streamlit
├── utils/
│   ├── data_fetcher.py   # Obtención de datos de Yahoo Finance
│   ├── chart_generator.py # Generación de gráficos interactivos
│   └── helpers.py        # Funciones auxiliares y formateo
├── .streamlit/
│   └── config.toml       # Configuración de Streamlit
└── README.md             # Este archivo
```

## Dependencias

- streamlit: Framework de aplicaciones web
- pandas: Manipulación y análisis de datos
- plotly: Visualizaciones interactivas
- yfinance: API de Yahoo Finance
- numpy: Computación numérica

## Licencia

MIT License