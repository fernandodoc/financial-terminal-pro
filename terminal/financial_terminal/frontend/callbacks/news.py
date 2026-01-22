import streamlit as st

def render_news_portal():
    """Renderiza os cards de acesso aos jornais e portais financeiros."""
    
    # Estilização local para os cards de notícias
    st.markdown("""
        <style>
        .news-card {
            background-color: #161b22;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #30363d;
            text-align: center;
            height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            transition: 0.3s;
            margin-bottom: 15px;
        }
        .news-card:hover {
            border-color: #58a6ff;
            background-color: #1f2937;
        }
        .news-link {
            text-decoration: none;
            color: #58a6ff;
            font-weight: bold;
            font-size: 18px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.subheader("📰 Portais de Notícias & Terminais")
    
    # --- SEÇÃO NACIONAL ---
    st.markdown("#### 🇧🇷 Brasil")
    br_col1, br_col2, br_col3, br_col4 = st.columns(4)
    
    br_news = [
        ("InfoMoney", "https://www.infomoney.com.br/"),
        ("Valor Econômico", "https://valor.globo.com/"),
        ("Money Times", "https://www.moneytimes.com.br/"),
        ("InvestSite", "https://www.investsite.com.br/"),
        ("Investing BR", "https://br.investing.com/"),
        ("Fundamentus", "https://www.fundamentus.com.br/")
    ]

    cols = [br_col1, br_col2, br_col3, br_col4]
    for i, (name, url) in enumerate(br_news):
        with cols[i % 4]:
            st.markdown(f"""
                <div class="news-card">
                    <a href="{url}" target="_blank" class="news-link">{name}</a>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # --- SEÇÃO INTERNACIONAL ---
    st.markdown("#### 🌎 Global (Tier 1)")
    int_col1, int_col2, int_col3, int_col4 = st.columns(4)
    
    int_news = [
        ("Financial Times", "https://www.ft.com/"),
        ("Bloomberg", "https://www.bloomberg.com/markets"),
        ("The Economist", "https://www.economist.com/"),
        ("MarketWatch", "https://www.marketwatch.com/"),
        ("Investopedia", "https://www.investopedia.com/"),
        ("Reuters", "https://www.reuters.com/"),
        ("NY Times Finance", "https://www.nytimes.com/"),
        ("Barron's", "https://www.barrons.com/"),
        ("Investor's Business Daily", "https://www.investors.com/")
    ]

    cols_int = [int_col1, int_col2, int_col3, int_col4]
    for i, (name, url) in enumerate(int_news):
        with cols_int[i % 4]:
            st.markdown(f"""
                <div class="news-card">
                    <a href="{url}" target="_blank" class="news-link">{name}</a>
                </div>
            """, unsafe_allow_html=True)