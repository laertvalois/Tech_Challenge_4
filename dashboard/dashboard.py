"""
Dashboard Analítico - Obesidade
Tech Challenge
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Configuração da página
st.set_page_config(
    page_title="Dashboard Analítico - Obesidade",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título
st.title("📊 Dashboard Analítico - Obesidade")
st.markdown("---")
st.markdown("""
Este dashboard apresenta insights e análises sobre os dados de obesidade para auxiliar a equipe médica na tomada de decisão.
""")

# Carregar dados
@st.cache_data
def load_data():
    """Carrega os dados"""
    try:
        df = pd.read_csv('data/obesity.csv')
        # Criar IMC
        df['BMI'] = df['Weight'] / (df['Height'] ** 2)
        return df
    except FileNotFoundError:
        st.error("Arquivo de dados não encontrado. Execute primeiro o script de extração.")
        return None

df = load_data()

if df is not None:
    # Sidebar com filtros
    with st.sidebar:
        st.header("🔍 Filtros")
        
        # Filtro por gênero
        gender_filter = st.multiselect(
            "Gênero",
            options=df['Gender'].unique(),
            default=df['Gender'].unique()
        )
        
        # Filtro por nível de obesidade
        obesity_filter = st.multiselect(
            "Nível de Obesidade",
            options=df['Obesity'].unique(),
            default=df['Obesity'].unique()
        )
        
        # Filtro por idade
        age_range = st.slider(
            "Faixa etária",
            min_value=int(df['Age'].min()),
            max_value=int(df['Age'].max()),
            value=(int(df['Age'].min()), int(df['Age'].max()))
        )
    
    # Aplicar filtros
    df_filtered = df[
        (df['Gender'].isin(gender_filter)) &
        (df['Obesity'].isin(obesity_filter)) &
        (df['Age'] >= age_range[0]) &
        (df['Age'] <= age_range[1])
    ]
    
    # Métricas principais
    st.header("📈 Métricas Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Registros", len(df_filtered))
    
    with col2:
        avg_bmi = df_filtered['BMI'].mean()
        st.metric("IMC Médio", f"{avg_bmi:.2f}")
    
    with col3:
        avg_age = df_filtered['Age'].mean()
        st.metric("Idade Média", f"{avg_age:.1f} anos")
    
    with col4:
        obesity_rate = (df_filtered['Obesity'].str.contains('Obesity|Overweight').sum() / len(df_filtered)) * 100
        st.metric("Taxa de Sobrepeso/Obesidade", f"{obesity_rate:.1f}%")
    
    st.markdown("---")
    
    # Distribuição de Obesidade
    st.header("📊 Distribuição de Níveis de Obesidade")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de barras
        obesity_counts = df_filtered['Obesity'].value_counts()
        fig_bar = px.bar(
            x=obesity_counts.index,
            y=obesity_counts.values,
            labels={'x': 'Nível de Obesidade', 'y': 'Frequência'},
            title='Distribuição de Níveis de Obesidade',
            color=obesity_counts.values,
            color_continuous_scale='Reds'
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # Gráfico de pizza
        fig_pie = px.pie(
            values=obesity_counts.values,
            names=obesity_counts.index,
            title='Proporção de Níveis de Obesidade'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("---")
    
    # Análise por Gênero
    st.header("👥 Análise por Gênero")
    
    col1, col2 = st.columns(2)
    
    with col1:
        gender_obesity = pd.crosstab(df_filtered['Gender'], df_filtered['Obesity'])
        fig_gender = px.bar(
            gender_obesity,
            barmode='group',
            title='Distribuição de Obesidade por Gênero',
            labels={'value': 'Frequência', 'Gender': 'Gênero'}
        )
        st.plotly_chart(fig_gender, use_container_width=True)
    
    with col2:
        avg_bmi_gender = df_filtered.groupby('Gender')['BMI'].mean()
        fig_bmi_gender = px.bar(
            x=avg_bmi_gender.index,
            y=avg_bmi_gender.values,
            title='IMC Médio por Gênero',
            labels={'x': 'Gênero', 'y': 'IMC Médio'},
            color=avg_bmi_gender.values,
            color_continuous_scale='Oranges'
        )
        fig_bmi_gender.update_layout(showlegend=False)
        st.plotly_chart(fig_bmi_gender, use_container_width=True)
    
    st.markdown("---")
    
    # Análise por Idade
    st.header("📅 Análise por Idade")
    
    # Criar faixas etárias
    df_filtered['Faixa Etária'] = pd.cut(
        df_filtered['Age'],
        bins=[0, 20, 30, 40, 50, 100],
        labels=['<20', '20-30', '30-40', '40-50', '50+']
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        age_obesity = pd.crosstab(df_filtered['Faixa Etária'], df_filtered['Obesity'])
        fig_age = px.bar(
            age_obesity,
            barmode='group',
            title='Distribuição de Obesidade por Faixa Etária',
            labels={'value': 'Frequência', 'Faixa Etária': 'Faixa Etária'}
        )
        st.plotly_chart(fig_age, use_container_width=True)
    
    with col2:
        # Scatter plot: Idade vs IMC
        fig_scatter = px.scatter(
            df_filtered,
            x='Age',
            y='BMI',
            color='Obesity',
            title='Relação entre Idade e IMC',
            labels={'Age': 'Idade', 'BMI': 'IMC'},
            hover_data=['Gender', 'Weight', 'Height']
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("---")
    
    # Análise de Hábitos
    st.header("🍽️ Análise de Hábitos e Estilo de Vida")
    
    # Atividade Física
    col1, col2 = st.columns(2)
    
    with col1:
        faf_obesity = pd.crosstab(df_filtered['FAF'], df_filtered['Obesity'])
        fig_faf = px.bar(
            faf_obesity,
            barmode='group',
            title='Impacto da Atividade Física na Obesidade',
            labels={'value': 'Frequência', 'FAF': 'Frequência de Atividade Física'}
        )
        st.plotly_chart(fig_faf, use_container_width=True)
    
    with col2:
        # Histórico familiar
        family_obesity = pd.crosstab(df_filtered['family_history'], df_filtered['Obesity'])
        fig_family = px.bar(
            family_obesity,
            barmode='group',
            title='Impacto do Histórico Familiar',
            labels={'value': 'Frequência', 'family_history': 'Histórico Familiar'}
        )
        st.plotly_chart(fig_family, use_container_width=True)
    
    # Consumo de alimentos calóricos
    col3, col4 = st.columns(2)
    
    with col3:
        favc_obesity = pd.crosstab(df_filtered['FAVC'], df_filtered['Obesity'])
        fig_favc = px.bar(
            favc_obesity,
            barmode='group',
            title='Impacto de Alimentos Altamente Calóricos',
            labels={'value': 'Frequência', 'FAVC': 'Alimentos Calóricos'}
        )
        st.plotly_chart(fig_favc, use_container_width=True)
    
    with col4:
        # Consumo de vegetais
        fcvc_obesity = df_filtered.groupby('Obesity')['FCVC'].mean()
        fig_fcvc = px.bar(
            x=fcvc_obesity.index,
            y=fcvc_obesity.values,
            title='Consumo Médio de Vegetais por Nível de Obesidade',
            labels={'x': 'Nível de Obesidade', 'y': 'Consumo Médio de Vegetais'},
            color=fcvc_obesity.values,
            color_continuous_scale='Greens'
        )
        fig_fcvc.update_layout(showlegend=False)
        st.plotly_chart(fig_fcvc, use_container_width=True)
    
    st.markdown("---")
    
    # Insights e Recomendações
    st.header("💡 Insights e Recomendações")
    
    insights_col1, insights_col2 = st.columns(2)
    
    with insights_col1:
        st.subheader("🔍 Principais Descobertas")
        
        # Insight 1: Gênero
        gender_obesity_rate = df_filtered.groupby('Gender')['Obesity'].apply(
            lambda x: (x.str.contains('Obesity|Overweight').sum() / len(x)) * 100
        )
        dominant_gender = gender_obesity_rate.idxmax()
        st.info(f"""
        **Gênero mais afetado:** {dominant_gender}
        - Taxa de sobrepeso/obesidade: {gender_obesity_rate[dominant_gender]:.1f}%
        """)
        
        # Insight 2: Atividade Física
        faf_impact = df_filtered.groupby('FAF')['Obesity'].apply(
            lambda x: (x.str.contains('Obesity|Overweight').sum() / len(x)) * 100
        )
        st.info(f"""
        **Atividade Física:**
        - Baixa atividade (0-1): {faf_impact.get(0.0, 0) + faf_impact.get(1.0, 0):.1f}% de sobrepeso/obesidade
        - Alta atividade (2-3): {faf_impact.get(2.0, 0) + faf_impact.get(3.0, 0):.1f}% de sobrepeso/obesidade
        """)
    
    with insights_col2:
        st.subheader("📋 Recomendações para Equipe Médica")
        
        st.success("""
        **1. Triagem Preventiva:**
        - Priorizar pacientes com histórico familiar
        - Monitorar pacientes com baixa atividade física
        
        **2. Intervenções:**
        - Programas de atividade física para grupos de risco
        - Educação nutricional sobre alimentos calóricos
        
        **3. Monitoramento:**
        - Acompanhamento regular de IMC
        - Avaliação de hábitos alimentares
        """)
    
    st.markdown("---")
    
    # Tabela de dados
    st.header("📋 Dados Filtrados")
    
    if st.checkbox("Mostrar dados completos"):
        st.dataframe(df_filtered, use_container_width=True, height=400)
    
    # Download dos dados
    csv = df_filtered.to_csv(index=False)
    st.download_button(
        label="📥 Download dos dados filtrados (CSV)",
        data=csv,
        file_name="obesity_filtered.csv",
        mime="text/csv"
    )

else:
    st.error("Não foi possível carregar os dados. Verifique se o arquivo existe.")

# Rodapé
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Dashboard desenvolvido para o Tech Challenge | Uso exclusivo para fins educacionais</p>
</div>
""", unsafe_allow_html=True)

