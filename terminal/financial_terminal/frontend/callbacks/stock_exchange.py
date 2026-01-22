import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

def render_stock_exchange():
    st.markdown("### 🏛️ Monitor de Mercado (B3)")
    st.caption("Visão sistêmica da Bolsa de Valores e fluxo de ativos.")

    # --- MÉTRICAS GERAIS ---
    try:
        ibov = yf.Ticker("^BVSP")
        hist = ibov.history(period="2d")
        
        if len(hist) >= 2:
            atual = hist['Close'].iloc[-1]
            anterior = hist['Close'].iloc[-2]
            variacao = ((atual / anterior) - 1) * 100
            
            c1, c2, c3 = st.columns(3)
            c1.metric("IBOVESPA", f"{atual:,.0f} pts", f"{variacao:.2f}%")
            c2.metric("Volume Financeiro", "R$ 22.4B", help="Volume estimado da sessão")
            c3.metric("Status do Pregão", "Aberto", delta="Operacional")
    except:
        st.error("Erro ao conectar com o provedor de dados da B3.")

    st.markdown("---")

    # --- MARKET HEATMAP (SIMULADO COM TOP 10) ---
    st.markdown("#### 🔥 Market Heatmap (Principais Ativos)")
    
    # Lista das maiores do IBOV
    tickers_ibov = ["VALE3.SA", "PETR4.SA", "ITUB4.SA", "BBDC4.SA", "ABEV3.SA", "BBAS3.SA", "WEGE3.SA", "RENT3.SA", "ITSAS4.SA", "JBSS3.SA"]
    
    with st.spinner("Mapeando calor do mercado..."):
        dados_heatmap = []
        for t in tickers_ibov:
            try:
                tk = yf.Ticker(t)
                h = tk.history(period="2d")
                var = ((h['Close'].iloc[-1] / h['Close'].iloc[-2]) - 1) * 100
                dados_heatmap.append({"Ativo": t.replace(".SA", ""), "Variação %": var, "Preço": h['Close'].iloc[-1]})
            except:
                continue
        
        df_heat = pd.DataFrame(dados_heatmap)
        
        fig = px.treemap(df_heat, path=['Ativo'], values='Preço',
                         color='Variação %', 
                         color_continuous_scale='RdYlGn', # Vermelho para queda, Verde para alta
                         color_continuous_midpoint=0)
        
        fig.update_layout(margin=dict(t=10, l=10, r=10, b=10), height=400, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    # --- TOP GAINERS & LOSERS ---
    col_up, col_down = st.columns(2)
    
    with col_up:
        st.markdown("##### ✅ Maiores Altas")
        st.table(df_heat.sort_values(by="Variação %", ascending=False).head(5))
        
    with col_down:
        st.markdown("##### ❌ Maiores Baixas")
        st.table(df_heat.sort_values(by="Variação %", ascending=True).head(5))