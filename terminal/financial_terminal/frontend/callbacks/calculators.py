import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def render_advanced_calculators():
    st.markdown("### 🎯 Simulador de Liberdade Financeira (Real)")
    
    with st.container():
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 💰 Fluxo de Caixa")
            receita = st.number_input("Receita Mensal Líquida (R$)", value=25000.0, step=1000.0)
            despesa = st.number_input("Despesa Mensal Média (R$)", value=15000.0, step=500.0)
            aporte = receita - despesa
            st.info(f"Capacidade de Aporte: **R$ {aporte:,.2f}**")
            
        with col2:
            st.markdown("#### 📈 Parâmetros de Mercado")
            selic = st.number_input("SELIC Estimada (% a.a.)", value=11.25, step=0.25) / 100
            ipca = st.number_input("IPCA Estimado (% a.a.)", value=4.5, step=0.1) / 100
            # Cálculo do Juro Real (Fórmula de Fisher)
            juro_real = ((1 + selic) / (1 + ipca)) - 1
            st.success(f"Juro Real Líquido: **{juro_real*100:.2f}% a.a.**")
            
        with col3:
            st.markdown("#### 🎯 Objetivo")
            patrimonio_atual = st.number_input("Patrimônio Investido (R$)", value=300000.0, step=10000.0)
            patrimonio_desejado = st.number_input("Patrimônio Desejado (R$)", value=5000000.0, step=100000.0)

    st.markdown("---")

    # Lógica de Cálculo de Projeção
    meses = 0
    patrimonio_nominal = patrimonio_atual
    patrimonio_real = patrimonio_atual
    dados_evolucao = []
    
    # Taxas mensais
    taxa_mensal_nom = (1 + selic)**(1/12) - 1
    taxa_mensal_real = (1 + juro_real)**(1/12) - 1
    taxa_inflacao_mensal = (1 + ipca)**(1/12) - 1

    # Simulação até 50 anos ou atingir objetivo
    while patrimonio_real < patrimonio_desejado and meses < 600:
        meses += 1
        # Evolução Nominal
        patrimonio_nominal = patrimonio_nominal * (1 + taxa_mensal_nom) + aporte
        # Evolução Real (Poder de Compra)
        patrimonio_real = patrimonio_real * (1 + taxa_mensal_real) + aporte
        
        dados_evolucao.append({
            "Mês": meses,
            "Anos": meses / 12,
            "Patrimônio Nominal": patrimonio_nominal,
            "Poder Real (Valor de Hoje)": patrimonio_real
        })

    df_evolucao = pd.DataFrame(dados_evolucao)

    # Exibição de Resultados Estratégicos
    res1, res2, res3 = st.columns(3)
    
    tempo_anos = meses / 12
    res1.metric("Tempo para Objetivo", f"{tempo_anos:.1f} Anos")
    res2.metric("Montante Final (Nominal)", f"R$ {patrimonio_nominal:,.0f}")
    res3.metric("Erosão inflacionária/ano", f"R$ {(patrimonio_nominal * ipca):,.2f}", delta_color="inverse")

    # Gráfico de Evolução Patrimonial
    st.markdown("#### Evolução Patrimonial: Nominal vs Real")
    fig = px.line(df_evolucao, x="Anos", y=["Patrimônio Nominal", "Poder Real (Valor de Hoje)"],
                  labels={"value": "Patrimônio (R$)", "Anos": "Tempo (Anos)"},
                  color_discrete_map={"Patrimônio Nominal": "#30363d", "Poder Real (Valor de Hoje)": "#58a6ff"})
    
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

    # Nota Técnica para o Cliente
    st.warning(f"**Nota de Elite:** Para manter o poder de compra de R$ {patrimonio_desejado:,.2f} daqui a {tempo_anos:.1f} anos, você precisará nominalmente de R$ {patrimonio_nominal:,.2f}. Isso se deve ao efeito corrosivo do IPCA de {ipca*100:.1f}% ao ano.")