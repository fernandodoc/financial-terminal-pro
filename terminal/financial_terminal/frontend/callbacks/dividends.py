import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

def render_dividends_analysis():
    st.markdown("### 💰 Mapa de Renda Passiva e Dividendos")
    st.caption("Analise o histórico de proventos e a sustentabilidade da renda gerada pelos ativos.")

    # --- FORMULÁRIO DE ENTRADA ---
    with st.form("dividends_form"):
        col1, col2 = st.columns([2, 1])
        with col1:
            ticker = st.text_input("Ticker do Ativo (ex: BBAS3.SA, PETR4.SA, VOO)", value="BBAS3.SA").upper()
            if not ticker.endswith(".SA") and len(ticker) == 5: # Auto-complete para B3
                ticker += ".SA"
        with col2:
            periodo = st.selectbox("Histórico", ["2y", "5y", "10y", "max"], index=1)
            submit_div = st.form_submit_button("Mapear Proventos")

    if submit_div:
        try:
            asset = yf.Ticker(ticker)
            # Buscar dividendos
            divs = asset.actions['Dividends']
            
            if divs.empty:
                st.warning(f"O ativo {ticker} não possui histórico de dividendos registrado ou é um ativo de crescimento.")
                return

            # Processamento de Dados
            df_divs = divs.to_frame().reset_index()
            df_divs['Year'] = df_divs['Date'].dt.year
            df_annual = df_divs.groupby('Year')['Dividends'].sum().reset_index()

            # --- MÉTRICAS DE ELITE ---
            info = asset.info
            current_price = info.get('previousClose', 1)
            dy_current = info.get('dividendYield', 0) * 100
            payout = info.get('payoutRatio', 0) * 100
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Dividend Yield (Atual)", f"{dy_current:.2f}%")
            m2.metric("Payout Ratio", f"{payout:.1f}%", help="Porcentagem do lucro líquido paga em dividendos.")
            m3.metric("Dividendos L12M", f"R$ {df_divs.tail(4)['Dividends'].sum():.2f}")

            # --- GRÁFICO DE EVOLUÇÃO ANUAL ---
            st.markdown("#### 📈 Evolução Anual de Proventos")
            fig = px.bar(df_annual, x='Year', y='Dividends', 
                         title=f"Total de Dividendos por Ano - {ticker}",
                         color_discrete_sequence=['#58a6ff'])
            
            fig.update_layout(
                template="plotly_dark",
                xaxis_title="Ano",
                yaxis_title="R$ por Ação",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)

            # --- TABELA DE PROVENTOS RECENTES ---
            with st.expander("📅 Histórico Detalhado (Últimos Lançamentos)"):
                st.dataframe(df_divs.sort_values(by='Date', ascending=False).head(10), 
                             use_container_width=True)

            # --- INSIGHT DO ASSESSOR ---
            st.markdown("#### 💡 Análise de Sustentabilidade")
            if payout > 80:
                st.error(f"**Payout Elevado ({payout:.1f}%):** A empresa distribui quase todo o lucro. Espaço limitado para crescimento orgânico.")
            elif payout < 20 and payout > 0:
                st.info(f"**Retenção de Lucro:** Empresa foca em crescimento. Dividendos podem ser baixos agora, mas visam valorização futura.")
            else:
                st.success(f"**Equilíbrio:** O payout de {payout:.1f}% sugere uma política de dividendos sustentável e saudável.")

        except Exception as e:
            st.error(f"Erro ao buscar dados de proventos: {e}")