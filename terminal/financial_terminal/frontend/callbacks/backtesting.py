import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def render_backtesting_analysis():
    st.markdown("### 🧪 Laboratório de Backtesting (Simulação Histórica)")
    st.caption("Teste sua estratégia de alocação no passado para entender o risco e o retorno potencial.")

    # --- CONFIGURAÇÃO DA CARTEIRA ---
    with st.form("backtest_form"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            tickers_input = st.text_input("Ativos da Carteira (separados por vírgula)", value="IVVB11.SA, BOVA11.SA, SMAL11.SA").upper()
            tickers = [t.strip() for t in tickers_input.split(",")]
        
        with col2:
            periodo = st.selectbox("Janela de Tempo", ["2y", "5y", "10y", "max"], index=1)

        st.markdown("##### Defina os Pesos (Devem somar 100%)")
        pesos = []
        cols_pesos = st.columns(len(tickers))
        for i, ticker in enumerate(tickers):
            with cols_pesos[i]:
                peso = st.number_input(f"% {ticker}", min_value=0, max_value=100, value=100//len(tickers))
                pesos.append(peso / 100)

        submit_bt = st.form_submit_button("Rodar Backtest")

    if submit_bt:
        if sum(pesos) < 0.99 or sum(pesos) > 1.01:
            st.error("A soma dos pesos deve ser exatamente 100%.")
            return

        try:
            with st.spinner("Processando dados históricos..."):
                # Download dos dados
                data = yf.download(tickers, period=periodo)['Close']
                benchmark = yf.download("^BVSP", period=periodo)['Close']

                # Cálculo de Retornos Diários
                retornos_diarios = data.pct_change().dropna()
                
                # Cálculo da Carteira (Soma ponderada dos retornos)
                carteira_retorno = (retornos_diarios * pesos).sum(axis=1)
                
                # Evolução Patrimonial (Base 100)
                carteira_acumulada = (1 + carteira_retorno).cumprod() * 100
                bench_acumulado = (1 + benchmark.pct_change().dropna()).cumprod() * 100

                # --- MÉTRICAS DE RISCO/RETORNO ---
                retorno_total = (carteira_acumulada.iloc[-1] / 100) - 1
                volatilidade = carteira_retorno.std() * np.sqrt(252) # Anualizada
                drawdown = (carteira_acumulada / carteira_acumulada.cummax()) - 1
                max_drawdown = drawdown.min()

                st.markdown("---")
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Retorno Acumulado", f"{retorno_total*100:.2f}%")
                m2.metric("Volatilidade (a.a.)", f"{volatilidade*100:.2f}%")
                m3.metric("Max Drawdown (Queda Máx)", f"{max_drawdown*100:.2f}%", delta_color="inverse")
                m4.metric("Sharpe Ratio", f"{(retorno_total / volatilidade):.2f}")

                # --- GRÁFICO DE EVOLUÇÃO ---
                st.markdown("#### Performance da Estratégia vs Ibovespa")
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=carteira_acumulada.index, y=carteira_acumulada, name="Minha Carteira", line=dict(color='#58a6ff', width=3)))
                fig.add_trace(go.Scatter(x=bench_acumulado.index, y=bench_acumulado, name="Ibovespa", line=dict(color='#30363d', width=2, dash='dot')))
                
                fig.update_layout(template="plotly_dark", hovermode='x unified', margin=dict(l=0,r=0,t=20,b=0), height=400)
                st.plotly_chart(fig, use_container_width=True)

                # --- GRÁFICO DE DRAWDOWN ---
                st.markdown("#### Histórico de Quedas (Drawdown)")
                fig_dd = go.Figure()
                fig_dd.add_trace(go.Scatter(x=drawdown.index, y=drawdown*100, fill='tozeroy', name="Drawdown", line=dict(color='#f85149')))
                fig_dd.update_layout(template="plotly_dark", yaxis_title="% de Queda", height=250)
                st.plotly_chart(fig_dd, use_container_width=True)

        except Exception as e:
            st.error(f"Erro ao processar backtest: {e}")