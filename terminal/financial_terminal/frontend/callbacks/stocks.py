import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

def render_stocks_analysis():
    st.markdown("### 📈 Análise de Ativos (B3 & Global)")
    
    # Barra de busca estilizada
    col_search1, col_search2 = st.columns([1, 3])
    with col_search1:
        ticker = st.text_input("Ticker do Ativo", value="PETR4.SA", help="Exemplo: PETR4.SA, VALE3.SA, AAPL").upper()
    
    with col_search2:
        periodo = st.selectbox("Período de Análise", 
                              options=["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"], 
                              index=3)

    if ticker:
        try:
            # Busca de dados
            asset = yf.Ticker(ticker)
            hist = asset.history(period=periodo)
            info = asset.info

            if hist.empty:
                st.error("Ativo não encontrado ou sem dados disponíveis.")
                return

            # Linha de Métricas Principais (Preço, Variação, Dividend Yield)
            price_current = hist['Close'].iloc[-1]
            price_open = hist['Open'].iloc[-1]
            change = price_current - hist['Close'].iloc[-2]
            change_pct = (change / hist['Close'].iloc[-2]) * 100

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Preço Atual", f"R$ {price_current:,.2f}", f"{change_pct:.2f}%")
            m2.metric("Mín. 52 Semanas", f"R$ {info.get('fiftyTwoWeekLow', 0):,.2f}")
            m3.metric("Máx. 52 Semanas", f"R$ {info.get('fiftyTwoWeekHigh', 0):,.2f}")
            m4.metric("Dividend Yield", f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else "N/A")

            # Gráfico de Candlestick Profissional
            fig = go.Figure(data=[go.Candlestick(
                x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'],
                name=ticker
            )])

            # Adicionando Média Móvel de 20 e 50 dias (Visão de Especialista)
            hist['MA20'] = hist['Close'].rolling(window=20).mean()
            hist['MA50'] = hist['Close'].rolling(window=50).mean()
            
            fig.add_trace(go.Scatter(x=hist.index, y=hist['MA20'], name='MMS 20', line=dict(color='#58a6ff', width=1.5)))
            fig.add_trace(go.Scatter(x=hist.index, y=hist['MA50'], name='MMS 50', line=dict(color='#f85149', width=1.5)))

            fig.update_layout(
                template="plotly_dark",
                xaxis_rangeslider_visible=False,
                margin=dict(l=10, r=10, t=10, b=10),
                height=450,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)

            # Resumo Fundamentalista (O que o cliente quer saber)
            with st.expander("🔍 Indicadores de Valor e Saúde Financeira"):
                f1, f2, f3 = st.columns(3)
                f1.write(f"**P/L:** {info.get('trailingPE', 'N/A')}")
                f1.write(f"**P/VP:** {info.get('priceToBook', 'N/A')}")
                
                f2.write(f"**Margem Líquida:** {info.get('profitMargins', 0)*100:.2f}%")
                f2.write(f"**ROE:** {info.get('returnOnEquity', 0)*100:.2f}%")
                
                f3.write(f"**Dívida Líquida/EBITDA:** {info.get('debtToEquity', 'N/A')}")
                f3.write(f"**Payout:** {info.get('payoutRatio', 0)*100:.2f}%")

        except Exception as e:
            st.warning(f"Não foi possível carregar todos os indicadores fundamentalistas para {ticker}, mas os dados de preço estão ativos.")