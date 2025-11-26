"""
Página de Dashboard Analítico - Sistema Preditivo de Obesidade
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

@st.cache_data
def load_data():
    """Carrega os dados"""
    try:
        base_path = os.path.join(os.path.dirname(__file__), '../..')
        csv_path = os.path.join(base_path, 'data/obesity.csv')
        df = pd.read_csv(csv_path)
        # Criar IMC
        df['BMI'] = df['Weight'] / (df['Height'] ** 2)
        return df
    except FileNotFoundError:
        st.error("Arquivo de dados não encontrado. Execute primeiro o script de extração.")
        return None

def show_dashboard_page():
    """Exibe a página do dashboard analítico"""
    
    st.header("📊 Dashboard Analítico")
    st.markdown("""
    Este dashboard apresenta insights e análises sobre os dados de obesidade para auxiliar a equipe médica na tomada de decisão.
    """)
    
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
        st.subheader("📈 Métricas Principais")
        
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
        st.subheader("📊 Distribuição de Níveis de Obesidade")
        
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
        
        # Análise após gráficos de distribuição
        with st.expander("📝 Análise: Distribuição de Obesidade", expanded=True):
            most_common = obesity_counts.idxmax()
            most_common_pct = (obesity_counts.max() / len(df_filtered)) * 100
            st.markdown(f"""
            **Insights:**
            - O nível de obesidade mais comum é **{most_common}**, representando **{most_common_pct:.1f}%** dos casos analisados.
            - A distribuição mostra uma variação significativa entre os diferentes níveis de obesidade.
            - Esta informação é crucial para entender o perfil da população estudada e direcionar estratégias de prevenção.
            
            **Recomendação:** Focar programas de intervenção nos grupos com maior prevalência identificados.
            """)
        
        st.markdown("---")
        
        # Análise por Gênero
        st.subheader("👥 Análise por Gênero")
        
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
        
        # Análise após gráficos de gênero
        with st.expander("📝 Análise: Impacto do Gênero", expanded=True):
            gender_obesity_rate = df_filtered.groupby('Gender')['Obesity'].apply(
                lambda x: (x.str.contains('Obesity|Overweight').sum() / len(x)) * 100
            )
            dominant_gender = gender_obesity_rate.idxmax()
            bmi_diff = abs(avg_bmi_gender['Male'] - avg_bmi_gender['Female']) if 'Male' in avg_bmi_gender.index and 'Female' in avg_bmi_gender.index else 0
            
            st.markdown(f"""
            **Insights:**
            - O gênero **{dominant_gender}** apresenta maior taxa de sobrepeso/obesidade: **{gender_obesity_rate[dominant_gender]:.1f}%**.
            - IMC médio por gênero: {', '.join([f'{g} = {avg_bmi_gender[g]:.2f}' for g in avg_bmi_gender.index])}.
            - Diferença de IMC entre gêneros: **{bmi_diff:.2f} pontos**.
            
            **Recomendação:** Desenvolver estratégias de prevenção específicas por gênero, considerando as diferenças observadas.
            """)
        
        st.markdown("---")
        
        # Análise por Idade
        st.subheader("📅 Análise por Idade")
        
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
        
        # Análise após gráficos de idade
        with st.expander("📝 Análise: Impacto da Idade", expanded=True):
            age_obesity_rate = df_filtered.groupby('Faixa Etária')['Obesity'].apply(
                lambda x: (x.str.contains('Obesity|Overweight').sum() / len(x)) * 100 if len(x) > 0 else 0
            )
            highest_age_group = age_obesity_rate.idxmax() if len(age_obesity_rate) > 0 else None
            correlation_age_bmi = df_filtered['Age'].corr(df_filtered['BMI'])
            
            st.markdown(f"""
            **Insights:**
            - A faixa etária **{highest_age_group}** apresenta maior taxa de sobrepeso/obesidade: **{age_obesity_rate[highest_age_group]:.1f}%** (quando aplicável).
            - Correlação entre Idade e IMC: **{correlation_age_bmi:.3f}** ({'positiva' if correlation_age_bmi > 0 else 'negativa'}).
            - O gráfico de dispersão mostra a relação entre idade e IMC, permitindo identificar padrões e outliers.
            
            **Recomendação:** Implementar programas preventivos específicos para faixas etárias de maior risco identificadas.
            """)
        
        st.markdown("---")
        
        # Análise de Hábitos
        st.subheader("🍽️ Análise de Hábitos e Estilo de Vida")
        
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
        
        # Análise após gráficos de atividade física e histórico familiar
        with st.expander("📝 Análise: Atividade Física e Histórico Familiar", expanded=True):
            faf_impact = df_filtered.groupby('FAF')['Obesity'].apply(
                lambda x: (x.str.contains('Obesity|Overweight').sum() / len(x)) * 100 if len(x) > 0 else 0
            )
            family_impact = df_filtered.groupby('family_history')['Obesity'].apply(
                lambda x: (x.str.contains('Obesity|Overweight').sum() / len(x)) * 100 if len(x) > 0 else 0
            )
            
            low_activity_rate = (faf_impact.get(0.0, 0) + faf_impact.get(1.0, 0)) / 2 if (faf_impact.get(0.0, 0) + faf_impact.get(1.0, 0)) > 0 else 0
            high_activity_rate = (faf_impact.get(2.0, 0) + faf_impact.get(3.0, 0)) / 2 if (faf_impact.get(2.0, 0) + faf_impact.get(3.0, 0)) > 0 else 0
            
            st.markdown(f"""
            **Insights - Atividade Física:**
            - Pacientes com baixa atividade física (0-1) apresentam maior risco de sobrepeso/obesidade.
            - A diferença entre baixa e alta atividade física é significativa, evidenciando a importância do exercício.
            
            **Insights - Histórico Familiar:**
            - Pacientes com histórico familiar de excesso de peso apresentam taxa de **{family_impact.get('yes', 0):.1f}%** de sobrepeso/obesidade.
            - Pacientes sem histórico familiar apresentam taxa de **{family_impact.get('no', 0):.1f}%**.
            
            **Recomendação:** Priorizar triagem e intervenção em pacientes com histórico familiar e baixa atividade física.
            """)
        
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
        
        # Análise após gráficos de hábitos alimentares
        with st.expander("📝 Análise: Hábitos Alimentares", expanded=True):
            favc_impact = df_filtered.groupby('FAVC')['Obesity'].apply(
                lambda x: (x.str.contains('Obesity|Overweight').sum() / len(x)) * 100 if len(x) > 0 else 0
            )
            avg_vegetables_normal = fcvc_obesity.get('Normal_Weight', 0)
            avg_vegetables_obese = fcvc_obesity[fcvc_obesity.index.str.contains('Obesity')].mean() if len(fcvc_obesity[fcvc_obesity.index.str.contains('Obesity')]) > 0 else 0
            
            st.markdown(f"""
            **Insights - Alimentos Calóricos:**
            - Consumo frequente de alimentos altamente calóricos está associado a maior risco de obesidade.
            - Taxa de sobrepeso/obesidade: **{favc_impact.get('yes', 0):.1f}%** (consumo frequente) vs **{favc_impact.get('no', 0):.1f}%** (consumo não frequente).
            
            **Insights - Consumo de Vegetais:**
            - Pacientes com peso normal consomem em média **{avg_vegetables_normal:.2f}** porções de vegetais.
            - Pacientes com obesidade consomem em média **{avg_vegetables_obese:.2f}** porções de vegetais.
            - Maior consumo de vegetais está associado a menor risco de obesidade.
            
            **Recomendação:** Promover educação nutricional focada em redução de alimentos calóricos e aumento do consumo de vegetais.
            """)
        
        st.markdown("---")
        
        # Resumo de Insights
        st.subheader("💡 Resumo de Insights e Recomendações")
        
        insights_col1, insights_col2 = st.columns(2)
        
        with insights_col1:
            st.markdown("""
            **🔍 Principais Descobertas:**
            
            1. **Fatores de Risco Identificados:**
               - Histórico familiar de excesso de peso
               - Baixa frequência de atividade física
               - Consumo frequente de alimentos altamente calóricos
               - Baixo consumo de vegetais
            
            2. **Grupos de Maior Risco:**
               - Determinadas faixas etárias
               - Gênero específico (conforme análise)
               - Pacientes com múltiplos fatores de risco
            """)
        
        with insights_col2:
            st.markdown("""
            **📋 Recomendações para Equipe Médica:**
            
            1. **Triagem Preventiva:**
               - Priorizar pacientes com histórico familiar
               - Monitorar pacientes com baixa atividade física
               - Avaliar hábitos alimentares regularmente
            
            2. **Intervenções:**
               - Programas de atividade física para grupos de risco
               - Educação nutricional sobre alimentos calóricos
               - Promoção do consumo de vegetais
            
            3. **Monitoramento:**
               - Acompanhamento regular de IMC
               - Avaliação periódica de hábitos de vida
               - Acompanhamento de progresso em intervenções
            """)
        
        st.markdown("---")
        
        # Tabela de dados
        st.subheader("📋 Dados Filtrados")
        
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

