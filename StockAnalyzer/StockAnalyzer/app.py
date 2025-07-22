import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# Import custom utilities
from utils.data_fetcher import StockDataFetcher
from utils.chart_generator import ChartGenerator
from utils.helpers import DataFormatter
from utils.investment_analysis import InvestmentAnalysis

# Page configuration
st.set_page_config(
    page_title="Stock Financial Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# TradingView-style CSS for professional trading interface
st.markdown("""
<style>
    /* TradingView color scheme: Blue (#2962ff) for bullish, Red (#f7525f) for bearish */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #2962ff, #1e4bff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-card {
        background: transparent;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 3px solid #2962ff;
        margin: 1rem 0;
        box-shadow: none;
        transition: all 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(41, 98, 255, 0.3);
        border-left-color: #2962ff;
    }
    
    .price-change-positive {
        color: #2962ff;
        font-weight: bold;
    }
    
    .price-change-negative {
        color: #f7525f;
        font-weight: bold;
    }
    
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2962ff;
        margin-bottom: 1rem;
    }
    
    .investment-card {
        background: transparent;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #363a45;
        box-shadow: none;
    }
    
    .status-badge {
        padding: 0.5rem 1rem;
        border-radius: 16px;
        font-weight: bold;
        text-align: center;
        margin: 0.5rem 0;
        display: inline-block;
        font-size: 0.9rem;
    }
    
    .status-positive {
        background-color: rgba(41, 98, 255, 0.15);
        color: #2962ff;
        border: 1px solid rgba(41, 98, 255, 0.3);
    }
    
    .status-neutral {
        background-color: rgba(183, 189, 198, 0.15);
        color: #b7bdc6;
        border: 1px solid rgba(183, 189, 198, 0.3);
    }
    
    .status-negative {
        background-color: rgba(247, 82, 95, 0.15);
        color: #f7525f;
        border: 1px solid rgba(247, 82, 95, 0.3);
    }
    
    .progress-container {
        background: transparent;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #363a45;
    }
    
    .analyst-recommendation {
        background: linear-gradient(45deg, #2962ff, #1e4bff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.3rem;
        font-weight: bold;
        text-align: center;
        margin: 1rem 0;
    }
    
    .tab-content {
        padding: 1rem;
        border-radius: 8px;
        background: transparent;
        margin-top: 1rem;
        border: none;
    }
    
    /* TradingView-style background */
    .stApp {
        background: linear-gradient(180deg, #0d1017 0%, #161b22 100%);
    }
    
    /* Enhanced dataframe styling */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        background-color: #1e222d;
    }
    
    /* Professional button styling - TradingView style */
    .stButton > button {
        border-radius: 6px;
        border: 1px solid #2962ff;
        background-color: transparent;
        color: #2962ff;
        transition: all 0.2s ease;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background-color: #2962ff;
        color: #ffffff;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(41, 98, 255, 0.4);
    }
    
    /* Enhanced metrics - TradingView style */
    [data-testid="metric-container"] {
        background: transparent;
        border: 1px solid #363a45;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: none;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #d1d4dc;
        font-weight: 600;
    }
    
    [data-testid="metric-container"] [data-testid="metric-delta"] {
        font-weight: 500;
    }
    
    /* Professional selectbox */
    .stSelectbox > div > div {
        border-radius: 6px;
        border-color: #363a45;
        background-color: #1e222d;
    }
    
    /* Enhanced text input */
    .stTextInput > div > div > input {
        border-radius: 6px;
        border-color: #363a45;
        background-color: #1e222d;
        color: #d1d4dc;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1e222d;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #1e222d;
        border-radius: 8px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: 500;
        color: #b7bdc6;
        background-color: transparent;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2962ff;
        color: #ffffff;
    }
    
    /* Progress bar styling */
    .stProgress .st-bo {
        background-color: #363a45;
    }
    
    .stProgress .st-bp {
        background-color: #2962ff;
    }
    
    /* Sidebar elements */
    .css-17eq0hr {
        background-color: #1e222d;
    }
    
    /* Main content area */
    .main .block-container {
        background-color: transparent;
        padding-top: 2rem;
    }
    
    /* Chart containers */
    .js-plotly-plot {
        border-radius: 8px;
        background-color: #1e222d;
    }
    
    /* Info boxes */
    .stInfo {
        background-color: rgba(41, 98, 255, 0.1);
        border: 1px solid rgba(41, 98, 255, 0.2);
        border-radius: 8px;
        color: #d1d4dc;
    }
    
    /* Error boxes */
    .stError {
        background-color: rgba(247, 82, 95, 0.1);
        border: 1px solid rgba(247, 82, 95, 0.2);
        border-radius: 8px;
        color: #f7525f;
    }
    
    /* Success boxes */
    .stSuccess {
        background-color: rgba(41, 98, 255, 0.1);
        border: 1px solid rgba(41, 98, 255, 0.2);
        border-radius: 8px;
        color: #2962ff;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Header with icon
    st.title("💹 Stock Financial Dashboard")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("🔍 Análisis de Acciones")
        
        # Stock symbol input
        col1, col2 = st.columns([3, 1])
        with col1:
            symbol = st.text_input(
                "Enter Stock Symbol",
                value="AAPL",
                placeholder="e.g., AAPL, GOOGL, MSFT",
                help="Enter a valid stock ticker symbol"
            ).upper()
        
        with col2:
            st.write("")
            search_button = st.button("🔎", help="Search stock")
        
        # Popular symbols
        st.markdown("**Popular Symbols:**")
        popular_symbols = DataFormatter.get_popular_symbols()
        selected_symbol = st.selectbox(
            "Select from popular stocks",
            options=[""] + popular_symbols,
            format_func=lambda x: "Choose a symbol..." if x == "" else x
        )
        
        if selected_symbol:
            symbol = selected_symbol
        
        # Time period selection
        st.markdown("---")
        st.markdown("**📅 Time Period:**")
        period = st.selectbox(
            "Select time period",
            options=["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y"],
            index=5,  # Default to 1y
            format_func=lambda x: {
                "1d": "1 Day",
                "5d": "5 Days", 
                "1mo": "1 Month",
                "3mo": "3 Months",
                "6mo": "6 Months",
                "1y": "1 Year",
                "2y": "2 Years",
                "5y": "5 Years"
            }[x]
        )
        
        # Chart type selection
        st.markdown("**📊 Chart Type:**")
        chart_type = st.radio(
            "Select chart type",
            options=["line", "candlestick"],
            format_func=lambda x: "Line Chart" if x == "line" else "Candlestick Chart"
        )
        
        # Auto-refresh option
        st.markdown("---")
        auto_refresh = st.checkbox("🔄 Auto-refresh (5 min)", value=False)
        
        if auto_refresh:
            # Auto-refresh every 5 minutes
            time.sleep(1)
            st.rerun()
    
    # Main content
    if symbol:
        # Validate symbol
        if not StockDataFetcher.validate_symbol(symbol):
            st.error(f"❌ Invalid stock symbol: {symbol}")
            st.info("Please enter a valid stock ticker symbol (e.g., AAPL, GOOGL, MSFT)")
            return
        
        # Loading spinner
        with st.spinner(f"Loading data for {symbol}..."):
            # Fetch data
            stock_info = StockDataFetcher.get_stock_info(symbol)
            historical_data = StockDataFetcher.get_stock_history(symbol, period)
            financial_metrics = StockDataFetcher.get_financial_metrics(symbol)
        
        if not stock_info or not financial_metrics:
            st.error(f"❌ Could not fetch data for {symbol}")
            return
        
        # Company information header
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.markdown(f"### {financial_metrics.get('Company Name', symbol)}")
            st.markdown(f"**{financial_metrics.get('Symbol', symbol)}** | {financial_metrics.get('Sector', 'N/A')}")
        
        with col2:
            current_price = financial_metrics.get('Current Price', 'N/A')
            previous_close = financial_metrics.get('Previous Close', 'N/A')
            
            if current_price != 'N/A' and previous_close != 'N/A':
                change_data = ChartGenerator.create_price_change_indicator(current_price, previous_close)
                
                st.markdown(f"### ${current_price:.2f}")
                if change_data['change'] != 'N/A':
                    change_symbol = "+" if change_data['change'] >= 0 else ""
                    # Show price change with appropriate styling
                    change_text = f"{change_symbol}{change_data['change']} ({change_symbol}{change_data['change_percent']}%)"
                    if change_data['change'] >= 0:
                        st.success(f"🟢 {change_text}")
                    else:
                        st.error(f"🔴 {change_text}")
            else:
                st.markdown("### Price: N/A")
        
        with col3:
            st.markdown(f"**Last Updated:**")
            st.markdown(f"{datetime.now().strftime('%H:%M:%S')}")
        
        st.markdown("---")
        
        # Main content tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Charts", "📊 Financial Metrics", "💡 Investment Analysis", "📋 Detailed Data", "📥 Export"])
        
        with tab1:
            if historical_data is not None and not historical_data.empty:
                # Add moving averages
                historical_data = StockDataFetcher.calculate_moving_averages(historical_data)
                
                # Price chart
                st.subheader(f"📈 {symbol} Price Chart")
                price_chart = ChartGenerator.create_price_chart(historical_data, symbol, chart_type)
                st.plotly_chart(price_chart, use_container_width=True)
                
                # Volume chart
                st.subheader(f"📊 {symbol} Trading Volume")
                volume_chart = ChartGenerator.create_volume_chart(historical_data, symbol)
                st.plotly_chart(volume_chart, use_container_width=True)
                
                # Financial ratios chart
                if financial_metrics:
                    st.subheader("📊 Key Financial Ratios")
                    ratios_chart = ChartGenerator.create_financial_metrics_chart(financial_metrics)
                    if ratios_chart.data:
                        st.plotly_chart(ratios_chart, use_container_width=True)
                    else:
                        st.info("No numeric financial ratios available for visualization")
            else:
                st.error("No historical data available for the selected period")
        
        with tab2:
            st.subheader("📊 Financial Metrics")
            
            if financial_metrics:
                # Create metrics DataFrame
                metrics_df = DataFormatter.create_metrics_dataframe(financial_metrics)
                
                # Display metrics in organized sections
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 💰 Price Information")
                    price_metrics = metrics_df[metrics_df['Metric'].isin([
                        'Current Price', 'Previous Close', 'Open', 'Day High', 'Day Low',
                        '52 Week High', '52 Week Low'
                    ])]
                    st.dataframe(price_metrics, hide_index=True, use_container_width=True)
                    
                    st.markdown("#### 📈 Valuation Ratios")
                    valuation_metrics = metrics_df[metrics_df['Metric'].isin([
                        'P/E Ratio', 'Forward P/E', 'PEG Ratio', 'Price to Book', 'Price to Sales'
                    ])]
                    st.dataframe(valuation_metrics, hide_index=True, use_container_width=True)
                
                with col2:
                    st.markdown("#### 📊 Market Data")
                    market_metrics = metrics_df[metrics_df['Metric'].isin([
                        'Market Cap', 'Enterprise Value', 'Volume', 'Average Volume', 'Beta'
                    ])]
                    st.dataframe(market_metrics, hide_index=True, use_container_width=True)
                    
                    st.markdown("#### 💼 Financial Health")
                    health_metrics = metrics_df[metrics_df['Metric'].isin([
                        'Debt to Equity', 'Return on Equity', 'Return on Assets',
                        'Dividend Yield', 'Dividend Rate', 'Payout Ratio'
                    ])]
                    st.dataframe(health_metrics, hide_index=True, use_container_width=True)
                
                # Company info
                st.markdown("#### 🏢 Company Information")
                company_info = metrics_df[metrics_df['Metric'].isin([
                    'Company Name', 'Symbol', 'Sector', 'Industry'
                ])]
                st.dataframe(company_info, hide_index=True, use_container_width=True)
            else:
                st.error("No financial metrics available")
        
        with tab3:
            st.subheader("💡 Análisis de Inversión")
            
            if financial_metrics:
                current_price = financial_metrics.get('Current Price', 0)
                if current_price == 'N/A' or current_price is None:
                    st.error("No se puede obtener el precio actual para el análisis")
                else:
                    day_low = financial_metrics.get('Day Low', current_price * 0.98)
                    day_high = financial_metrics.get('Day High', current_price * 1.02)
                    week52_low = financial_metrics.get('52 Week Low', current_price * 0.8)
                    week52_high = financial_metrics.get('52 Week High', current_price * 1.2)
                    
                    # Convert to float if needed
                    try:
                        current_price = float(current_price)
                        day_low = float(day_low) if day_low != 'N/A' else current_price * 0.98
                        day_high = float(day_high) if day_high != 'N/A' else current_price * 1.02
                        week52_low = float(week52_low) if week52_low != 'N/A' else current_price * 0.8
                        week52_high = float(week52_high) if week52_high != 'N/A' else current_price * 1.2
                        
                        # Create layout
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            # Price ranges
                            InvestmentAnalysis.create_price_range_widget(
                                symbol, current_price, day_low, day_high, week52_low, week52_high
                            )
                            
                            # Technical analysis gauge
                            InvestmentAnalysis.create_technical_analysis_gauge(symbol)
                            
                            # Analyst opinion
                            InvestmentAnalysis.create_analyst_opinion_widget(symbol, current_price)
                        
                        with col2:
                            # Investment summary card
                            InvestmentAnalysis.create_investment_summary_card(symbol, current_price, financial_metrics)
                            
                            # Company health card
                            InvestmentAnalysis.create_company_health_card(symbol, financial_metrics)
                            
                            # Market sentiment
                            InvestmentAnalysis.create_sentiment_widget(symbol)
                    except (ValueError, TypeError) as e:
                        st.error(f"Error procesando datos de precio: {e}")
            else:
                st.error("No hay datos financieros disponibles para el análisis de inversión")
        
        with tab4:
            st.subheader("📋 Datos Históricos")
            
            if historical_data is not None and not historical_data.empty:
                # Display data summary
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        label="Total Records",
                        value=len(historical_data)
                    )
                
                with col2:
                    st.metric(
                        label="Date Range",
                        value=f"{historical_data['Date'].min().strftime('%Y-%m-%d')} to {historical_data['Date'].max().strftime('%Y-%m-%d')}"
                    )
                
                with col3:
                    avg_volume = historical_data['Volume'].mean() if 'Volume' in historical_data.columns else 0
                    st.metric(
                        label="Avg Volume",
                        value=DataFormatter.format_number(avg_volume)
                    )
                
                with col4:
                    price_range = historical_data['High'].max() - historical_data['Low'].min()
                    st.metric(
                        label="Price Range",
                        value=f"${price_range:.2f}"
                    )
                
                # Display full data table
                st.markdown("#### 📊 Complete Historical Data")
                
                # Format data for display
                display_data = historical_data.copy()
                display_data['Date'] = display_data['Date'].dt.strftime('%Y-%m-%d')
                
                # Round numeric columns
                numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                for col in numeric_columns:
                    if col in display_data.columns:
                        if col == 'Volume':
                            display_data[col] = display_data[col].apply(DataFormatter.format_number)
                        else:
                            display_data[col] = display_data[col].round(2)
                
                st.dataframe(
                    display_data,
                    hide_index=True,
                    use_container_width=True,
                    height=400
                )
            else:
                st.error("No historical data available")
        
        with tab5:
            st.subheader("📥 Export Data")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📊 Export Historical Data")
                if historical_data is not None and not historical_data.empty:
                    csv_data = DataFormatter.export_to_csv(historical_data, f"{symbol}_historical_data.csv")
                    st.download_button(
                        label="📈 Download Historical Data (CSV)",
                        data=csv_data,
                        file_name=f"{symbol}_historical_data_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        help="Download complete historical price and volume data"
                    )
                else:
                    st.info("No historical data available for export")
            
            with col2:
                st.markdown("#### 📋 Export Financial Metrics")
                if financial_metrics:
                    metrics_df = DataFormatter.create_metrics_dataframe(financial_metrics)
                    csv_metrics = DataFormatter.export_to_csv(metrics_df, f"{symbol}_financial_metrics.csv")
                    st.download_button(
                        label="📊 Download Financial Metrics (CSV)",
                        data=csv_metrics,
                        file_name=f"{symbol}_financial_metrics_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        help="Download all financial metrics and ratios"
                    )
                else:
                    st.info("No financial metrics available for export")
            
            # Export instructions
            st.markdown("---")
            st.markdown("#### 📄 Export Information")
            st.info("""
            **Historical Data CSV includes:**
            - Date, Open, High, Low, Close, Volume
            - Moving averages (if calculated)
            
            **Financial Metrics CSV includes:**
            - All available financial ratios and metrics
            - Company information
            - Market data and valuation ratios
            """)
    
    else:
        # Welcome screen
        st.markdown("""
        ## Welcome to the Stock Financial Dashboard! 📈
        
        This dashboard provides comprehensive financial analysis for stocks with:
        
        - **Real-time Data**: Live stock prices and metrics from Yahoo Finance
        - **Interactive Charts**: Candlestick and line charts with moving averages
        - **Financial Metrics**: Complete ratio analysis and company information
        - **Data Export**: Download historical data and metrics as CSV files
        
        ### 🚀 Getting Started
        1. Enter a stock symbol in the sidebar (e.g., AAPL, GOOGL, MSFT)
        2. Select your preferred time period and chart type
        3. Explore the data across different tabs
        4. Export data for further analysis
        
        ### 📊 Features
        - Price charts with technical indicators
        - Volume analysis with price movement indicators
        - Comprehensive financial ratios
        - Historical data analysis
        - CSV export functionality
        """)
        
        # Display popular symbols
        st.markdown("### 🔥 Popular Stocks")
        popular_cols = st.columns(8)
        popular_symbols = DataFormatter.get_popular_symbols()[:8]
        
        for i, pop_symbol in enumerate(popular_symbols):
            with popular_cols[i]:
                if st.button(pop_symbol, key=f"pop_{pop_symbol}"):
                    st.session_state.selected_symbol = pop_symbol
                    st.rerun()

# Auto-refresh mechanism
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()

# Check if we need to refresh
if datetime.now() - st.session_state.last_refresh > timedelta(minutes=5):
    st.session_state.last_refresh = datetime.now()
    if st.session_state.get('auto_refresh', False):
        st.rerun()

if __name__ == "__main__":
    main()
