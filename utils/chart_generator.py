import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class ChartGenerator:
    """Class to generate various types of financial charts"""
    
    def __init__(self, data, symbol):
        self.data = data
        self.symbol = symbol
        self.colors = {
            'primary': '#00ff88',
            'secondary': '#ff6b6b',
            'background': '#0e1117',
            'text': '#fafafa',
            'grid': '#262730'
        }
    
    def create_line_chart(self):
        """Create an interactive line chart for stock price"""
        fig = go.Figure()
        
        # Add closing price line
        fig.add_trace(go.Scatter(
            x=self.data.index,
            y=self.data['Close'],
            mode='lines',
            name='Close Price',
            line=dict(color=self.colors['primary'], width=2),
            hovertemplate='<b>Date:</b> %{x}<br>' +
                         '<b>Price:</b> $%{y:.2f}<br>' +
                         '<extra></extra>'
        ))
        
        # Add moving averages if enough data
        if len(self.data) >= 20:
            ma20 = self.data['Close'].rolling(window=20).mean()
            fig.add_trace(go.Scatter(
                x=self.data.index,
                y=ma20,
                mode='lines',
                name='20-day MA',
                line=dict(color='orange', width=1, dash='dash'),
                hovertemplate='<b>20-day MA:</b> $%{y:.2f}<extra></extra>'
            ))
        
        if len(self.data) >= 50:
            ma50 = self.data['Close'].rolling(window=50).mean()
            fig.add_trace(go.Scatter(
                x=self.data.index,
                y=ma50,
                mode='lines',
                name='50-day MA',
                line=dict(color='red', width=1, dash='dot'),
                hovertemplate='<b>50-day MA:</b> $%{y:.2f}<extra></extra>'
            ))
        
        # Update layout
        fig.update_layout(
            title=f'{self.symbol} Stock Price',
            xaxis_title='Date',
            yaxis_title='Price ($)',
            template='plotly_dark',
            hovermode='x unified',
            showlegend=True,
            height=500,
            paper_bgcolor=self.colors['background'],
            plot_bgcolor=self.colors['background'],
            font=dict(color=self.colors['text'])
        )
        
        # Customize axes
        fig.update_xaxes(
            gridcolor=self.colors['grid'],
            showgrid=True
        )
        fig.update_yaxes(
            gridcolor=self.colors['grid'],
            showgrid=True,
            tickformat='$,.2f'
        )
        
        return fig
    
    def create_candlestick_chart(self):
        """Create an interactive candlestick chart"""
        fig = go.Figure()
        
        # Add candlestick chart
        fig.add_trace(go.Candlestick(
            x=self.data.index,
            open=self.data['Open'],
            high=self.data['High'],
            low=self.data['Low'],
            close=self.data['Close'],
            name=self.symbol,
            increasing_line_color=self.colors['primary'],
            decreasing_line_color=self.colors['secondary'],
            hoverinfo='x+y'
        ))
        
        # Add volume bars as subplot
        fig_with_volume = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            subplot_titles=(f'{self.symbol} Price', 'Volume'),
            row_width=[0.3, 0.7]
        )
        
        # Add candlestick to main plot
        fig_with_volume.add_trace(go.Candlestick(
            x=self.data.index,
            open=self.data['Open'],
            high=self.data['High'],
            low=self.data['Low'],
            close=self.data['Close'],
            name=self.symbol,
            increasing_line_color=self.colors['primary'],
            decreasing_line_color=self.colors['secondary']
        ), row=1, col=1)
        
        # Add volume bars
        colors = [self.colors['primary'] if close >= open else self.colors['secondary'] 
                 for close, open in zip(self.data['Close'], self.data['Open'])]
        
        fig_with_volume.add_trace(go.Bar(
            x=self.data.index,
            y=self.data['Volume'],
            name='Volume',
            marker_color=colors,
            opacity=0.7
        ), row=2, col=1)
        
        # Update layout
        fig_with_volume.update_layout(
            template='plotly_dark',
            showlegend=False,
            height=600,
            paper_bgcolor=self.colors['background'],
            plot_bgcolor=self.colors['background'],
            font=dict(color=self.colors['text'])
        )
        
        # Update axes
        fig_with_volume.update_xaxes(
            gridcolor=self.colors['grid'],
            showgrid=True
        )
        fig_with_volume.update_yaxes(
            title_text="Price ($)",
            gridcolor=self.colors['grid'],
            showgrid=True,
            tickformat='$,.2f',
            row=1, col=1
        )
        fig_with_volume.update_yaxes(
            title_text="Volume",
            gridcolor=self.colors['grid'],
            showgrid=True,
            row=2, col=1
        )
        
        return fig_with_volume
    
    def create_volume_chart(self):
        """Create a volume chart"""
        fig = go.Figure()
        
        # Color bars based on price movement
        colors = []
        for i in range(len(self.data)):
            if i == 0:
                colors.append(self.colors['primary'])
            else:
                if self.data['Close'].iloc[i] >= self.data['Close'].iloc[i-1]:
                    colors.append(self.colors['primary'])
                else:
                    colors.append(self.colors['secondary'])
        
        fig.add_trace(go.Bar(
            x=self.data.index,
            y=self.data['Volume'],
            name='Volume',
            marker_color=colors,
            opacity=0.8,
            hovertemplate='<b>Date:</b> %{x}<br>' +
                         '<b>Volume:</b> %{y:,.0f}<br>' +
                         '<extra></extra>'
        ))
        
        # Add volume moving average
        if len(self.data) >= 20:
            vol_ma = self.data['Volume'].rolling(window=20).mean()
            fig.add_trace(go.Scatter(
                x=self.data.index,
                y=vol_ma,
                mode='lines',
                name='20-day Volume MA',
                line=dict(color='white', width=2),
                hovertemplate='<b>Volume MA:</b> %{y:,.0f}<extra></extra>'
            ))
        
        # Update layout
        fig.update_layout(
            title=f'{self.symbol} Trading Volume',
            xaxis_title='Date',
            yaxis_title='Volume',
            template='plotly_dark',
            hovermode='x unified',
            showlegend=True,
            height=400,
            paper_bgcolor=self.colors['background'],
            plot_bgcolor=self.colors['background'],
            font=dict(color=self.colors['text'])
        )
        
        # Customize axes
        fig.update_xaxes(
            gridcolor=self.colors['grid'],
            showgrid=True
        )
        fig.update_yaxes(
            gridcolor=self.colors['grid'],
            showgrid=True,
            tickformat=',.'
        )
        
        return fig
    
    def create_returns_distribution(self):
        """Create a histogram of daily returns"""
        if len(self.data) < 2:
            return None
            
        daily_returns = self.data['Close'].pct_change().dropna() * 100
        
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=daily_returns,
            nbinsx=50,
            name='Daily Returns',
            marker_color=self.colors['primary'],
            opacity=0.7,
            hovertemplate='<b>Return Range:</b> %{x:.2f}%<br>' +
                         '<b>Frequency:</b> %{y}<br>' +
                         '<extra></extra>'
        ))
        
        # Add mean line
        mean_return = daily_returns.mean()
        fig.add_vline(
            x=mean_return,
            line_dash="dash",
            line_color="white",
            annotation_text=f"Mean: {mean_return:.2f}%"
        )
        
        # Update layout
        fig.update_layout(
            title=f'{self.symbol} Daily Returns Distribution',
            xaxis_title='Daily Return (%)',
            yaxis_title='Frequency',
            template='plotly_dark',
            showlegend=False,
            height=400,
            paper_bgcolor=self.colors['background'],
            plot_bgcolor=self.colors['background'],
            font=dict(color=self.colors['text'])
        )
        
        return fig
