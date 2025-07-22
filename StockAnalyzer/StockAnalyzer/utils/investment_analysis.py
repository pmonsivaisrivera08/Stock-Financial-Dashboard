import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
import random

class InvestmentAnalysis:
    """Class to generate investment analysis components similar to trading platforms"""
    
    @staticmethod
    def create_fair_value_indicator(current_price: float, fair_value: Optional[float] = None) -> dict:
        """
        Create fair value assessment
        
        Args:
            current_price: Current stock price
            fair_value: Calculated fair value (if None, estimate based on current price)
        
        Returns:
            Dictionary with fair value analysis
        """
        if fair_value is None:
            # Estimate fair value with some variation
            fair_value = current_price * (0.95 + random.random() * 0.1)
        
        difference = current_price - fair_value
        percentage_diff = (difference / fair_value) * 100
        
        if percentage_diff < -10:
            status = "Subvalorado"
            color = "#00cc44"  # Verde
            recommendation = "Compra fuerte"
        elif percentage_diff < -5:
            status = "Algo subvalorado"
            color = "#00cc44"  # Verde
            recommendation = "Compra"
        elif percentage_diff < 5:
            status = "Valor razonable"
            color = "#ffaa00"  # Amarillo
            recommendation = "Mantener"
        elif percentage_diff < 10:
            status = "Algo sobrevalorado"
            color = "#ff4444"  # Rojo
            recommendation = "Precaución"
        else:
            status = "Sobrevalorado"
            color = "#ff4444"  # Rojo
            recommendation = "Venta"
        
        return {
            'current_price': current_price,
            'fair_value': fair_value,
            'difference': difference,
            'percentage_diff': percentage_diff,
            'status': status,
            'color': color,
            'recommendation': recommendation
        }
    
    @staticmethod
    def create_price_range_widget(symbol: str, current_price: float, day_low: float, day_high: float, 
                                week52_low: float, week52_high: float) -> None:
        """
        Create price range indicators similar to the image
        
        Args:
            symbol: Stock symbol
            current_price: Current price
            day_low: Day's low price
            day_high: Day's high price
            week52_low: 52-week low
            week52_high: 52-week high
        """
        st.markdown("#### 📊 Rangos de Precio")
        
        # Daily range
        st.markdown("**Rango diario**")
        day_progress = (current_price - day_low) / (day_high - day_low) if day_high > day_low else 0.5
        
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.write(f"${day_low:.2f}")
        with col2:
            st.progress(day_progress)
        with col3:
            st.write(f"${day_high:.2f}")
        
        # 52-week range
        st.markdown("**52 semanas**")
        year_progress = (current_price - week52_low) / (week52_high - week52_low) if week52_high > week52_low else 0.5
        
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.write(f"${week52_low:.2f}")
        with col2:
            st.progress(year_progress)
        with col3:
            st.write(f"${week52_high:.2f}")
    
    @staticmethod
    def create_analyst_opinion_widget(symbol: str, current_price: float) -> None:
        """
        Create analyst opinion widget
        
        Args:
            symbol: Stock symbol
            current_price: Current stock price
        """
        # Simulate analyst data
        target_price = current_price * (1.05 + random.random() * 0.1)
        upside = ((target_price - current_price) / current_price) * 100
        
        recommendations = ["Compra fuerte", "Compra", "Mantener", "Venta", "Venta fuerte"]
        weights = [0.3, 0.4, 0.2, 0.08, 0.02]  # Bias towards buy recommendations
        recommendation = np.random.choice(recommendations, p=weights)
        
        st.markdown("#### 📈 Opinión de los Analistas")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            if recommendation in ["Compra fuerte", "Compra"]:
                st.success(f"🟢 **{recommendation}**")
            elif recommendation == "Mantener":
                st.warning(f"🟡 **{recommendation}**")
            else:
                st.error(f"🔴 **{recommendation}**")
        
        st.markdown("**Precio objetivo**")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Precio objetivo", f"${target_price:.2f}")
        with col2:
            st.metric("Al alza", f"+{upside:.2f}%", delta=f"+{upside:.1f}%")
    
    @staticmethod
    def create_technical_analysis_gauge(symbol: str) -> None:
        """
        Create technical analysis gauge similar to the image
        
        Args:
            symbol: Stock symbol
        """
        # Simulate technical analysis score (0-100)
        tech_score = random.randint(60, 85)  # Bias towards positive
        
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = tech_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Análisis Técnico"},
            delta = {'reference': 50},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#262730"},
                'steps': [
                    {'range': [0, 30], 'color': "#ff4444"},    # Rojo
                    {'range': [30, 70], 'color': "#ffaa00"},   # Amarillo
                    {'range': [70, 100], 'color': "#00cc44"}  # Verde
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': tech_score
                }
            }
        ))
        
        fig.update_layout(
            height=200,
            width=280,
            template='plotly_dark',
            font={'color': "white", 'family': "Arial", 'size': 12},
            margin=dict(l=10, r=10, t=30, b=10),
            showlegend=False
        )
        
        if tech_score >= 70:
            recommendation = "Compra fuerte"
            color = "#00cc44"  # Verde
        elif tech_score >= 50:
            recommendation = "Compra"
            color = "#ffaa00"  # Amarillo
        else:
            recommendation = "Precaución"
            color = "#ff4444"  # Rojo
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.plotly_chart(fig, use_container_width=False)
        with col2:
            st.markdown("#### Señal Técnica")
            if recommendation == "Compra fuerte":
                st.success(f"🟢 **{recommendation}**")
            elif recommendation == "Compra":
                st.warning(f"🟡 **{recommendation}**")
            else:
                st.error(f"🔴 **{recommendation}**")
            
            # Add score display
            st.metric("Puntuación", f"{tech_score}/100")
    
    @staticmethod
    def create_sentiment_widget(symbol: str) -> None:
        """
        Create market sentiment widget
        
        Args:
            symbol: Stock symbol
        """
        # Simulate sentiment data
        sentiments = ["Bajista", "Neutral", "Alcista"]
        weights = [0.2, 0.3, 0.5]
        current_sentiment = np.random.choice(sentiments, p=weights)
        
        st.markdown("#### 📊 Sentimientos del Mercado")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if current_sentiment == "Bajista":
                st.error("🐻 **Bajista**")
            else:
                st.markdown("🐻 Bajista")
        
        with col2:
            if current_sentiment == "Alcista":
                st.success("🐂 **Alcista**")
            else:
                st.markdown("🐂 Alcista")
                
        # Show current sentiment prominently
        if current_sentiment == "Alcista":
            st.success(f"🚀 Sentimiento actual: **{current_sentiment}**")
        elif current_sentiment == "Bajista":
            st.error(f"📉 Sentimiento actual: **{current_sentiment}**")
        else:
            st.info(f"⚖️ Sentimiento actual: **{current_sentiment}**")
    
    @staticmethod
    def create_company_health_card(symbol: str, metrics: Dict[str, Any]) -> None:
        """
        Create company health assessment card
        
        Args:
            symbol: Stock symbol
            metrics: Financial metrics dictionary
        """
        st.markdown("#### 🏥 Salud de la Empresa")
        
        # Calculate health score based on available metrics
        health_factors = []
        
        # Debt to Equity (lower is better)
        debt_to_equity = metrics.get('Debt to Equity', 'N/A')
        if debt_to_equity != 'N/A' and debt_to_equity is not None:
            try:
                de_ratio = float(debt_to_equity)
                if de_ratio < 0.3:
                    health_factors.append(90)
                elif de_ratio < 0.6:
                    health_factors.append(70)
                elif de_ratio < 1.0:
                    health_factors.append(50)
                else:
                    health_factors.append(30)
            except:
                pass
        
        # ROE (higher is better)
        roe = metrics.get('Return on Equity', 'N/A')
        if roe != 'N/A' and roe is not None:
            try:
                roe_value = float(roe)
                if roe_value < 0:
                    roe_value = roe_value * 100  # Convert to percentage if needed
                if roe_value > 15:
                    health_factors.append(90)
                elif roe_value > 10:
                    health_factors.append(70)
                elif roe_value > 5:
                    health_factors.append(50)
                else:
                    health_factors.append(30)
            except:
                pass
        
        # Calculate overall health score
        if health_factors:
            health_score = sum(health_factors) / len(health_factors)
        else:
            health_score = random.randint(60, 85)  # Default if no data
        
        # Health status
        if health_score >= 80:
            status = "Excelente"
            color = "#00cc44"  # Verde
        elif health_score >= 60:
            status = "Buena"
            color = "#ffaa00"  # Amarillo
        elif health_score >= 40:
            status = "Regular"
            color = "#ff9500"  # Naranja
        else:
            status = "Preocupante"
            color = "#ff4444"  # Rojo
        
        # Create health assessment using native Streamlit components
        st.markdown("**Estado de Salud de la Empresa**")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.progress(health_score/100)
        with col2:
            st.metric("Salud", f"{health_score:.0f}/100", delta=None)
        
        # Show status without background
        if health_score >= 80:
            st.success(f"🟢 {status}")
        elif health_score >= 60:
            st.warning(f"🟡 {status}")
        elif health_score >= 40:
            st.warning(f"🟠 {status}")
        else:
            st.error(f"🔴 {status}")
    
    @staticmethod
    def create_investment_summary_card(symbol: str, current_price: float, metrics: Dict[str, Any]) -> None:
        """
        Create investment summary card with key insights
        
        Args:
            symbol: Stock symbol
            current_price: Current stock price
            metrics: Financial metrics dictionary
        """
        st.markdown("#### 💡 Resumen de Inversión")
        
        # Get fair value analysis
        fair_value_data = InvestmentAnalysis.create_fair_value_indicator(current_price)
        
        # Create investment summary using native Streamlit components
        st.markdown(f"#### 🎯 {symbol} Análisis de Inversión")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Precio Actual", f"${current_price:.2f}")
            st.metric("Valor Razonable", f"${fair_value_data['fair_value']:.2f}")
        with col2:
            # Show recommendation with appropriate styling
            if fair_value_data['recommendation'] in ["Compra fuerte", "Compra"]:
                st.success(f"🟢 {fair_value_data['recommendation']}")
            elif fair_value_data['recommendation'] == "Mantener":
                st.warning(f"🟡 {fair_value_data['recommendation']}")
            else:
                st.error(f"🔴 {fair_value_data['recommendation']}")
                
            # Show status
            st.write(f"**Estado:** {fair_value_data['status']}")
        
        # Show difference
        diff_percentage = fair_value_data['percentage_diff']
        if diff_percentage > 0:
            st.error(f"🔴 Sobrevalorado por {diff_percentage:.1f}%")
        elif diff_percentage < -5:
            st.success(f"🟢 Subvalorado por {abs(diff_percentage):.1f}%")
        else:
            st.warning(f"🟡 Cerca del valor razonable ({diff_percentage:+.1f}%)")