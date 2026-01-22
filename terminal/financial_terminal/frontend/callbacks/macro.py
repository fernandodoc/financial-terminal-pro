import streamlit as st

def render_macro_panel():
    # Estilização para métricas compactas
    st.markdown("""
        <style>
        .macro-section {
            background-color: #161b22;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 5px solid #58a6ff;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- CATEGORIA 1: BRASIL ---
    with st.expander("🇧🇷 Macro Brasil", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        # Aqui no futuro chamaremos get_brazil_macro_data()
        col1.metric("Selic Meta", "11.25%", "0.00%")
        col2.metric("IPCA (12m)", "4.51%", "+0.12%")
        col3.metric("Ibovespa", "128.520", "+1.2%")
        col4.metric("Dólar Ptax", "R$ 4,92", "-0.5%")

    # --- CATEGORIA 2: GLOBAL EQUITIES ---
    with st.expander("🌎 Macro Global - Equities"):
        col1, col2, col3 = st.columns(3)
        col1.metric("MSCI World", "3.240", "+0.5%")
        col2.metric("Euro Stoxx 50", "4.620", "-0.2%")
        col3.metric("Nikkei 225", "36.150", "+1.1%")

    # --- CATEGORIA 3: VOLATILIDADE E RISCO ---
    with st.expander("⚠️ Volatilidade e Risco Sistêmico"):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("VIX (Fear Index)", "13.45", "-2.1%")
        c2.metric("MOVE Index", "105.2", "+1.5%") # Essencial para Renda Fixa
        c3.metric("Skew Index", "145.2", "High")
        c4.metric("Financial Stress", "-0.52", "Stable")

    # --- CATEGORIA 4: JUROS E POLÍTICA MONETÁRIA ---
    with st.expander("🏦 Juros Globais e Bonds"):
        c1, c2, c3 = st.columns(3)
        c1.metric("US 10Y Treasury", "4.15%", "+0.02")
        c2.metric("US 2Y Treasury", "4.45%", "-0.01")
        c3.metric("Spread 2Y-10Y", "-0.30", "Inverted")

    # --- CATEGORIA 5: COMMODITIES ---
    with st.expander("⛽ Commodities Estratégicas"):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Petróleo Brent", "$ 82.30", "+0.8%")
        c2.metric("Ouro (Oz)", "$ 2.030", "-0.1%")
        c3.metric("Cobre", "$ 3.85", "+0.4%")
        c4.metric("CRB Index", "275.4", "+0.2%")