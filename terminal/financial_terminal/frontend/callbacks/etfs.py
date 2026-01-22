import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

def render_etfs_analysis():
    st.markdown("### 🌍 Global & Factor ETFs Selection")
    st.caption("Análise de fundos de índice para diversificação internacional e setorial.")

    # --- FORMULÁRIO DE SELEÇÃO E COMPARAÇÃO ---
    with st.form("etf_form"):
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            etf_ticker = st.text_input("ETF Principal (ex: IVVB11.SA, BOVA11.SA, VOO)", value="IVVB11.SA").upper()
        with col2:
            benchmark = st.text_input("Benchmark para Comparar (ex: ^BVSP, SPY)", value="^BVSP").upper()
        with col3:
            periodo = st.selectbox("Período", ["6mo", "1y", "2y", "5y", "max"], index=1)
            
        submit_etf = st.form_submit_button("Comparar Performance")

    if submit_etf:
        try:
            # Coleta de dados (Normalizados para base 100 para comparação justa)
            data_etf = yf.download(etf_ticker, period=periodo)['Close']
            data_bench = yf.download(benchmark, period=periodo)['Close']

            if data_etf.empty or data_bench.empty:
                st.error("Erro ao buscar um dos ativos. Verifique os tickers.")
                return

            # Normalização (Base 100)
            etf_norm = (data_etf / data_etf.iloc[0]) * 100
            bench_norm = (data_bench / data_bench.iloc[0]) * 100

            # --- MÉTRICAS DE PERFORMANCE ---
            retorno_etf = ((data_etf.iloc[-1] / data_etf.iloc[0]) - 1) * 100
            retorno_bench = ((data_bench.iloc[-1] / data_bench.iloc[0]) - 1) * 100
            
            m1, m2, m3 = st.columns(3)
            m1.metric(f"Retorno {etf_ticker}", f"{retorno_etf:.2f}%")
            m2.metric(f"Retorno {benchmark}", f"{retorno_bench:.2f}%")
            m3.metric("Alpha (Diferença)", f"{retorno_etf - retorno_bench:.2f}%")

            # --- GRÁFICO DE PERFORMANCE RELATIVA ---
            st.markdown(f"#### {etf_ticker} vs {benchmark} (Base 100)")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=etf_norm.index, y=etf_norm, name=etf_ticker, line=dict(color='#58a6ff', width=2.5)))
            fig.add_trace(go.Scatter(x=bench_norm.index, y=bench_norm, name=benchmark, line=dict(color='#30363d', width=2, dash='dot')))
            
            fig.update_layout(
                template="plotly_dark",
                hovermode='x unified',
                margin=dict(l=0, r=0, t=20, b=0),
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)

            # --- INFO DO ATIVO ---
            info = yf.Ticker(etf_ticker).info
            with st.expander("📄 Detalhes Técnicos e Exposição"):
                c1, c2 = st.columns(2)
                c1.write(f"**Nome:** {info.get('longName', 'N/A')}")
                c1.write(f"**Taxa de Administração (ER):** {info.get('feesExpensesMax', 'N/A')}")
                c2.write(f"**Patrimônio Líquido:** $ {info.get('totalAssets', 0)/1e9:.2f}B")
                c2.write(f"**Categoria:** {info.get('category', 'Global Equity')}")

        except Exception as e:
            st.error(f"Erro no processamento: {e}")