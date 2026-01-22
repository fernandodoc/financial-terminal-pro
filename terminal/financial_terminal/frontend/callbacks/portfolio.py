import streamlit as st

def render_portfolio_vision():
    # Estilização de Luxo para a seção de Portfólio
    st.markdown("""
        <style>
        .portfolio-header {
            background: linear-gradient(90deg, #161b22 0%, #0d1117 100%);
            padding: 40px;
            border-radius: 15px;
            border-left: 8px solid #58a6ff;
            margin-bottom: 30px;
        }
        .contact-card {
            background-color: #1c2128;
            padding: 30px;
            border-radius: 10px;
            border: 1px solid #30363d;
            margin-top: 40px;
        }
        .highlight {
            color: #58a6ff;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- VISÃO ESTRATÉGICA ---
    st.markdown("""
        <div class="portfolio-header">
            <h1>💼 Gestão de Portfólio de Elite</h1>
            <p style='font-size: 1.2rem; line-height: 1.6;'>
                A construção de um patrimônio superior a <span class="highlight">R$ 300.000,00</span> exige mais do que a simples escolha de ativos. 
                Requer uma arquitetura financeira que equilibre <b>Otimização de Rentabilidade</b>, <b>Eficiência Fiscal</b> e a <b>Proteção de Legado</b>.
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎯 O Tripé da Gestão Profissional")
        st.write("""
        1. **Eficiência Fiscal:** Não se trata de quanto você ganha, mas de quanto você mantém. Estruturas que minimizam o impacto tributário são fundamentais para o crescimento composto.
        2. **Blindagem Patrimonial:** Proteção contra riscos sistêmicos e jurisdicionais, garantindo que o capital esteja seguro para as próximas gerações.
        3. **Transmissão de Legado:** Um planejamento sucessório inteligente evita a dilapidação do patrimônio em processos burocráticos e onerosos.
        """)

    with col2:
        st.markdown("### ⚖️ O Papel do Especialista")
        st.info("""
        O mercado financeiro é complexo e ruidoso. Um profissional certificado (**C-PRO, ANCORD**) atua como um filtro, removendo o viés emocional e aplicando modelos matemáticos para buscar a fronteira eficiente de risco e retorno.
        
        **A tecnologia fornece os dados, mas o estrategista fornece a direção.**
        """)

    st.markdown("---")

    # --- FORMULÁRIO DE CONTATO (CTA) ---
    st.markdown("<div class='contact-card'>", unsafe_allow_html=True)
    st.subheader("🚀 Solicitar Diagnóstico de Portfólio")
    st.write("Agende uma consultoria técnica para estruturar sua carteira de forma profissional.")

    with st.form("contact_professional"):
        c1, c2 = st.columns(2)
        nome = c1.text_input("Nome Completo")
        email = c2.text_input("E-mail Estratégico")
        
        c3, c4 = st.columns(2)
        telefone = c3.text_input("WhatsApp para Contato")
        faixa_patrimonial = c4.selectbox("Patrimônio Estimado", [
            "R$ 300k - R$ 1M", 
            "R$ 1M - R$ 5M", 
            "Acima de R$ 5M"
        ])
        
        mensagem = st.text_area("Objetivo Principal (ex: Sucessão, Renda, Alocação Global)")
        
        submit_contact = st.form_submit_button("Enviar Dados ao Especialista")
        
        if submit_contact:
            if nome and email and telefone:
                st.success(f"Obrigado, {nome}! Seus dados foram enviados com prioridade. O especialista entrará em contato em breve.")
                # Aqui você poderia integrar com uma API de e-mail ou Telegram
            else:
                st.error("Por favor, preencha os campos essenciais para o contato.")
    
    st.markdown("</div>", unsafe_allow_html=True)