import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
from io import BytesIO

from utils.data_fetcher import StockDataFetcher
from utils.chart_generator import ChartGenerator
from utils.helpers import format_currency, format_percentage, validate_symbol

# Configure page
st.set_page_config(
    page_title="Stock Financial Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'stock_data' not in st.session_state:
    st.session_state.stock_data = None
if 'current_symbol' not in st.session_state:
    st.session_state.current_symbol = ""

def main():
    st.title("📈 Stock Financial Dashboard")
    st.markdown("---")
    
    # Sidebar for stock input and settings
    with st.sidebar:
        st.header("Stock Selection")
        
        # Stock symbol input
        symbol_input = st.text_input(
            "Ingresa Símbolo de Acción",
            value="AAPL",
            placeholder="ej., AAPL, GOOGL, MSFT",
            help="Ingresa un símbolo bursátil válido"
        ).upper().strip()
        
        # Time period selection
        time_period = st.selectbox(
            "Seleccionar Período",
            options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
            index=3,
            help="Período de datos históricos"
        )
        
        # Chart type selection
        chart_type = st.selectbox(
            "Tipo de Gráfico",
            options=["Gráfico de Línea", "Gráfico de Velas"],
            index=0
        )
        
        # Fetch data button
        fetch_button = st.button("📊 Obtener Datos", type="primary", use_container_width=True)
    
    # Main content area
    if fetch_button or (symbol_input and symbol_input != st.session_state.current_symbol):
        if validate_symbol(symbol_input):
            with st.spinner(f"Fetching data for {symbol_input}..."):
                try:
                    # Initialize data fetcher
                    data_fetcher = StockDataFetcher(symbol_input)
                    
                    # Fetch all required data
                    stock_info = data_fetcher.get_stock_info()
                    historical_data = data_fetcher.get_historical_data(time_period)
                    financial_metrics = data_fetcher.get_financial_metrics()
                    
                    if historical_data is not None and not historical_data.empty:
                        st.session_state.stock_data = {
                            'symbol': symbol_input,
                            'info': stock_info,
                            'historical': historical_data,
                            'metrics': financial_metrics,
                            'time_period': time_period
                        }
                        st.session_state.current_symbol = symbol_input
                        st.success(f"✅ Successfully loaded data for {symbol_input}")
                    else:
                        st.error(f"❌ No data found for symbol: {symbol_input}")
                        
                except Exception as e:
                    st.error(f"❌ Error fetching data: {str(e)}")
        else:
            st.error("❌ Please enter a valid stock symbol")
    
    # Display data if available
    if st.session_state.stock_data:
        display_dashboard(chart_type)
    else:
        # Welcome message
        st.info("👆 Ingresa un símbolo de acción en la barra lateral para comenzar!")
        
        # Sample symbols suggestion
        st.markdown("### Acciones Populares para Probar:")
        st.markdown("**Haz clic en cualquier botón para cargar datos instantáneamente:**")
        col1, col2, col3, col4 = st.columns(4)
        
        sample_stocks = [
            ("AAPL", "Apple Inc."),
            ("GOOGL", "Alphabet Inc."),
            ("MSFT", "Microsoft Corp."),
            ("TSLA", "Tesla Inc.")
        ]
        
        for i, (symbol, name) in enumerate(sample_stocks):
            with [col1, col2, col3, col4][i]:
                if st.button(f"{symbol}\n{name}", key=f"sample_{symbol}"):
                    # Force fetch new data when sample button is clicked
                    with st.spinner(f"Cargando datos para {symbol}..."):
                        try:
                            data_fetcher = StockDataFetcher(symbol)
                            stock_info = data_fetcher.get_stock_info()
                            historical_data = data_fetcher.get_historical_data("1y")
                            financial_metrics = data_fetcher.get_financial_metrics()
                            
                            if historical_data is not None and not historical_data.empty:
                                st.session_state.stock_data = {
                                    'symbol': symbol,
                                    'info': stock_info,
                                    'historical': historical_data,
                                    'metrics': financial_metrics,
                                    'time_period': "1y"
                                }
                                st.session_state.current_symbol = symbol
                                st.success(f"✅ Datos cargados exitosamente para {symbol}")
                                st.rerun()
                            else:
                                st.error(f"❌ No se pudieron cargar los datos para {symbol}")
                        except Exception as e:
                            st.error(f"❌ Error cargando {symbol}: {str(e)}")

def display_dashboard(chart_type):
    data = st.session_state.stock_data
    symbol = data['symbol']
    stock_info = data['info']
    historical_data = data['historical']
    metrics = data['metrics']
    
    # Company header
    st.header(f"{stock_info.get('longName', symbol)} ({symbol})")
    
    # Key metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    current_price = historical_data['Close'].iloc[-1] if not historical_data.empty else 0
    price_change = historical_data['Close'].iloc[-1] - historical_data['Close'].iloc[-2] if len(historical_data) > 1 else 0
    price_change_pct = (price_change / historical_data['Close'].iloc[-2] * 100) if len(historical_data) > 1 and historical_data['Close'].iloc[-2] != 0 else 0
    
    with col1:
        st.metric(
            "Current Price",
            format_currency(current_price),
            f"{format_currency(price_change)} ({format_percentage(price_change_pct)})"
        )
    
    with col2:
        st.metric(
            "Market Cap",
            format_currency(stock_info.get('marketCap', 0), short=True),
            help="Total market value of company's shares"
        )
    
    with col3:
        st.metric(
            "P/E Ratio",
            f"{stock_info.get('trailingPE', 'N/A'):.2f}" if stock_info.get('trailingPE') else "N/A",
            help="Price-to-Earnings ratio"
        )
    
    with col4:
        st.metric(
            "52W High",
            format_currency(stock_info.get('fiftyTwoWeekHigh', 0)),
            help="52-week high price"
        )
    
    with col5:
        st.metric(
            "52W Low",
            format_currency(stock_info.get('fiftyTwoWeekLow', 0)),
            help="52-week low price"
        )
    
    st.markdown("---")
    
    # Charts section
    st.subheader("📊 Price Chart")
    
    # Generate and display chart
    chart_generator = ChartGenerator(historical_data, symbol)
    
    if chart_type == "Gráfico de Velas":
        fig = chart_generator.create_candlestick_chart()
    else:
        fig = chart_generator.create_line_chart()
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Volume chart
    st.subheader("📈 Volume Chart")
    volume_fig = chart_generator.create_volume_chart()
    st.plotly_chart(volume_fig, use_container_width=True)
    
    # Financial data table and CSV download
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📋 Financial Metrics")
    
    with col2:
        # CSV download button
        try:
            csv_data = prepare_csv_data(historical_data, metrics, stock_info)
            if not csv_data.empty:
                csv_string = csv_data.to_csv(index=True)
                
                st.download_button(
                    label="📥 Descargar CSV",
                    data=csv_string.encode('utf-8'),
                    file_name=f"{symbol}_datos_financieros_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    type="primary",
                    key=f"download_csv_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                )
            else:
                st.warning("No hay datos disponibles para descargar")
        except Exception as e:
            st.error(f"Error preparando descarga: {str(e)}")
    
    # Display financial metrics table
    display_financial_table(metrics, stock_info)
    
    # Historical data table
    st.subheader("📊 Historical Price Data")
    
    # Format historical data for display
    display_data = historical_data.copy()
    display_data.index = display_data.index.strftime('%Y-%m-%d')
    
    # Round numerical columns
    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in numeric_columns:
        if col in display_data.columns:
            if col == 'Volume':
                display_data[col] = display_data[col].apply(lambda x: f"{x:,.0f}")
            else:
                display_data[col] = display_data[col].apply(lambda x: f"${x:.2f}")
    
    st.dataframe(display_data, use_container_width=True)

def display_financial_table(metrics, stock_info):
    """Display financial metrics in a formatted table"""
    
    # Prepare financial data
    financial_data = []
    
    # Basic metrics
    basic_metrics = [
        ("Market Cap", format_currency(stock_info.get('marketCap', 0), short=True)),
        ("Enterprise Value", format_currency(stock_info.get('enterpriseValue', 0), short=True)),
        ("P/E Ratio", f"{stock_info.get('trailingPE', 'N/A'):.2f}" if stock_info.get('trailingPE') else "N/A"),
        ("Forward P/E", f"{stock_info.get('forwardPE', 'N/A'):.2f}" if stock_info.get('forwardPE') else "N/A"),
        ("PEG Ratio", f"{stock_info.get('pegRatio', 'N/A'):.2f}" if stock_info.get('pegRatio') else "N/A"),
        ("Price to Book", f"{stock_info.get('priceToBook', 'N/A'):.2f}" if stock_info.get('priceToBook') else "N/A"),
        ("Price to Sales", f"{stock_info.get('priceToSalesTrailing12Months', 'N/A'):.2f}" if stock_info.get('priceToSalesTrailing12Months') else "N/A"),
        ("Dividend Yield", format_percentage(stock_info.get('dividendYield', 0) * 100) if stock_info.get('dividendYield') else "N/A"),
        ("Beta", f"{stock_info.get('beta', 'N/A'):.2f}" if stock_info.get('beta') else "N/A"),
        ("52W High", format_currency(stock_info.get('fiftyTwoWeekHigh', 0))),
        ("52W Low", format_currency(stock_info.get('fiftyTwoWeekLow', 0))),
        ("Shares Outstanding", f"{stock_info.get('sharesOutstanding', 0):,.0f}" if stock_info.get('sharesOutstanding') else "N/A"),
        ("Float", f"{stock_info.get('floatShares', 0):,.0f}" if stock_info.get('floatShares') else "N/A"),
        ("Revenue", format_currency(stock_info.get('totalRevenue', 0), short=True)),
        ("Gross Profit", format_currency(stock_info.get('grossProfits', 0), short=True)),
        ("EBITDA", format_currency(stock_info.get('ebitda', 0), short=True)),
        ("Net Income", format_currency(stock_info.get('netIncomeToCommon', 0), short=True)),
        ("Total Cash", format_currency(stock_info.get('totalCash', 0), short=True)),
        ("Total Debt", format_currency(stock_info.get('totalDebt', 0), short=True)),
        ("Return on Equity", format_percentage(stock_info.get('returnOnEquity', 0) * 100) if stock_info.get('returnOnEquity') else "N/A"),
        ("Return on Assets", format_percentage(stock_info.get('returnOnAssets', 0) * 100) if stock_info.get('returnOnAssets') else "N/A"),
        ("Profit Margins", format_percentage(stock_info.get('profitMargins', 0) * 100) if stock_info.get('profitMargins') else "N/A"),
        ("Operating Margins", format_percentage(stock_info.get('operatingMargins', 0) * 100) if stock_info.get('operatingMargins') else "N/A"),
    ]
    
    # Create DataFrame for display
    df = pd.DataFrame(basic_metrics, columns=['Metric', 'Value'])
    
    # Display in two columns
    col1, col2 = st.columns(2)
    
    mid_point = len(df) // 2
    
    with col1:
        st.dataframe(df.iloc[:mid_point], hide_index=True, use_container_width=True)
    
    with col2:
        st.dataframe(df.iloc[mid_point:], hide_index=True, use_container_width=True)

def prepare_csv_data(historical_data, metrics, stock_info):
    """Prepare comprehensive data for CSV export"""
    
    if historical_data is None or historical_data.empty:
        return pd.DataFrame()
    
    # Start with historical data
    csv_data = historical_data.copy()
    
    # Add calculated fields
    try:
        csv_data['Daily_Return'] = csv_data['Close'].pct_change()
        csv_data['Cumulative_Return'] = (1 + csv_data['Daily_Return']).cumprod() - 1
        csv_data['Price_Change'] = csv_data['Close'].diff()
        csv_data['High_Low_Spread'] = csv_data['High'] - csv_data['Low']
        
        # Add moving averages if enough data
        if len(csv_data) >= 20:
            csv_data['SMA_20'] = csv_data['Close'].rolling(window=20).mean()
        if len(csv_data) >= 50:
            csv_data['SMA_50'] = csv_data['Close'].rolling(window=50).mean()
            
    except Exception as e:
        st.warning(f"Error añadiendo campos calculados: {str(e)}")
    
    return csv_data

if __name__ == "__main__":
    main()
