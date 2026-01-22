import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

def render_funds_analysis():
    st.markdown("### 🏦 Screening de Fundos de Investimento")
    st.caption("Analise a performance de fundos de investimento contra seus benchmarks de referência.")

    # --- FORMULÁRIO DE BUSCA ---
    with st.form("funds_form"):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            # Nota: O Yahoo Finance usa o CNPJ ou Nome para alguns fundos com o sufixo .SA
            # Muitos fundos brasileiros estão disponíveis via tickers específicos
            fund_ticker = st.text_input("Ticker/CNPJ do Fundo (Ex: Alaska Black: ABPZ11.SA)", value="ABPZ11.SA").upper()
        with col2:
            benchmark = st.selectbox("Benchmark", ["CDI", "Ibovespa", "S&P 500"])
        with col3:
            periodo = st.selectbox("Período", ["1y", "2y", "5y", "max"], index=0)
        
        submit_fund = st.form_submit_button("Analisar Fundo")

    if submit_fund:
        try:
            # Coleta de dados do Fundo
            fund = yf.Ticker(fund_ticker)
            hist_fund = fund.history(period=periodo)['Close']
            
            if hist_fund.empty:
                st.error("Dados do fundo não encontrados. Verifique o ticker no Yahoo Finance.")
                return

            # Coleta de dados do Benchmark
            bench_ticker = "^BVSP" if benchmark == "Ibovespa" else "SPY"
            # Simplificação para CDI (usando uma aproximação de taxa fixa se necessário, 
            # mas aqui buscaremos o ativo de referência se disponível)
            hist_bench = yf.download(bench_ticker, period=periodo)['Close']

            # Normalização para Base 100 (Comparação de performance acumulada)
            fund_norm = (hist_fund / hist_fund.iloc[0]) * 100
            bench_norm = (hist_bench / hist_bench.iloc[0]) * 100

            # --- DASHBOARD DE MÉTRICAS ---
            ret_acum_fund = ((hist_fund.iloc[-1] / hist_fund.iloc[0]) - 1) * 100
            ret_acum_bench = ((hist_bench.iloc[-1] / hist_bench.iloc[0]) - 1) * 100
            
            m1, m2, m3 = st.columns(3)
            m1.metric(f"Retorno Acumulado", f"{ret_acum_fund:.2f}%")
            m2.metric(f"Retorno {benchmark}", f"{ret_acum_bench:.2f}%")
            m3.metric("Alpha/Beta", f"{ret_acum_fund - ret_acum_bench:.2f}%")

            # --- GRÁFICO DE PERFORMANCE ---
            st.markdown(f"#### Comparativo: {fund_ticker} vs {benchmark}")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=fund_norm.index, y=fund_norm, name="Fundo", line=dict(color='#58a6ff', width=3)))
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

            # --- ANÁLISE TÉCNICA (EXPANDER) ---
            with st.expander("📝 Detalhes sobre a Gestão"):
                info = fund.info
                st.write(f"**Gestora:** {info.get('longName', 'N/A')}")
                st.write(f"**Taxa de Administração:** {info.get('feesExpensesMax', 'N/A')}")
                st.write(f"**Objetivo:** {info.get('longBusinessSummary', 'Descrição não disponível.')}")

        except Exception as e:
            st.error(f"Erro ao processar dados: {e}")