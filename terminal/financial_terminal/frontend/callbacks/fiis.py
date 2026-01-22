import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

def render_fiis_analysis():
    st.markdown("### 🏢 Real Estate Intelligence (FIIs)")
    st.caption("Análise de Fundos Imobiliários: Renda Mensal e Avaliação Patrimonial.")

    # --- BUSCA DE FII ---
    with st.form("fii_search_form"):
        col1, col2 = st.columns([2, 1])
        with col1:
            fii_ticker = st.text_input("Ticker do FII (ex: HGLG11, KNRI11)", value="HGLG11").upper()
            if not fii_ticker.endswith(".SA"):
                fii_ticker += ".SA"
        with col2:
            periodo = st.selectbox("Período", ["1mo", "6mo", "1y", "5y"], index=2)
            submit_fii = st.form_submit_button("Analisar Fundo")

    if submit_fii:
        try:
            # Coleta de dados
            fii = yf.Ticker(fii_ticker)
            hist = fii.history(period=periodo)
            info = fii.info

            if hist.empty:
                st.error("Dados não encontrados para este ticker.")
                return

            # --- MÉTRICAS PRINCIPAIS ---
            price_current = hist['Close'].iloc[-1]
            dy = info.get('dividendYield', 0) * 100
            pvp = info.get('priceToBook', 0)
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Preço Atual", f"R$ {price_current:,.2f}")
            m2.metric("Dividend Yield (L12M)", f"{dy:.2f}%")
            m3.metric("P/VP", f"{pvp:.2f}", help="Abaixo de 1.00 indica que o fundo está sendo negociado com desconto.")
            m4.metric("Liquidez Diária", f"R$ {info.get('averageVolume', 0)/1e6:.1f}M")

            # --- GRÁFICO DE RENDIMENTO ---
            st.markdown("#### Evolução da Cota")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], name="Preço", line=dict(color='#58a6ff', width=2)))
            
            fig.update_layout(
                template="plotly_dark",
                margin=dict(l=0, r=0, t=20, b=0),
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)

            # --- ANÁLISE DO ASSESSOR ---
            st.markdown("#### 📋 Detalhes do Portfólio")
            d1, d2, d3 = st.columns(3)
            
            # Nota: Muitos dados de FIIs específicos (vacância, m2) exigem scrapers mais complexos 
            # ou APIs pagas, mas o Yahoo Finance nos dá o básico estrutural:
            d1.write(f"**Nome:** {info.get('longName', 'N/A')}")
            d2.write(f"**Setor:** {info.get('sector', 'Imobiliário')}")
            d3.write(f"**Próximo Dividendo:** R$ {info.get('dividendRate', 'N/A')}")

            # Lógica de Recomendação Visual
            if pvp < 1.0:
                st.success(f"💎 **Oportunidade:** O {fii_ticker[:-3]} está descontado em relação ao valor patrimonial (P/VP < 1).")
            elif pvp > 1.1:
                st.warning(f"⚠️ **Atenção:** O fundo está sendo negociado com um prêmio de {(pvp-1)*100:.0f}% sobre o valor real dos imóveis.")

        except Exception as e:
            st.error(f"Erro ao processar dados: {e}")