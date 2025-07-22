import yfinance as yf
import pandas as pd
import streamlit as st
from typing import Optional, Dict, Any
import numpy as np

class StockDataFetcher:
    """Class to handle stock data fetching from Yahoo Finance"""
    
    @staticmethod
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_stock_info(symbol: str) -> Optional[Dict[str, Any]]:
        """
        Fetch basic stock information
        
        Args:
            symbol (str): Stock symbol (e.g., 'AAPL')
            
        Returns:
            Dict containing stock info or None if error
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Validate that we got valid data
            if not info or 'symbol' not in info:
                return None
                
            return info
        except Exception as e:
            st.error(f"Error fetching stock info for {symbol}: {str(e)}")
            return None
    
    @staticmethod
    @st.cache_data(ttl=300)
    def get_stock_history(symbol: str, period: str = "1y") -> Optional[pd.DataFrame]:
        """
        Fetch historical stock data
        
        Args:
            symbol (str): Stock symbol
            period (str): Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
            
        Returns:
            DataFrame with historical data or None if error
        """
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                return None
                
            # Reset index to make Date a column
            hist.reset_index(inplace=True)
            
            return hist
        except Exception as e:
            st.error(f"Error fetching historical data for {symbol}: {str(e)}")
            return None
    
    @staticmethod
    @st.cache_data(ttl=300)
    def get_financial_metrics(symbol: str) -> Dict[str, Any]:
        """
        Extract key financial metrics from stock info
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            Dictionary with formatted financial metrics
        """
        info = StockDataFetcher.get_stock_info(symbol)
        
        if not info:
            return {}
        
        metrics = {}
        
        # Basic info
        metrics['Company Name'] = info.get('longName', 'N/A')
        metrics['Symbol'] = info.get('symbol', symbol.upper())
        metrics['Sector'] = info.get('sector', 'N/A')
        metrics['Industry'] = info.get('industry', 'N/A')
        
        # Price data
        metrics['Current Price'] = info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))
        metrics['Previous Close'] = info.get('previousClose', 'N/A')
        metrics['Open'] = info.get('open', 'N/A')
        metrics['Day High'] = info.get('dayHigh', 'N/A')
        metrics['Day Low'] = info.get('dayLow', 'N/A')
        
        # Volume data
        metrics['Volume'] = info.get('volume', 'N/A')
        metrics['Average Volume'] = info.get('averageVolume', 'N/A')
        
        # Market data
        metrics['Market Cap'] = info.get('marketCap', 'N/A')
        metrics['Enterprise Value'] = info.get('enterpriseValue', 'N/A')
        
        # Valuation ratios
        metrics['P/E Ratio'] = info.get('trailingPE', 'N/A')
        metrics['Forward P/E'] = info.get('forwardPE', 'N/A')
        metrics['PEG Ratio'] = info.get('pegRatio', 'N/A')
        metrics['Price to Book'] = info.get('priceToBook', 'N/A')
        metrics['Price to Sales'] = info.get('priceToSalesTrailing12Months', 'N/A')
        
        # Financial health
        metrics['Debt to Equity'] = info.get('debtToEquity', 'N/A')
        metrics['Return on Equity'] = info.get('returnOnEquity', 'N/A')
        metrics['Return on Assets'] = info.get('returnOnAssets', 'N/A')
        
        # Dividend data
        metrics['Dividend Yield'] = info.get('dividendYield', 'N/A')
        metrics['Dividend Rate'] = info.get('dividendRate', 'N/A')
        metrics['Payout Ratio'] = info.get('payoutRatio', 'N/A')
        
        # Range data
        metrics['52 Week High'] = info.get('fiftyTwoWeekHigh', 'N/A')
        metrics['52 Week Low'] = info.get('fiftyTwoWeekLow', 'N/A')
        
        # Beta
        metrics['Beta'] = info.get('beta', 'N/A')
        
        return metrics
    
    @staticmethod
    def validate_symbol(symbol: str) -> bool:
        """
        Validate if a stock symbol exists
        
        Args:
            symbol (str): Stock symbol to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return bool(info and 'symbol' in info)
        except:
            return False
    
    @staticmethod
    @st.cache_data(ttl=300)
    def calculate_moving_averages(df: pd.DataFrame, periods: list = [20, 50, 200]) -> pd.DataFrame:
        """
        Calculate moving averages for given periods
        
        Args:
            df (pd.DataFrame): DataFrame with 'Close' column
            periods (list): List of periods for moving averages
            
        Returns:
            DataFrame with moving averages added
        """
        df_copy = df.copy()
        
        for period in periods:
            if len(df_copy) >= period:
                df_copy[f'MA_{period}'] = df_copy['Close'].rolling(window=period).mean()
        
        return df_copy
