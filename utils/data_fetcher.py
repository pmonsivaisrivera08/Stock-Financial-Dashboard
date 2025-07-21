import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

class StockDataFetcher:
    """Class to handle all stock data fetching operations"""
    
    def __init__(self, symbol):
        self.symbol = symbol.upper()
        self.ticker = yf.Ticker(self.symbol)
    
    def get_stock_info(self):
        """Fetch basic stock information"""
        try:
            info = self.ticker.info
            return info
        except Exception as e:
            st.error(f"Error fetching stock info: {str(e)}")
            return {}
    
    def get_historical_data(self, period="1y"):
        """Fetch historical stock data"""
        try:
            # Convert period to yfinance format if needed
            period_map = {
                "1mo": "1mo",
                "3mo": "3mo", 
                "6mo": "6mo",
                "1y": "1y",
                "2y": "2y",
                "5y": "5y"
            }
            
            yf_period = period_map.get(period, "1y")
            
            # Fetch historical data
            hist_data = self.ticker.history(period=yf_period)
            
            if hist_data.empty:
                st.error(f"No historical data available for {self.symbol}")
                return None
                
            # Clean the data
            hist_data = hist_data.dropna()
            
            # Ensure we have the required columns
            required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            missing_columns = [col for col in required_columns if col not in hist_data.columns]
            
            if missing_columns:
                st.warning(f"Missing columns in historical data: {missing_columns}")
            
            return hist_data
            
        except Exception as e:
            st.error(f"Error fetching historical data: {str(e)}")
            return None
    
    def get_financial_metrics(self):
        """Calculate and return financial metrics"""
        try:
            info = self.get_stock_info()
            historical = self.get_historical_data("1y")
            
            metrics = {}
            
            if historical is not None and not historical.empty:
                # Price-based metrics
                current_price = historical['Close'].iloc[-1]
                metrics['current_price'] = current_price
                
                # Volatility (standard deviation of daily returns)
                daily_returns = historical['Close'].pct_change().dropna()
                metrics['volatility'] = daily_returns.std() * (252 ** 0.5)  # Annualized
                
                # Price performance
                if len(historical) > 1:
                    price_1d = historical['Close'].iloc[-2] if len(historical) > 1 else current_price
                    price_1w = historical['Close'].iloc[-7] if len(historical) > 7 else current_price
                    price_1m = historical['Close'].iloc[-30] if len(historical) > 30 else current_price
                    
                    metrics['price_change_1d'] = (current_price - price_1d) / price_1d
                    metrics['price_change_1w'] = (current_price - price_1w) / price_1w
                    metrics['price_change_1m'] = (current_price - price_1m) / price_1m
                
                # Volume metrics
                metrics['avg_volume'] = historical['Volume'].mean()
                metrics['current_volume'] = historical['Volume'].iloc[-1]
                
                # Trading range
                metrics['52w_high'] = historical['High'].max()
                metrics['52w_low'] = historical['Low'].min()
                
                # Moving averages
                metrics['sma_20'] = historical['Close'].rolling(window=20).mean().iloc[-1]
                metrics['sma_50'] = historical['Close'].rolling(window=50).mean().iloc[-1]
                metrics['sma_200'] = historical['Close'].rolling(window=200).mean().iloc[-1] if len(historical) >= 200 else None
            
            # Add fundamental metrics from info
            if info:
                fundamental_keys = [
                    'marketCap', 'enterpriseValue', 'trailingPE', 'forwardPE',
                    'priceToBook', 'priceToSalesTrailing12Months', 'pegRatio',
                    'dividendYield', 'beta', 'profitMargins', 'operatingMargins',
                    'returnOnEquity', 'returnOnAssets', 'totalRevenue', 'grossProfits',
                    'ebitda', 'totalCash', 'totalDebt', 'sharesOutstanding'
                ]
                
                for key in fundamental_keys:
                    if key in info:
                        metrics[key] = info[key]
            
            return metrics
            
        except Exception as e:
            st.error(f"Error calculating financial metrics: {str(e)}")
            return {}
    
    def get_company_news(self, limit=5):
        """Fetch recent company news"""
        try:
            news = self.ticker.news
            return news[:limit] if news else []
        except Exception as e:
            st.warning(f"Could not fetch news: {str(e)}")
            return []
    
    def get_recommendations(self):
        """Fetch analyst recommendations"""
        try:
            recommendations = self.ticker.recommendations
            return recommendations
        except Exception as e:
            st.warning(f"Could not fetch recommendations: {str(e)}")
            return None
    
    def get_financials(self):
        """Fetch financial statements"""
        try:
            financials = {
                'income_statement': self.ticker.financials,
                'balance_sheet': self.ticker.balance_sheet,
                'cash_flow': self.ticker.cashflow
            }
            return financials
        except Exception as e:
            st.warning(f"Could not fetch financial statements: {str(e)}")
            return {}
