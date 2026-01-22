import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def render_compound_interest():
    st.markdown("### ⏳ Simulador de Projeção Patrimonial")
    st.caption("Insira os parâmetros para calcular a evolução do capital no tempo.")

    # --- FORMULÁRIO DE ENTRADA ---
    with st.form("compound_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("##### 🏦 Capital")
            capital_inicial = st.number_input("Capital Inicial (R$)", value=300000.0, step=10000.0)
            aporte_mensal = st.number_input("Aporte Mensal (R$)", value=5000.0, step=500.0)
            
        with col2:
            st.markdown("##### 📈 Taxas (% a.a.)")
            taxa_anual = st.number_input("Rentabilidade Estimada", value=12.0, step=0.5) / 100
            inflacao_anual = st.number_input("IPCA Estimado", value=4.5, step=0.1) / 100
            
        with col3:
            st.markdown("##### 📅 Prazo")
            anos = st.slider("Tempo (Anos)", 1, 40, 20)
            st.write("") # Espaçador
            submit_button = st.form_submit_button("Simular Crescimento")

    # --- LÓGICA DE PROCESSAMENTO (PÓS-ENTER) ---
    if submit_button:
        # Fórmulas de conversão para mensal
        taxa_mensal = (1 + taxa_anual)**(1/12) - 1
        inflacao_mensal = (1 + inflacao_anual)**(1/12) - 1
        meses = anos * 12
        
        dados = []
        saldo_nominal = capital_inicial
        total_investido = capital_inicial
        
        for mes in range(1, meses + 1):
            juros_mes = saldo_nominal * taxa_mensal
            saldo_nominal += juros_mes + aporte_mensal
            total_investido += aporte_mensal
            
            # Valor Real (Poder de Compra descontando inflação)
            poder_compra = saldo_nominal / ((1 + inflacao_mensal) ** mes)
            
            if mes % 12 == 0:  # Dados anuais para o gráfico
                dados.append({
                    "Ano": mes // 12,
                    "Total Investido": total_investido,
                    "Juros Acumulados": saldo_nominal - total_investido,
                    "Patrimônio Nominal": saldo_nominal,
                    "Poder de Compra (Real)": poder_compra
                })

        df = pd.DataFrame(dados)

        # --- EXIBIÇÃO DOS RESULTADOS ---
        st.markdown("---")
        res1, res2, res3 = st.columns(3)
        
        final_nominal = df['Patrimônio Nominal'].iloc[-1]
        final_real = df['Poder de Compra (Real)'].iloc[-1]
        total_juros = df['Juros Acumulados'].iloc[-1]

        res1.metric("Montante Final (Nominal)", f"R$ {final_nominal:,.2f}")
        res2.metric("Poder de Compra Real", f"R$ {final_real:,.2f}", 
                   delta=f"Corrosão: {((final_real/final_nominal)-1)*100:.1f}%", delta_color="inverse")
        res3.metric("Total em Juros", f"R$ {total_juros:,.2f}")

        # --- GRÁFICO PROFISSIONAL ---
        fig = go.Figure()
        
        # Área de Aportes
        fig.add_trace(go.Scatter(
            x=df['Ano'], y=df['Total Investido'],
            stackgroup='one', name='Total Investido',
            line=dict(width=0), fillcolor='rgba(100, 100, 100, 0.5)'
        ))
        
        # Área de Juros
        fig.add_trace(go.Scatter(
            x=df['Ano'], y=df['Patrimônio Nominal'],
            stackgroup='one', name='Juros Compostos',
            line=dict(width=0), fillcolor='rgba(88, 166, 255, 0.6)'
        ))

        # Linha de Poder Real
        fig.add_trace(go.Scatter(
            x=df['Ano'], y=df['Poder de Compra (Real)'],
            name='Valor Real (Ajustado pelo IPCA)',
            line=dict(color='#ff7b72', width=3, dash='dot')
        ))

        fig.update_layout(
            template="plotly_dark",
            hovermode='x unified',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=20, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

        # Mensagem Estratégica
        st.info(f"💡 **Fator de Multiplicação:** Seu capital inicial e aportes se transformaram em **{(final_nominal / (capital_inicial + (aporte_mensal * meses))):.2f}x** o valor investido devido ao efeito do tempo.")