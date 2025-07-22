import pandas as pd
import streamlit as st
from typing import Any, Dict
import io

class DataFormatter:
    """Class for data formatting and helper functions"""
    
    @staticmethod
    def format_currency(value: Any) -> str:
        """
        Format value as currency
        
        Args:
            value: Numeric value to format
            
        Returns:
            Formatted currency string
        """
        if value == 'N/A' or value is None:
            return 'N/A'
        
        try:
            num_value = float(value)
            if num_value >= 1e12:
                return f"${num_value/1e12:.2f}T"
            elif num_value >= 1e9:
                return f"${num_value/1e9:.2f}B"
            elif num_value >= 1e6:
                return f"${num_value/1e6:.2f}M"
            elif num_value >= 1e3:
                return f"${num_value/1e3:.2f}K"
            else:
                return f"${num_value:.2f}"
        except (ValueError, TypeError):
            return str(value)
    
    @staticmethod
    def format_number(value: Any) -> str:
        """
        Format large numbers with appropriate suffixes
        
        Args:
            value: Numeric value to format
            
        Returns:
            Formatted number string
        """
        if value == 'N/A' or value is None:
            return 'N/A'
        
        try:
            num_value = float(value)
            if num_value >= 1e12:
                return f"{num_value/1e12:.2f}T"
            elif num_value >= 1e9:
                return f"{num_value/1e9:.2f}B"
            elif num_value >= 1e6:
                return f"{num_value/1e6:.2f}M"
            elif num_value >= 1e3:
                return f"{num_value/1e3:.2f}K"
            else:
                return f"{num_value:,.2f}"
        except (ValueError, TypeError):
            return str(value)
    
    @staticmethod
    def format_percentage(value: Any) -> str:
        """
        Format value as percentage
        
        Args:
            value: Numeric value to format
            
        Returns:
            Formatted percentage string
        """
        if value == 'N/A' or value is None:
            return 'N/A'
        
        try:
            num_value = float(value)
            # If value is already in percentage form (> 1), don't multiply by 100
            if num_value > 1:
                return f"{num_value:.2f}%"
            else:
                return f"{num_value * 100:.2f}%"
        except (ValueError, TypeError):
            return str(value)
    
    @staticmethod
    def format_ratio(value: Any) -> str:
        """
        Format financial ratios
        
        Args:
            value: Numeric value to format
            
        Returns:
            Formatted ratio string
        """
        if value == 'N/A' or value is None:
            return 'N/A'
        
        try:
            num_value = float(value)
            return f"{num_value:.2f}"
        except (ValueError, TypeError):
            return str(value)
    
    @staticmethod
    def create_metrics_dataframe(metrics: Dict[str, Any]) -> pd.DataFrame:
        """
        Create a formatted DataFrame from metrics dictionary
        
        Args:
            metrics: Dictionary of financial metrics
            
        Returns:
            Formatted pandas DataFrame
        """
        formatted_metrics = {}
        
        # Format different types of metrics
        currency_fields = ['Current Price', 'Previous Close', 'Open', 'Day High', 'Day Low', 
                          '52 Week High', '52 Week Low', 'Dividend Rate']
        
        large_number_fields = ['Market Cap', 'Enterprise Value', 'Volume', 'Average Volume']
        
        percentage_fields = ['Dividend Yield', 'Return on Equity', 'Return on Assets', 'Payout Ratio']
        
        ratio_fields = ['P/E Ratio', 'Forward P/E', 'PEG Ratio', 'Price to Book', 
                       'Price to Sales', 'Debt to Equity', 'Beta']
        
        for key, value in metrics.items():
            if key in currency_fields:
                formatted_metrics[key] = DataFormatter.format_currency(value)
            elif key in large_number_fields:
                formatted_metrics[key] = DataFormatter.format_number(value)
            elif key in percentage_fields:
                formatted_metrics[key] = DataFormatter.format_percentage(value)
            elif key in ratio_fields:
                formatted_metrics[key] = DataFormatter.format_ratio(value)
            else:
                formatted_metrics[key] = str(value) if value != 'N/A' else 'N/A'
        
        # Create DataFrame
        df = pd.DataFrame.from_dict({'Metric': list(formatted_metrics.keys()), 
                                   'Value': list(formatted_metrics.values())})
        return df
    
    @staticmethod
    def export_to_csv(df: pd.DataFrame, filename: str) -> bytes:
        """
        Export DataFrame to CSV bytes
        
        Args:
            df: DataFrame to export
            filename: Name for the file
            
        Returns:
            CSV data as bytes
        """
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        return csv_buffer.getvalue().encode('utf-8')
    
    @staticmethod
    def get_popular_symbols() -> list:
        """
        Get list of popular stock symbols
        
        Returns:
            List of popular stock symbols
        """
        return [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX',
            'BABA', 'V', 'JNJ', 'WMT', 'JPM', 'PG', 'UNH', 'MA', 'DIS', 'HD',
            'PYPL', 'BAC', 'ADBE', 'CRM', 'VZ', 'CMCSA', 'NKE', 'MRK', 'PFE',
            'T', 'PEP', 'ABT', 'COST', 'AVGO', 'TMO', 'ACN', 'MDT', 'LLY',
            'ORCL', 'CVX', 'TXN', 'QCOM', 'DHR', 'NEE', 'AMT', 'BMY', 'PM',
            'LIN', 'HON', 'IBM', 'SBUX', 'MMM', 'GE', 'CAT', 'AXP', 'BA'
        ]
    
    @staticmethod
    def validate_and_clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate and clean stock data
        
        Args:
            df: Raw stock data DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        if df is None or df.empty:
            return df
        
        # Remove any rows with all NaN values
        df = df.dropna(how='all')
        
        # Forward fill any missing values in price columns
        price_columns = ['Open', 'High', 'Low', 'Close']
        for col in price_columns:
            if col in df.columns:
                df[col] = df[col].fillna(method='ffill')
        
        # Fill missing volume with 0
        if 'Volume' in df.columns:
            df['Volume'] = df['Volume'].fillna(0)
        
        return df
