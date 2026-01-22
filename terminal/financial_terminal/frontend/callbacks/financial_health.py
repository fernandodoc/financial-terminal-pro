import streamlit as st
import pandas as pd

def render_financial_health():
    st.markdown("### 🏥 Check-up de Saúde Financeira (Diagnóstico Patrimonial)")
    st.caption("Insira os dados abaixo para gerar o relatório de saúde financeira do cliente.")

    # --- INPUTS DO CLIENTE EM UM FORMULÁRIO ---
    with st.form("diagnostico_form"):
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("##### 📦 Balanço Patrimonial")
            patrimonio_total = st.number_input("Patrimônio Líquido Total (R$)", value=300000.0, step=10000.0)
            dividas_totais = st.number_input("Total de Passivos/Dívidas (R$)", value=0.0, step=1000.0)
            custo_ativo = st.number_input("Capital Total Investido (Preço de Custo)", value=250000.0, step=10000.0)
            
        with col_b:
            st.markdown("##### 💸 Fluxo de Caixa")
            renda_mensal = st.number_input("Renda Mensal Líquida (Pró-labore/Salário)", value=20000.0, step=1000.0)
            gastos_mensais = st.number_input("Despesas Mensais Totais", value=12000.0, step=500.0)
            renda_passiva = st.number_input("Renda Passiva Mensal (Dividendos/Aluguéis)", value=1500.0, step=100.0)

        st.markdown("##### 📈 Premissas de Mercado")
        c1, c2 = st.columns(2)
        rentabilidade_ano = c1.slider("Rentabilidade Estimada da Carteira (% a.a.)", 0.0, 30.0, 12.5) / 100
        ipca_ano = c2.slider("IPCA Esperado (% a.a.)", 0.0, 15.0, 4.5) / 100

        # Botão de Execução
        submit_button = st.form_submit_button("Gerar Diagnóstico de Elite")

    # --- LÓGICA DE PROCESSAMENTO APÓS O "ENTER" (SUBMIT) ---
    if submit_button:
        # 1. Cálculos de Liquidez e Estrutura
        reserva_ideal = gastos_mensais * 6
        meses_reserva = patrimonio_total / gastos_mensais if gastos_mensais > 0 else 0
        taxa_endividamento = (dividas_totais / patrimonio_total) * 100 if patrimonio_total > 0 else 0
        
        # 2. Performance e Acúmulo
        savings_rate = ((renda_mensal - gastos_mensais) / renda_mensal) * 100 if renda_mensal > 0 else 0
        rentabilidade_real = ((1 + rentabilidade_ano) / (1 + ipca_ano)) - 1
        yoc = (renda_passiva * 12 / custo_ativo) * 100 if custo_ativo > 0 else 0
        cobertura_passiva = (renda_passiva / gastos_mensais) * 100 if gastos_mensais > 0 else 0
        
        # 3. Independência
        nif = (patrimonio_total / (gastos_mensais * 12)) if gastos_mensais > 0 else 0
        velocity_of_wealth = (patrimonio_total / custo_ativo) if custo_ativo > 0 else 1

        st.markdown("---")
        
        # --- EXIBIÇÃO DO RESULTADO ---
        st.subheader("📊 Relatório de Indicadores")

        tabs = st.tabs(["🛡️ Liquidez", "📈 Performance", "🏁 Independência"])

        with tabs[0]:
            c1, c2, c3 = st.columns(3)
            c1.metric("Reserva de Emergência", f"{meses_reserva:.1f} meses", delta=f"{meses_reserva - 6:.1f} vs Ideal")
            c2.metric("Liquidez Corrente", f"{meses_reserva/6:.2f}x", help="Acima de 1.0 é o ideal para segurança.")
            c3.metric("Endividamento", f"{taxa_endividamento:.1f}%", delta_color="inverse")
            
            if taxa_endividamento > 30:
                st.error("⚠️ Atenção: O nível de endividamento está acima do recomendado para o perfil Elite.")

        with tabs[1]:
            p1, p2, p3, p4 = st.columns(4)
            p1.metric("Savings Rate", f"{savings_rate:.1f}%")
            p2.metric("Rentabilidade Real", f"{rentabilidade_real*100:.2f}% a.a.")
            p3.metric("Yield on Cost", f"{yoc:.2f}%")
            p4.metric("Cobertura de Gastos", f"{cobertura_passiva:.1f}%")

        with tabs[2]:
            i1, i2, i3 = st.columns(3)
            i1.metric("Anos de Sobrevivência (NIF)", f"{nif:.1f} anos")
            i2.metric("Net Worth", f"R$ {patrimonio_total:,.2f}")
            i3.metric("Velocity of Wealth", f"{velocity_of_wealth:.2f}x")

        # Conclusão para o Cliente
        st.markdown("### 📝 Parecer do Especialista")
        if nif > 25:
            st.success(f"O cliente possui um patrimônio sólido que sustenta seu estilo de vida por {nif:.1f} anos. Foco em sucessão e otimização fiscal.")
        elif savings_rate > 30:
            st.info(f"Fase de acúmulo acelerada. Com um Savings Rate de {savings_rate:.1f}%, a estratégia deve focar em ativos de valor para potencializar o Velocity of Wealth.")
        else:
            st.warning("Recomendação: Revisar despesas operacionais para aumentar a capacidade de aporte mensal.")

# Não esqueça de importar e chamar no app.py