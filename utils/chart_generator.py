import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st

class ChartGenerator:
    """Class to generate interactive charts for stock data"""
    
    @staticmethod
    def create_price_chart(df: pd.DataFrame, symbol: str, chart_type: str = "line") -> go.Figure:
        """
        Create price chart (line or candlestick)
        
        Args:
            df (pd.DataFrame): Historical stock data
            symbol (str): Stock symbol
            chart_type (str): 'line' or 'candlestick'
            
        Returns:
            Plotly figure object
        """
        if df is None or df.empty:
            return go.Figure()
        
        if chart_type == "candlestick":
            fig = go.Figure(data=go.Candlestick(
                x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name=symbol,
                increasing=dict(line=dict(color='#00cc44')),  # Verde para subida
                decreasing=dict(line=dict(color='#ff4444'))
            ))
        else:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['Date'],
                y=df['Close'],
                mode='lines',
                name=f'{symbol} Price',
                line=dict(color='#2962ff', width=2)  # Azul para línea
            ))
        
        # Add moving averages with distinct colors
        ma_colors = ['#ff9500', '#9c27b0', '#00bcd4']  # Naranja, Morado, Cian
        ma_periods = [20, 50, 200]
        
        for i, period in enumerate(ma_periods):
            ma_col = f'MA_{period}'
            if ma_col in df.columns:
                fig.add_trace(go.Scatter(
                    x=df['Date'],
                    y=df[ma_col],
                    mode='lines',
                    name=f'MA {period}',
                    line=dict(color=ma_colors[i % len(ma_colors)], width=1.5, dash='dot'),
                    opacity=0.8
                ))
        
        fig.update_layout(
            title=f'{symbol} Stock Price Chart',
            xaxis_title='Date',
            yaxis_title='Price ($)',
            template='plotly_dark',
            height=500,
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        fig.update_xaxes(rangeslider_visible=False)
        
        return fig
    
    @staticmethod
    def create_volume_chart(df: pd.DataFrame, symbol: str) -> go.Figure:
        """
        Create volume chart with price movement indicators
        
        Args:
            df (pd.DataFrame): Historical stock data
            symbol (str): Stock symbol
            
        Returns:
            Plotly figure object
        """
        if df is None or df.empty:
            return go.Figure()
        
        # Calculate price movement
        df['Price_Change'] = df['Close'] - df['Open']
        df['Color'] = df['Price_Change'].apply(lambda x: '#00cc44' if x >= 0 else '#ff4444')
        
        fig = go.Figure()
        
        # Add volume bars
        fig.add_trace(go.Bar(
            x=df['Date'],
            y=df['Volume'],
            name='Volume',
            marker_color=df['Color'],
            opacity=0.7
        ))
        
        fig.update_layout(
            title=f'{symbol} Trading Volume',
            xaxis_title='Date',
            yaxis_title='Volume',
            template='plotly_dark',
            height=300,
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_financial_metrics_chart(metrics: dict) -> go.Figure:
        """
        Create a chart for key financial ratios
        
        Args:
            metrics (dict): Financial metrics dictionary
            
        Returns:
            Plotly figure object
        """
        # Extract numeric ratios for visualization
        ratio_metrics = {
            'P/E Ratio': metrics.get('P/E Ratio'),
            'Forward P/E': metrics.get('Forward P/E'),
            'PEG Ratio': metrics.get('PEG Ratio'),
            'Price to Book': metrics.get('Price to Book'),
            'Beta': metrics.get('Beta'),
            'ROE (%)': metrics.get('Return on Equity'),
            'ROA (%)': metrics.get('Return on Assets')
        }
        
        # Filter out non-numeric values
        valid_ratios = {}
        for key, value in ratio_metrics.items():
            if value != 'N/A' and value is not None:
                try:
                    if key in ['ROE (%)', 'ROA (%)'] and value:
                        # Convert to percentage if it's a decimal
                        numeric_value = float(value)
                        if numeric_value < 1:
                            numeric_value *= 100
                        valid_ratios[key] = numeric_value
                    else:
                        valid_ratios[key] = float(value)
                except (ValueError, TypeError):
                    continue
        
        if not valid_ratios:
            return go.Figure()
        
        fig = go.Figure(data=go.Bar(
            x=list(valid_ratios.keys()),
            y=list(valid_ratios.values()),
            marker_color='#00ff88',
            opacity=0.8
        ))
        
        fig.update_layout(
            title='Key Financial Ratios',
            xaxis_title='Metrics',
            yaxis_title='Value',
            template='plotly_dark',
            height=400,
            xaxis={'tickangle': -45}
        )
        
        return fig
    
    @staticmethod
    def create_price_change_indicator(current_price: float, previous_close: float) -> dict:
        """
        Create price change indicator data
        
        Args:
            current_price (float): Current stock price
            previous_close (float): Previous closing price
            
        Returns:
            Dictionary with change data
        """
        if current_price == 'N/A' or previous_close == 'N/A':
            return {'change': 'N/A', 'change_percent': 'N/A', 'color': '#ffffff'}
        
        try:
            change = current_price - previous_close
            change_percent = (change / previous_close) * 100
            color = '#00ff88' if change >= 0 else '#ff6b6b'
            
            return {
                'change': round(change, 2),
                'change_percent': round(change_percent, 2),
                'color': color
            }
        except (TypeError, ZeroDivisionError):
            return {'change': 'N/A', 'change_percent': 'N/A', 'color': '#ffffff'}
