# Stock Financial Dashboard

## Overview

This is a comprehensive stock financial dashboard system with two main components:

1. **Streamlit Application**: Python-based interactive dashboard using yfinance for real-time stock data
2. **Pure Web Dashboard**: HTML/JavaScript version that works directly in browsers without installation

The system provides interactive financial visualizations, real-time stock data analysis, and comprehensive export capabilities. Both versions feature dark themes and professional financial metrics display.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web framework
- **UI Layout**: Wide layout with expandable sidebar for user controls
- **Visualization**: Plotly for interactive charts and graphs
- **Styling**: Custom color scheme with dark theme support

### Backend Architecture
- **Data Source**: Yahoo Finance API via yfinance library
- **Data Processing**: Pandas for data manipulation and analysis
- **Session Management**: Streamlit's built-in session state for maintaining user data across interactions

### Application Structure
The application follows a modular design pattern with clear separation of concerns:
- Main application logic in `app.py`
- Data fetching operations in `utils/data_fetcher.py`
- Chart generation in `utils/chart_generator.py`
- Helper functions and utilities in `utils/helpers.py`

## Key Components

### 1. Main Application (`app.py`)
- **Purpose**: Entry point and UI coordination
- **Features**: 
  - Page configuration and layout setup
  - Session state initialization
  - Main dashboard interface
  - Sidebar controls for stock selection and time period

### 2. Stock Data Fetcher (`utils/data_fetcher.py`)
- **Purpose**: Handles all stock data retrieval operations
- **Features**:
  - Fetches basic stock information and metadata
  - Retrieves historical price data with configurable time periods
  - Error handling for invalid symbols or data issues
  - Data validation and cleaning

### 3. Chart Generator (`utils/chart_generator.py`)
- **Purpose**: Creates interactive financial visualizations
- **Features**:
  - Line charts for stock price trends
  - Moving averages calculation and display
  - Custom styling with consistent color scheme
  - Interactive hover tooltips and zoom functionality

### 4. Helper Functions (`utils/helpers.py`)
- **Purpose**: Utility functions for data formatting and validation
- **Features**:
  - Stock symbol validation using regex patterns
  - Currency formatting with unit abbreviations (K, M, B, T)
  - Percentage formatting for financial metrics

## Data Flow

1. **User Input**: User enters stock symbol and selects time period through sidebar
2. **Data Validation**: Symbol is validated using regex patterns
3. **Data Fetching**: StockDataFetcher retrieves data from Yahoo Finance API
4. **Data Processing**: Raw data is cleaned and structured using pandas
5. **Visualization**: ChartGenerator creates interactive charts using Plotly
6. **Display**: Results are rendered in the Streamlit interface
7. **Session Management**: Data is cached in session state for performance

## External Dependencies

### Core Libraries
- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive visualization library
- **yfinance**: Yahoo Finance API wrapper
- **numpy**: Numerical computing support

### Data Sources
- **Yahoo Finance**: Primary data source for stock prices, company information, and historical data
- **Real-time Updates**: Data is fetched on-demand when users request new symbols or time periods

## Deployment Strategy

### Local Development
- Standard Python environment with pip-installed dependencies
- Streamlit development server for local testing
- No database requirements (data fetched from external APIs)

### Production Considerations
- **Scalability**: Stateless design allows for horizontal scaling
- **Caching**: Session state provides basic caching; can be enhanced with Redis for production
- **Rate Limiting**: Yahoo Finance API has implicit rate limits that should be monitored
- **Error Handling**: Comprehensive error handling for network issues and invalid data

### Platform Compatibility
- Compatible with cloud platforms like Streamlit Cloud, Heroku, or AWS
- No persistent storage requirements
- Minimal resource requirements due to efficient data processing