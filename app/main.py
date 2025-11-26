"""
Aplicação Streamlit Unificada - Sistema Preditivo de Obesidade
Tech Challenge
"""
import streamlit as st
import sys
import os

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Importar módulos
from modules.prediction import show_prediction_page
from modules.dashboard import show_dashboard_page

# Configuração da página
st.set_page_config(
    page_title="Sistema Preditivo de Obesidade",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🏥 Sistema Preditivo de Obesidade")
st.markdown("---")

# Sidebar com informações
with st.sidebar:
    st.header("ℹ️ Sobre o Sistema")
    st.markdown("""
    Este sistema foi desenvolvido como parte do Tech Challenge.
    
    **Funcionalidades:**
    - Predição do nível de obesidade
    - Análise de probabilidades por classe
    - Dashboard com insights analíticos
    - Recomendações baseadas nos dados
    
    **Modelo:**
    - Algoritmo: Random Forest
    - Acurácia: 98.58%
    - F1-Score: 98.58%
    """)
    
    st.markdown("---")
    st.markdown("**Desenvolvido para auxiliar profissionais de saúde**")

# Criar abas
tab1, tab2, tab3 = st.tabs(["🏠 Início", "🔮 Predição", "📊 Dashboard Analítico"])

with tab1:
    st.header("Bem-vindo ao Sistema Preditivo de Obesidade")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Objetivo
        
        Este sistema utiliza Machine Learning para auxiliar médicos e médicas 
        na previsão do nível de obesidade de pacientes, fornecendo ferramentas 
        para auxiliar na tomada de decisão clínica.
        
        ### 🔮 Predição
        
        Na aba **Predição**, você pode:
        - Preencher dados do paciente
        - Obter predição do nível de obesidade
        - Ver probabilidades por classe
        - Receber recomendações personalizadas
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Dashboard Analítico
        
        Na aba **Dashboard Analítico**, você encontra:
        - Visualizações interativas dos dados
        - Análises e insights sobre obesidade
        - Filtros para análise personalizada
        - Métricas e estatísticas relevantes
        
        ### 📈 Recursos
        
        - Modelo com 98.58% de acurácia
        - Interface intuitiva e profissional
        - Análises baseadas em dados reais
        """)
    
    st.markdown("---")
    
    st.subheader("🚀 Como Usar")
    
    st.markdown("""
    1. **Para fazer uma predição:**
       - Navegue para a aba "🔮 Predição"
       - Preencha o formulário com os dados do paciente
       - Clique em "Fazer Predição"
       - Analise os resultados e recomendações
    
    2. **Para análise de dados:**
       - Navegue para a aba "📊 Dashboard Analítico"
       - Use os filtros na barra lateral para personalizar a análise
       - Explore os gráficos e insights apresentados
       - Baixe os dados filtrados se necessário
    """)
    
    st.markdown("---")
    
    st.subheader("📋 Informações Técnicas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Acurácia do Modelo", "98.58%")
    
    with col2:
        st.metric("Total de Registros", "2.111")
    
    with col3:
        st.metric("Variáveis de Entrada", "16")

with tab2:
    show_prediction_page()

with tab3:
    show_dashboard_page()

# Rodapé
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Sistema desenvolvido para o Tech Challenge | Uso exclusivo para fins educacionais</p>
</div>
""", unsafe_allow_html=True)

