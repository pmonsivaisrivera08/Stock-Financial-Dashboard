# Stock Financial Dashboard

## Overview

This is a Python-based web application built with Streamlit that provides an interactive stock financial dashboard. The application integrates with Yahoo Finance to fetch real-time stock data and presents it through interactive charts and financial metrics. Users can input any stock symbol and view comprehensive financial information including price charts, candlestick charts, volume data, and key financial ratios.

## User Preferences

Preferred communication style: Simple, everyday language.
Language preference: Spanish for interface elements and labels.
Design preference: Professional financial platform appearance with investment analysis features similar to trading platforms.

## System Architecture

The application follows a modular architecture with clear separation of concerns:

- **Frontend**: Streamlit web framework for the user interface
- **Data Layer**: Yahoo Finance API integration via yfinance library
- **Visualization**: Plotly for interactive charts and graphs
- **Data Processing**: Pandas for data manipulation and analysis
- **Caching**: Streamlit's built-in caching for performance optimization

## Key Components

### Main Application (`app.py`)
- Entry point for the Streamlit application
- Handles page configuration and custom CSS styling
- Orchestrates the interaction between different utility modules
- Implements a green-themed dark UI design

### Data Fetcher (`utils/data_fetcher.py`)
- **Purpose**: Handles all data retrieval from Yahoo Finance
- **Key Features**:
  - Cached stock information retrieval (5-minute TTL)
  - Historical stock data fetching with configurable time periods
  - Error handling for invalid stock symbols
  - Data validation to ensure quality

### Chart Generator (`utils/chart_generator.py`)
- **Purpose**: Creates interactive financial charts
- **Capabilities**:
  - Line charts for price trends
  - Candlestick charts for detailed OHLC data
  - Moving averages integration
  - Volume charts with price movement indicators
  - Custom styling with green/red color scheme for gains/losses

### Data Formatter (`utils/helpers.py`)
- **Purpose**: Provides utility functions for data presentation
- **Functions**:
  - Currency formatting with appropriate suffixes (K, M, B, T)
  - Number formatting for large values
  - CSV export functionality
  - Data validation and error handling

### Investment Analysis (`utils/investment_analysis.py`)
- **Purpose**: Creates professional investment analysis components
- **Features**:
  - Fair value assessment with price recommendations
  - Price range indicators (daily and 52-week ranges)
  - Technical analysis gauge with scoring system
  - Analyst opinion simulation with target prices
  - Market sentiment indicators (bullish/bearish)
  - Company health assessment based on financial ratios
  - Investment summary cards with actionable insights

## Data Flow

1. **User Input**: User enters stock symbol in the Streamlit interface
2. **Data Retrieval**: StockDataFetcher queries Yahoo Finance API
3. **Caching**: Results are cached for 5 minutes to improve performance
4. **Data Processing**: Raw data is processed and formatted using helper functions
5. **Visualization**: ChartGenerator creates interactive plots
6. **Display**: Formatted data and charts are rendered in the Streamlit UI
7. **Export**: Users can download data as CSV files

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework for the user interface
- **yfinance**: Yahoo Finance API wrapper for stock data
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualization library
- **NumPy**: Numerical computing support

### API Integration
- **Yahoo Finance**: Primary data source for stock information, historical prices, and financial metrics
- **No authentication required**: Uses public Yahoo Finance endpoints

## Deployment Strategy

The application is designed for local development and can be easily deployed to various platforms:

### Local Development
- Run with `streamlit run app.py`
- Serves on `http://localhost:8501`
- Hot reload enabled for development

### Production Considerations
- Caching implemented to reduce API calls and improve performance
- Error handling for network issues and invalid stock symbols
- Responsive design suitable for desktop and mobile viewing
- Can be deployed to Streamlit Cloud, Heroku, or other cloud platforms

### Configuration
- Streamlit configuration can be customized via `.streamlit/config.toml`
- Dark theme enabled by default
- Wide layout for better chart visibility

### Performance Optimizations
- Data caching with 5-minute TTL to balance freshness and performance
- Efficient data structures using Pandas DataFrames
- Lazy loading of chart components
- Minimal external dependencies to reduce load times

## Recent Changes (January 2025)

### Web Application Migration
- Converted Streamlit application to pure web application (HTML/CSS/JavaScript)
- Maintained identical functionality and design from Streamlit version
- Features implemented:
  - Interactive stock symbol search with popular symbol buttons
  - Real-time price charts (line and candlestick) with Plotly.js
  - Volume analysis with color-coded bars
  - Moving averages (20, 50, 200 day) with distinct colors
  - Complete financial metrics display
  - Investment analysis with gauges and recommendations
  - Historical data tables with export functionality
  - CSV/JSON export capabilities
- Design maintains TradingView-style color scheme:
  - Blue/red for bullish/bearish indicators
  - Green/yellow/red semaphore for technical analysis
  - Professional dark theme with gradients
- Responsive design for desktop and mobile
- Static file serving via Python HTTP server on port 5000

### Previous Investment Analysis Integration
