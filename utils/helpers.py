import re
import pandas as pd
import numpy as np
from datetime import datetime

def validate_symbol(symbol):
    """Validate stock symbol format"""
    if not symbol:
        return False
    
    # Basic validation: alphanumeric characters, dots, and dashes
    # Length between 1-8 characters (most stock symbols are within this range)
    pattern = r'^[A-Z0-9.-]{1,8}$'
    
    if re.match(pattern, symbol.upper()):
        return True
    
    return False

def format_currency(value, short=False):
    """Format currency values with appropriate units"""
    if value is None or pd.isna(value):
        return "N/A"
    
    try:
        value = float(value)
    except (ValueError, TypeError):
        return "N/A"
    
    if value == 0:
        return "$0.00"
    
    if short:
        # Format large numbers with units (K, M, B, T)
        if abs(value) >= 1e12:
            return f"${value/1e12:.2f}T"
        elif abs(value) >= 1e9:
            return f"${value/1e9:.2f}B"
        elif abs(value) >= 1e6:
            return f"${value/1e6:.2f}M"
        elif abs(value) >= 1e3:
            return f"${value/1e3:.2f}K"
        else:
            return f"${value:.2f}"
    else:
        # Standard currency format
        return f"${value:,.2f}"

def format_percentage(value):
    """Format percentage values"""
    if value is None or pd.isna(value):
        return "N/A"
    
    try:
        value = float(value)
        return f"{value:.2f}%"
    except (ValueError, TypeError):
        return "N/A"

def format_number(value, decimals=2):
    """Format numbers with thousand separators"""
    if value is None or pd.isna(value):
        return "N/A"
    
    try:
        value = float(value)
        if decimals == 0:
            return f"{value:,.0f}"
        else:
            return f"{value:,.{decimals}f}"
    except (ValueError, TypeError):
        return "N/A"

def calculate_performance_metrics(data):
    """Calculate various performance metrics from price data"""
    if data is None or data.empty:
        return {}
    
    metrics = {}
    
    try:
        # Calculate daily returns
        daily_returns = data['Close'].pct_change().dropna()
        
        if len(daily_returns) > 0:
            # Annualized return (assuming 252 trading days)
            total_return = (data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1
            days = len(data)
            annualized_return = (1 + total_return) ** (252 / days) - 1
            metrics['annualized_return'] = annualized_return
            
            # Volatility (annualized standard deviation)
            volatility = daily_returns.std() * np.sqrt(252)
            metrics['volatility'] = volatility
            
            # Sharpe ratio (assuming risk-free rate of 2%)
            risk_free_rate = 0.02
            if volatility > 0:
                sharpe_ratio = (annualized_return - risk_free_rate) / volatility
                metrics['sharpe_ratio'] = sharpe_ratio
            
            # Maximum drawdown
            cumulative_returns = (1 + daily_returns).cumprod()
            rolling_max = cumulative_returns.expanding().max()
            drawdown = (cumulative_returns - rolling_max) / rolling_max
            max_drawdown = drawdown.min()
            metrics['max_drawdown'] = max_drawdown
            
            # Value at Risk (95% confidence)
            var_95 = np.percentile(daily_returns, 5)
            metrics['var_95'] = var_95
            
            # Average daily return
            avg_daily_return = daily_returns.mean()
            metrics['avg_daily_return'] = avg_daily_return
            
    except Exception as e:
        print(f"Error calculating performance metrics: {e}")
    
    return metrics

def get_trading_status():
    """Determine if markets are currently open"""
    try:
        from datetime import datetime, time
        import pytz
        
        # US Eastern timezone
        eastern = pytz.timezone('US/Eastern')
        now = datetime.now(eastern)
        
        # Check if it's a weekday
        if now.weekday() >= 5:  # Saturday = 5, Sunday = 6
            return "Markets Closed (Weekend)"
        
        # Market hours: 9:30 AM to 4:00 PM ET
        market_open = time(9, 30)
        market_close = time(16, 0)
        current_time = now.time()
        
        if market_open <= current_time <= market_close:
            return "Markets Open"
        else:
            return "Markets Closed"
            
    except Exception:
        return "Market Status Unknown"

def format_market_cap(market_cap):
    """Format market capitalization with appropriate units"""
    return format_currency(market_cap, short=True)

def calculate_rsi(prices, window=14):
    """Calculate Relative Strength Index"""
    if len(prices) < window + 1:
        return None
    
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

def calculate_bollinger_bands(prices, window=20, num_std=2):
    """Calculate Bollinger Bands"""
    if len(prices) < window:
        return None, None, None
    
    rolling_mean = prices.rolling(window=window).mean()
    rolling_std = prices.rolling(window=window).std()
    
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    
    return upper_band, rolling_mean, lower_band

def safe_divide(a, b, default=0):
    """Safely divide two numbers, returning default if division by zero"""
    try:
        if b == 0 or pd.isna(b):
            return default
        return a / b
    except (TypeError, ZeroDivisionError):
        return default

def clean_dataframe(df):
    """Clean and prepare dataframe for display"""
    if df is None or df.empty:
        return df
    
    # Remove any rows with all NaN values
    df = df.dropna(how='all')
    
    # Replace infinite values with NaN
    df = df.replace([np.inf, -np.inf], np.nan)
    
    return df

def get_sector_performance():
    """Get major sector performance (placeholder for future implementation)"""
    # This could be expanded to fetch sector ETF performance
    sectors = {
        'Technology': 'XLK',
        'Healthcare': 'XLV', 
        'Financial': 'XLF',
        'Energy': 'XLE',
        'Consumer Discretionary': 'XLY',
        'Industrials': 'XLI',
        'Consumer Staples': 'XLP',
        'Utilities': 'XLU',
        'Materials': 'XLB',
        'Real Estate': 'XLRE',
        'Communication': 'XLC'
    }
    return sectors
