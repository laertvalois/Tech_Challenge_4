"""
Aplicação Streamlit - Sistema Preditivo de Obesidade
Tech Challenge
"""
import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.load_model import load_trained_model, load_preprocessor
from src.data_preprocessing import DataPreprocessor

# Configuração da página
st.set_page_config(
    page_title="Sistema Preditivo de Obesidade",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado com cores frias
st.markdown("""
<style>
    /* Background das páginas - branco */
    .main {
        background-color: white;
    }
    .stApp {
        background-color: white;
    }
    
    /* Background do sidebar/menu */
    section[data-testid="stSidebar"] {
        background-color: #dcdcdc !important;
        width: 350px !important;
    }
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        width: 350px !important;
        background-color: #dcdcdc;
    }
    [data-testid="stSidebar"] > div:first-child {
        background-color: #dcdcdc;
    }
    
    /* Títulos das páginas - menores e mais discretos */
    h1 {
        color: white !important;
        background-color: #005ca9e6 !important;
        padding: 0.5rem 1rem !important;
        border-radius: 6px !important;
        margin-bottom: 0.75rem !important;
        font-weight: 600 !important;
        font-size: 1.5rem !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }
    
    /* Headers (h2) - menores e mais discretos */
    h2 {
        color: white !important;
        background-color: #005ca9e6 !important;
        padding: 0.4rem 0.8rem !important;
        border-radius: 6px !important;
        margin-top: 1rem !important;
        margin-bottom: 0.75rem !important;
        font-weight: 600 !important;
        font-size: 1.25rem !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }
    
    /* Aplicar estilo também para elementos específicos do Streamlit */
    [data-testid="stHeader"] h1 {
        color: white !important;
        background-color: #005ca9e6 !important;
        padding: 0.5rem 1rem !important;
        border-radius: 6px !important;
        font-size: 1.5rem !important;
    }
    
    /* Subheaders (h3) - tom mais claro e discreto */
    h3 {
        color: #005ca9 !important;
        font-weight: 600 !important;
        margin-top: 0.75rem !important;
        font-size: 1.1rem !important;
    }
    
    /* Filtros - estilo com cor fria */
    div[style*="background-color: #005ca9e6"] label,
    div[style*="005ca9e6"] label {
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* Botões - mais discretos */
    .stButton>button {
        background-color: #005ca9 !important;
        color: white !important;
        border-radius: 6px;
        padding: 0.4rem 1.5rem;
        font-weight: 500;
        font-size: 0.95rem;
        border: none;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #004a8a !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }
    
    /* Cards de métricas - mais discretos */
    .metric-card {
        background-color: white;
        padding: 0.75rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin: 0.5rem 0;
        border-left: 3px solid #005ca9;
    }
    
    /* Result box - mais discreto */
    .result-box {
        background: linear-gradient(135deg, #005ca9 0%, #0073c7 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    
    /* Info boxes - mais discretos */
    .info-box {
        background-color: #e8f4f8;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        border-left: 3px solid #005ca9;
        margin: 0.75rem 0;
    }
    
    /* Logo/título do sidebar - mais discreto */
    .logo-title {
        background: linear-gradient(135deg, #005ca9 0%, #0073c7 100%);
        color: white;
        padding: 0.75rem;
        border-radius: 8px;
        text-align: center;
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Multiselect e selectboxes nos filtros - manter branco mas com borda azul se necessário */
    div[data-baseweb="select"] {
        background-color: white;
    }
    
    /* Garantir que todos os selectboxes tenham borda azul */
    div[data-baseweb="select"] > div {
        border: 1.5px solid #005ca9 !important;
    }
    
    /* Labels dos filtros - mais discretos */
    .filter-container .stMultiSelect label,
    .filter-container .stSelectbox label,
    .filter-container .stSlider label {
        color: white !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    
    /* Slider nos filtros */
    .stSlider label {
        color: white !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    
    /* Labels dentro do container azul */
    div[style*="background-color: #005ca9e6"] label {
        color: white !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    
    /* Ajustar cor dos textos dentro do container de filtros */
    .filter-container p,
    .filter-container div {
        color: white;
    }
    
    /* Estilo mais discreto para os componentes de filtro */
    div[style*="background-color: #005ca9e6"] {
        padding: 1rem 1.25rem !important;
        border-radius: 8px !important;
        margin-bottom: 1rem !important;
    }
    
    /* Garantir que o texto "Filtros" esteja branco */
    div[style*="background-color: #005ca9e6"] h3 {
        color: white !important;
    }
    
    /* Campos de input - padronizados: azul claro acinzentado sem borda */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input {
        background-color: #e8f0f5 !important;
        border: none !important;
        border-radius: 6px !important;
    }
    
    .stTextInput>div>div>input:hover,
    .stNumberInput>div>div>input:hover {
        background-color: #dde8f0 !important;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus {
        background-color: #d3e0eb !important;
        box-shadow: 0 0 0 2px rgba(0, 92, 169, 0.1) !important;
    }
    
    /* Selectbox - padronizado: azul claro acinzentado sem borda */
    .stSelectbox>div>div>div,
    div[data-baseweb="select"] > div {
        background-color: #e8f0f5 !important;
        border: none !important;
        border-radius: 6px !important;
    }
    
    .stSelectbox>div>div>div:hover,
    div[data-baseweb="select"] > div:hover {
        background-color: #dde8f0 !important;
    }
    
    /* Multiselect - tags azuis em vez de vermelhas */
    div[data-baseweb="tag"] {
        background-color: #005ca9 !important;
        color: white !important;
        border: none !important;
    }
    
    /* Container das tags do multiselect */
    div[data-baseweb="popover"] div[data-baseweb="tag"] {
        background-color: #005ca9 !important;
        color: white !important;
    }
    
    /* Slider - azul em vez de vermelho */
    .stSlider > div > div > div {
        background-color: #005ca9 !important;
    }
    
    .stSlider > div > div > div > div {
        background-color: #005ca9 !important;
    }
    
    /* Track do slider */
    .stSlider > div > div > div[data-baseweb="slider-track"] {
        background-color: #005ca9 !important;
    }
    
    /* Handle do slider */
    .stSlider > div > div > div[data-baseweb="slider-handle"] {
        background-color: #005ca9 !important;
        border: 2px solid white !important;
    }
    
    /* Valores do slider - azul */
    .stSlider > div > div > span {
        color: #005ca9 !important;
        font-weight: 600 !important;
    }
    
    /* Garantir que todos os textos dentro do container de filtros sejam brancos */
    div[style*="background-color: #005ca9e6"] h3,
    div[style*="background-color: #005ca9e6"] * {
        color: white !important;
    }
    
    /* Expanders - mais discretos */
    .streamlit-expanderHeader {
        background-color: #e8f4f8;
        color: #005ca9;
        font-weight: 500;
        font-size: 0.95rem;
        padding: 0.5rem 0.75rem;
        border-radius: 4px;
    }
    
    /* Tabelas */
    .dataframe {
        background-color: white;
    }
    
    /* Markdown info/success/warning */
    .stAlert {
        border-left: 4px solid #005ca9;
    }
    
    /* Garantir que todos os campos tenham borda azul padrão */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background-color: white !important;
        border: 1.5px solid #005ca9 !important;
        border-radius: 6px !important;
    }
    
    .stTextInput > div > div > input:hover,
    .stNumberInput > div > div > input:hover,
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border: 1.5px solid #004a8a !important;
        box-shadow: 0 0 0 2px rgba(0, 92, 169, 0.1) !important;
    }
    
    /* Selectbox com borda azul padrão */
    .stSelectbox > div > div > div[data-baseweb="select"] {
        background-color: white !important;
        border: 1.5px solid #005ca9 !important;
        border-radius: 6px !important;
    }
    
    .stSelectbox > div > div > div[data-baseweb="select"]:hover {
        border: 1.5px solid #004a8a !important;
    }
    
    /* Container dos inputs - transparente para não interferir */
    .stTextInput > div,
    .stNumberInput > div,
    .stSelectbox > div {
        background-color: transparent !important;
    }
    
    /* Garantir que selectboxes também tenham borda azul */
    div[data-baseweb="select"] {
        border: 1.5px solid #005ca9 !important;
        border-radius: 6px !important;
    }
    
    /* Override das tags vermelhas do Streamlit para azul */
    span[data-baseweb="tag"] {
        background-color: #005ca9 !important;
        color: white !important;
    }
    
    /* Tags do multiselect */
    div[data-baseweb="tag"] span {
        color: white !important;
    }
    
    /* Forçar cor azul nas tags selecionadas */
    div[data-baseweb="popover"] div[data-baseweb="tag"],
    div[data-baseweb="base-popover"] div[data-baseweb="tag"] {
        background-color: #005ca9 !important;
        color: white !important;
    }
    
    /* Slider - override completo para azul */
    .stSlider div[data-baseweb="slider"] {
        color: #005ca9 !important;
    }
    
    /* Garantir que o texto Filtros seja branco */
    div[style*="005ca9e6"] h3,
    div[style*="005ca9e6"] * {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Mapeamento de níveis de obesidade para português
OBESITY_LEVELS_PT = {
    'Normal_Weight': 'Peso Normal',
    'Overweight_Level_I': 'Sobrepeso Nível I',
    'Overweight_Level_II': 'Sobrepeso Nível II',
    'Obesity_Type_I': 'Obesidade Tipo I',
    'Obesity_Type_II': 'Obesidade Tipo II',
    'Obesity_Type_III': 'Obesidade Tipo III',
    'Insufficient_Weight': 'Peso Insuficiente'
}

# Traduções para português
TRANSLATIONS = {
    'Gender': {
        'Male': 'Masculino',
        'Female': 'Feminino'
    },
    'family_history': {
        'yes': 'Sim',
        'no': 'Não'
    },
    'FAVC': {
        'yes': 'Sim',
        'no': 'Não'
    },
    'CAEC': {
        'no': 'Não',
        'Sometimes': 'Às vezes',
        'Frequently': 'Frequentemente',
        'Always': 'Sempre'
    },
    'SMOKE': {
        'yes': 'Sim',
        'no': 'Não'
    },
    'SCC': {
        'yes': 'Sim',
        'no': 'Não'
    },
    'CALC': {
        'no': 'Não',
        'Sometimes': 'Às vezes',
        'Frequently': 'Frequentemente'
    },
    'MTRANS': {
        'Public_Transportation': 'Transporte Público',
        'Automobile': 'Automóvel',
        'Walking': 'Caminhada',
        'Motorbike': 'Motocicleta',
        'Bike': 'Bicicleta'
    }
}

# Função para carregar modelo (com cache)
@st.cache_resource
def load_model():
    """Carrega o modelo e pré-processador"""
    try:
        model = load_trained_model('models/obesity_model.joblib')
        preprocessor_data = load_preprocessor('models/preprocessor.joblib')
        return model, preprocessor_data
    except Exception as e:
        st.error(f"Erro ao carregar modelo: {str(e)}")
        return None, None

# Função para fazer predição
def make_prediction(input_data, model, preprocessor_data):
    """Faz predição usando o modelo treinado"""
    try:
        # Criar DataFrame com os dados de entrada
        df = pd.DataFrame([input_data])
        
        # Pré-processar dados
        preprocessor = DataPreprocessor()
        preprocessor.label_encoders = preprocessor_data['label_encoders']
        preprocessor.scaler = preprocessor_data['scaler']
        preprocessor.feature_names = preprocessor_data['feature_names']
        
        # Aplicar pré-processamento
        df_processed = preprocessor.handle_missing_values(df)
        df_processed = preprocessor.encode_categorical(df_processed, fit=False)
        
        # Criar IMC
        df_processed = preprocessor.create_bmi(df_processed)
        
        # Preparar features (sem target)
        X = df_processed[preprocessor.feature_names]
        
        # Normalizar
        X_scaled = preprocessor.scale_features(X, fit=False)
        
        # Fazer predição
        prediction = model.predict(X_scaled)[0]
        probabilities = model.predict_proba(X_scaled)[0]
        classes = model.classes_
        
        return prediction, probabilities, classes
        
    except Exception as e:
        st.error(f"Erro ao fazer predição: {str(e)}")
        return None, None, None

# Função para gerar PDF
def generate_pdf(medico_nome, medico_crm, paciente_nome, input_data, prediction, probabilities, classes):
    """Gera PDF com o resultado da predição"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=12
    )
    
    # Título
    story.append(Paragraph("Relatório de Predição de Obesidade", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Informações do médico e paciente (tratar campos vazios)
    profissional = medico_nome.strip() if medico_nome else "Não informado"
    registro = medico_crm.strip() if medico_crm else "Não informado"
    paciente = paciente_nome.strip() if paciente_nome else "Não informado"
    
    info_data = [
        ['Profissional:', profissional],
        ['Registro do Conselho:', registro],
        ['Paciente:', paciente],
        ['Data:', datetime.now().strftime('%d/%m/%Y %H:%M')]
    ]
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Resultado da predição
    prediction_pt = OBESITY_LEVELS_PT.get(prediction, prediction)
    pred_idx = list(classes).index(prediction)
    confidence = probabilities[pred_idx] * 100
    
    story.append(Paragraph("Resultado da Predição", heading_style))
    story.append(Paragraph(f"<b>Nível de Obesidade:</b> {prediction_pt}", styles['Normal']))
    story.append(Paragraph(f"<b>Confiança:</b> {confidence:.2f}%", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Probabilidades
    story.append(Paragraph("Probabilidades por Classe", heading_style))
    prob_data = [['Nível de Obesidade', 'Probabilidade (%)']]
    prob_df = pd.DataFrame({
        'Nível': [OBESITY_LEVELS_PT.get(c, c) for c in classes],
        'Probabilidade': [p * 100 for p in probabilities]
    }).sort_values('Probabilidade', ascending=False)
    
    for _, row in prob_df.iterrows():
        prob_data.append([row['Nível'], f"{row['Probabilidade']:.2f}%"])
    
    prob_table = Table(prob_data, colWidths=[3.5*inch, 2.5*inch])
    prob_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    story.append(prob_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Dados do paciente
    story.append(Paragraph("Dados do Paciente", heading_style))
    
    # Mapeamento de tradução dos campos
    field_translations = {
        'Gender': 'Gênero',
        'Age': 'Idade',
        'Height': 'Altura (m)',
        'Weight': 'Peso (kg)',
        'family_history': 'Histórico Familiar',
        'FAVC': 'Alimentos Altamente Calóricos',
        'FCVC': 'Frequência de Consumo de Vegetais',
        'NCP': 'Número de Refeições Principais',
        'CAEC': 'Come Entre Refeições',
        'SMOKE': 'Fuma',
        'CH2O': 'Consumo de Água',
        'SCC': 'Monitora Calorias',
        'FAF': 'Frequência de Atividade Física',
        'TUE': 'Tempo em Dispositivos Tecnológicos',
        'CALC': 'Frequência de Consumo de Álcool',
        'MTRANS': 'Meio de Transporte'
    }
    
    patient_data = []
    for key, value in input_data.items():
        # Traduzir nome do campo
        field_name = field_translations.get(key, key.replace('_', ' ').title())
        
        # Traduzir valores
        if key in TRANSLATIONS and value in TRANSLATIONS[key]:
            value = TRANSLATIONS[key][value]
        
        patient_data.append([field_name, str(value)])
    
    patient_table = Table(patient_data, colWidths=[2.5*inch, 3.5*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    story.append(patient_table)
    
    # Rodapé
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(
        "<i>Sistema desenvolvido para o Tech Challenge 4 - FIAP | Uso exclusivo para fins educacionais</i>",
        styles['Normal']
    ))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# Menu lateral
with st.sidebar:
    # Logo/Título estilizado
    st.markdown("""
    <div class="logo-title">
        🏥 Sistema Preditivo<br>de Obesidade
    </div>
    """, unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,
        options=["Início", "Predição de Obesidade", "Insights e Métricas"],
        icons=["house", "activity", "graph-up"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#dcdcdc"},
            "icon": {"color": "#005ca9", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "color": "#2c3e50",
                "--hover-color": "#b3d9f2",
                "border-radius": "5px",
            },
            "nav-link-selected": {
                "background-color": "#005ca9e6",
                "color": "white",
            },
        }
    )
    
    st.markdown("---")
    
    # Seção Sobre o Sistema
    st.markdown("### ℹ️ Sobre o Sistema")
    st.markdown("""
    Este sistema foi desenvolvido como parte do Tech Challenge 4.
    
    **Funcionalidades:**
    - Predição do nível de obesidade
    - Análise de probabilidades por classe
    - Dashboard com insights analíticos
    - Recomendações baseadas nos dados
    
    **Modelo:**
    - Algoritmo: Random Forest
    - Acurácia: 98.58%
    
    Desenvolvido para auxiliar profissionais de saúde
    """)

# Página Início
if selected == "Início":
    st.title("🏥 Bem-vindo ao Sistema Preditivo de Obesidade")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎯 Objetivo
        
        Este sistema utiliza Machine Learning para auxiliar médicos e médicas na previsão do nível de obesidade de pacientes, 
        fornecendo ferramentas para auxiliar na tomada de decisão clínica.
        """)
        
        st.markdown("""
        ### 🔮 Predição
        
        Na aba **Predição de Obesidade**, você pode:
        
        - Preencher dados do paciente
        - Obter predição do nível de obesidade
        - Ver probabilidades por classe
        - Receber recomendações personalizadas
        - Exportar relatório em PDF
        """)
        
        st.markdown("""
        ### 📊 Insights e Métricas
        
        Na aba **Insights e Métricas**, você encontra:
        
        - Visualizações interativas dos dados
        - Análises e insights sobre obesidade
        - Métricas do modelo
        - Recomendações clínicas
        """)
    
    with col2:
        st.markdown("### 📈 Recursos")
        st.info("""
        - Modelo com 98.58% de acurácia
        - Interface intuitiva e profissional
        - Análises baseadas em dados reais
        """)
        
        st.markdown("### 🚀 Como Usar")
        st.markdown("""
        **Para fazer uma predição:**
        
        1. Navegue para a aba "🔮 Predição de Obesidade"
        2. Preencha o formulário com os dados do paciente
        3. Clique em "Fazer Predição"
        4. Analise os resultados e recomendações
        5. Exporte o relatório em PDF se necessário
        
        **Para análise de dados:**
        
        1. Navegue para a aba "📊 Insights e Métricas"
        2. Explore os gráficos e insights apresentados
        3. Analise as métricas do modelo
        """)
    
    st.markdown("---")
    
    # Métricas principais
    st.markdown("### 📋 Informações Técnicas")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Acurácia do Modelo", "98.58%")
    
    with col2:
        st.metric("Total de Registros", "2.111")
    
    with col3:
        st.metric("Variáveis de Entrada", "16")
    
    with col4:
        st.metric("Classes de Obesidade", "7")
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; padding: 2rem;'>
        <p>Sistema desenvolvido para o Tech Challenge 4 - FIAP | Uso exclusivo para fins educacionais</p>
    </div>
    """, unsafe_allow_html=True)

# Página Predição
elif selected == "Predição de Obesidade":
    st.title("🔮 Predição de Nível de Obesidade")
    st.markdown("---")
    
    # Carregar modelo
    model, preprocessor_data = load_model()
    
    if model is None or preprocessor_data is None:
        st.error("Não foi possível carregar o modelo. Verifique se os arquivos estão no diretório correto.")
        st.stop()
    
    # Seção de informações do médico e paciente
    st.subheader("👨‍⚕️ Informações do Profissional e Paciente")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        medico_nome = st.text_input("Nome do Profissional (opcional)", placeholder="Ex: Dr. João Silva")
    
    with col2:
        medico_crm = st.text_input("Registro do Conselho (opcional)", placeholder="Ex: CRM 123456")
    
    with col3:
        paciente_nome = st.text_input("Nome do Paciente (opcional)", placeholder="Ex: Maria Santos")
    
    st.markdown("---")
    
    # Formulário de entrada - Reorganizado para melhor uso do espaço
    st.subheader("📝 Dados do Paciente")
    
    # Primeira linha: Dados Demográficos em 3 colunas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📊 Dados Demográficos")
        gender = st.selectbox("Gênero", ["Masculino", "Feminino"])
        age = st.number_input("Idade", min_value=1, max_value=120, value=30)
    
    with col2:
        st.markdown("#### 📏 Medidas")
        height = st.number_input("Altura (metros)", min_value=0.5, max_value=2.5, value=1.70, step=0.01)
        weight = st.number_input("Peso (kg)", min_value=10.0, max_value=300.0, value=70.0, step=0.1)
        
        # Calcular IMC
        if height > 0:
            bmi = weight / (height ** 2)
            st.info(f"**IMC:** {bmi:.2f}")
    
    with col3:
        st.markdown("#### 👨‍👩‍👧‍👦 Histórico")
        family_history = st.selectbox("Histórico familiar de excesso de peso", ["Sim", "Não"])
    
    st.markdown("---")
    
    # Segunda linha: Hábitos Alimentares em 3 colunas
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown("#### 🍽️ Alimentação")
        favc = st.selectbox("Alimentos altamente calóricos?", ["Sim", "Não"])
        fcvc = st.number_input("Consumo de vegetais (1-3)", min_value=1.0, max_value=3.0, value=2.0, step=0.1)
        ncp = st.number_input("Refeições principais (1-4)", min_value=1.0, max_value=4.0, value=3.0, step=0.1)
    
    with col5:
        st.markdown("#### 💧 Hidratação")
        caec = st.selectbox("Come entre refeições?", ["Não", "Às vezes", "Frequentemente", "Sempre"])
        ch2o = st.number_input("Consumo de água (1-3)", min_value=1.0, max_value=3.0, value=2.0, step=0.1)
        scc = st.selectbox("Monitora calorias?", ["Sim", "Não"])
    
    with col6:
        st.markdown("#### 🏃 Estilo de Vida")
        smoke = st.selectbox("Fuma?", ["Sim", "Não"])
        faf = st.number_input("Atividade física (0-3)", min_value=0.0, max_value=3.0, value=1.0, step=0.1)
        tue = st.number_input("Tempo em dispositivos (0-2)", min_value=0.0, max_value=2.0, value=1.0, step=0.1)
    
    st.markdown("---")
    
    # Terceira linha: Outros hábitos
    col7, col8 = st.columns(2)
    
    with col7:
        calc = st.selectbox("Frequência de consumo de álcool", ["Não", "Às vezes", "Frequentemente"])
    
    with col8:
        mtrans = st.selectbox("Meio de transporte", [
            "Transporte Público",
            "Automóvel",
            "Caminhada",
            "Motocicleta",
            "Bicicleta"
        ])
    
    # Converter valores para inglês (formato do modelo)
    gender_en = "Male" if gender == "Masculino" else "Female"
    family_history_en = "yes" if family_history == "Sim" else "no"
    favc_en = "yes" if favc == "Sim" else "no"
    smoke_en = "yes" if smoke == "Sim" else "no"
    scc_en = "yes" if scc == "Sim" else "no"
    
    caec_map = {"Não": "no", "Às vezes": "Sometimes", "Frequentemente": "Frequently", "Sempre": "Always"}
    caec_en = caec_map[caec]
    
    calc_map = {"Não": "no", "Às vezes": "Sometimes", "Frequentemente": "Frequently"}
    calc_en = calc_map[calc]
    
    mtrans_map = {
        "Transporte Público": "Public_Transportation",
        "Automóvel": "Automobile",
        "Caminhada": "Walking",
        "Motocicleta": "Motorbike",
        "Bicicleta": "Bike"
    }
    mtrans_en = mtrans_map[mtrans]
    
    input_data = {
        'Gender': gender_en,
        'Age': age,
        'Height': height,
        'Weight': weight,
        'family_history': family_history_en,
        'FAVC': favc_en,
        'FCVC': fcvc,
        'NCP': ncp,
        'CAEC': caec_en,
        'SMOKE': smoke_en,
        'CH2O': ch2o,
        'SCC': scc_en,
        'FAF': faf,
        'TUE': tue,
        'CALC': calc_en,
        'MTRANS': mtrans_en
    }
    
    # Botão de predição
    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    
    with col_btn2:
        predict_button = st.button("🔮 Fazer Predição", type="primary", use_container_width=True)
    
    # Fazer predição
    if predict_button:
        with st.spinner("Processando predição..."):
            prediction, probabilities, classes = make_prediction(input_data, model, preprocessor_data)
        
        if prediction is not None:
            st.markdown("---")
            st.header("📊 Resultado da Predição")
            
            # Resultado principal
            prediction_pt = OBESITY_LEVELS_PT.get(prediction, prediction)
            
            # Container para resultado
            st.markdown(f"""
            <div class="result-box">
                <h2 style="color: white; margin: 0;">🎯 Nível de Obesidade Previsto</h2>
                <h1 style="color: white; margin: 1rem 0;">{prediction_pt}</h1>
            </div>
            """, unsafe_allow_html=True)
            
            # Probabilidade da classe predita
            pred_idx = list(classes).index(prediction)
            confidence = probabilities[pred_idx] * 100
            st.progress(confidence / 100)
            st.caption(f"**Confiança:** {confidence:.2f}%")
            
            # Probabilidades por classe
            st.markdown("---")
            st.subheader("📈 Probabilidades por Classe")
            
            # Criar DataFrame com probabilidades
            prob_df = pd.DataFrame({
                'Nível de Obesidade': [OBESITY_LEVELS_PT.get(c, c) for c in classes],
                'Probabilidade (%)': [p * 100 for p in probabilities]
            }).sort_values('Probabilidade (%)', ascending=False)
            
            # Gráfico de barras
            fig = px.bar(
                prob_df,
                x='Nível de Obesidade',
                y='Probabilidade (%)',
                color='Probabilidade (%)',
                color_continuous_scale='Blues',
                title='Probabilidades por Nível de Obesidade'
            )
            fig.update_layout(
                xaxis_tickangle=-45,
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabela
            st.dataframe(prob_df, use_container_width=True, hide_index=True)
            
            # Recomendações
            st.markdown("---")
            st.subheader("💡 Recomendações")
            
            if 'Obesity' in prediction or 'Overweight' in prediction:
                st.warning("""
                **⚠️ Atenção:** O modelo indica risco de sobrepeso/obesidade. Recomenda-se:
                - Consultar um profissional de saúde
                - Avaliar hábitos alimentares
                - Aumentar atividade física regular
                - Monitorar peso e IMC periodicamente
                """)
            elif prediction == 'Normal_Weight':
                st.success("""
                **✅ Peso Normal:** Mantenha hábitos saudáveis:
                - Continue com alimentação balanceada
                - Mantenha atividade física regular
                - Monitore peso periodicamente
                """)
            else:
                st.info("""
                **ℹ️ Peso Insuficiente:** Consulte um nutricionista para:
                - Avaliar necessidades nutricionais
                - Desenvolver plano alimentar adequado
                - Monitorar ganho de peso saudável
                """)
            
            # Exportar PDF
            st.markdown("---")
            st.subheader("📄 Exportar Relatório")
            
            pdf_buffer = generate_pdf(medico_nome, medico_crm, paciente_nome, input_data, prediction, probabilities, classes)
            
            # Nome do arquivo PDF
            if paciente_nome and paciente_nome.strip():
                file_name = f"relatorio_obesidade_{paciente_nome.strip().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            else:
                file_name = f"relatorio_obesidade_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            st.download_button(
                label="📥 Baixar Relatório em PDF",
                data=pdf_buffer,
                file_name=file_name,
                mime="application/pdf",
                type="primary"
            )

# Página Insights e Métricas
elif selected == "Insights e Métricas":
    st.title("📊 Insights e Métricas")
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
        # Filtros no topo da página com estilo mais discreto
        st.markdown("""
        <div style="background-color: #005ca9e6; padding: 1rem 1.25rem; border-radius: 8px; margin-bottom: 1rem;">
            <h3 style="color: white !important; margin: 0 0 0.75rem 0; padding: 0; font-weight: 600; font-size: 1.1rem;">🔍 Filtros</h3>
        """, unsafe_allow_html=True)
        
        # Container para filtros
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            # Filtro por gênero (traduzido)
            gender_options_en = df['Gender'].unique()
            gender_options_pt = ['Masculino' if g == 'Male' else 'Feminino' for g in gender_options_en]
            gender_mapping = dict(zip(gender_options_pt, gender_options_en))
            
            gender_filter_pt = st.multiselect(
                "Gênero",
                options=gender_options_pt,
                default=gender_options_pt
            )
            # Converter de volta para inglês para filtro
            gender_filter = [gender_mapping[g] for g in gender_filter_pt]
        
        with filter_col2:
            # Filtro por nível de obesidade (traduzido)
            obesity_options_en = df['Obesity'].unique()
            obesity_options_pt = [OBESITY_LEVELS_PT.get(obs, obs) for obs in obesity_options_en]
            obesity_mapping = dict(zip(obesity_options_pt, obesity_options_en))
            
            obesity_filter_pt = st.multiselect(
                "Nível de Obesidade",
                options=obesity_options_pt,
                default=obesity_options_pt
            )
            # Converter de volta para inglês para filtro
            obesity_filter = [obesity_mapping[obs] for obs in obesity_filter_pt]
        
        with filter_col3:
            # Filtro por idade
            age_range = st.slider(
                "Faixa Etária (anos)",
                min_value=int(df['Age'].min()),
                max_value=int(df['Age'].max()),
                value=(int(df['Age'].min()), int(df['Age'].max()))
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Aplicar filtros
        df_filtered = df[
            (df['Gender'].isin(gender_filter)) &
            (df['Obesity'].isin(obesity_filter)) &
            (df['Age'] >= age_range[0]) &
            (df['Age'] <= age_range[1])
        ]
        
        # Mostrar quantidade de registros filtrados
        if len(df_filtered) < len(df):
            st.info(f"📊 Mostrando {len(df_filtered)} de {len(df)} registros com os filtros aplicados.")
        
        st.markdown("---")
        
        # Métricas principais
        st.header("📈 Métricas Principais")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Registros", len(df_filtered), delta=None)
        
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
            # Traduzir labels
            obesity_counts_pt = pd.Series({
                OBESITY_LEVELS_PT.get(k, k): v for k, v in obesity_counts.items()
            })
            
            fig_bar = px.bar(
                x=obesity_counts_pt.index,
                y=obesity_counts_pt.values,
                labels={'x': 'Nível de Obesidade', 'y': 'Frequência'},
                title='Distribuição de Níveis de Obesidade',
                color=obesity_counts_pt.values,
                color_continuous_scale='Blues'
            )
            fig_bar.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            # Gráfico de pizza
            fig_pie = px.pie(
                values=obesity_counts.values,
                names=[OBESITY_LEVELS_PT.get(k, k) for k in obesity_counts.index],
                title='Proporção de Níveis de Obesidade',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown("---")
        
        # Análise por Gênero
        st.header("👥 Análise por Gênero")
        
        col1, col2 = st.columns(2)
        
        with col1:
            gender_obesity = pd.crosstab(df_filtered['Gender'], df_filtered['Obesity'])
            # Traduzir colunas
            gender_obesity.columns = [OBESITY_LEVELS_PT.get(col, col) for col in gender_obesity.columns]
            gender_obesity.index = ['Feminino' if idx == 'Female' else 'Masculino' for idx in gender_obesity.index]
            
            fig_gender = px.bar(
                gender_obesity,
                barmode='group',
                title='Distribuição de Obesidade por Gênero',
                labels={'value': 'Frequência', 'Gender': 'Gênero'},
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_gender.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_gender, use_container_width=True)
        
        with col2:
            avg_bmi_gender = df_filtered.groupby('Gender')['BMI'].mean()
            avg_bmi_gender.index = ['Feminino' if idx == 'Female' else 'Masculino' for idx in avg_bmi_gender.index]
            
            fig_bmi_gender = px.bar(
                x=avg_bmi_gender.index,
                y=avg_bmi_gender.values,
                title='IMC Médio por Gênero',
                labels={'x': 'Gênero', 'y': 'IMC Médio'},
                color=avg_bmi_gender.values,
                color_continuous_scale='Oranges'
            )
            fig_bmi_gender.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
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
            age_obesity.columns = [OBESITY_LEVELS_PT.get(col, col) for col in age_obesity.columns]
            
            fig_age = px.bar(
                age_obesity,
                barmode='group',
                title='Distribuição de Obesidade por Faixa Etária',
                labels={'value': 'Frequência', 'Faixa Etária': 'Faixa Etária'},
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_age.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_age, use_container_width=True)
        
        with col2:
            # Scatter plot: Idade vs IMC
            df_filtered_plot = df_filtered.copy()
            df_filtered_plot['Obesity_PT'] = df_filtered_plot['Obesity'].map(OBESITY_LEVELS_PT)
            
            fig_scatter = px.scatter(
                df_filtered_plot,
                x='Age',
                y='BMI',
                color='Obesity_PT',
                title='Relação entre Idade e IMC',
                labels={'Age': 'Idade', 'BMI': 'IMC'},
                hover_data=['Gender', 'Weight', 'Height'],
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_scatter.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        st.markdown("---")
        
        # Análise de Hábitos
        st.header("🍽️ Análise de Hábitos e Estilo de Vida")
        
        # Atividade Física
        col1, col2 = st.columns(2)
        
        with col1:
            faf_obesity = pd.crosstab(df_filtered['FAF'], df_filtered['Obesity'])
            faf_obesity.columns = [OBESITY_LEVELS_PT.get(col, col) for col in faf_obesity.columns]
            
            fig_faf = px.bar(
                faf_obesity,
                barmode='group',
                title='Impacto da Atividade Física na Obesidade',
                labels={'value': 'Frequência', 'FAF': 'Frequência de Atividade Física'},
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_faf.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_faf, use_container_width=True)
        
        with col2:
            # Histórico familiar
            family_obesity = pd.crosstab(df_filtered['family_history'], df_filtered['Obesity'])
            family_obesity.columns = [OBESITY_LEVELS_PT.get(col, col) for col in family_obesity.columns]
            family_obesity.index = ['Sim' if idx == 'yes' else 'Não' for idx in family_obesity.index]
            
            fig_family = px.bar(
                family_obesity,
                barmode='group',
                title='Impacto do Histórico Familiar',
                labels={'value': 'Frequência', 'family_history': 'Histórico Familiar'},
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_family.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_family, use_container_width=True)
        
        # Consumo de alimentos calóricos
        col3, col4 = st.columns(2)
        
        with col3:
            favc_obesity = pd.crosstab(df_filtered['FAVC'], df_filtered['Obesity'])
            favc_obesity.columns = [OBESITY_LEVELS_PT.get(col, col) for col in favc_obesity.columns]
            favc_obesity.index = ['Sim' if idx == 'yes' else 'Não' for idx in favc_obesity.index]
            
            fig_favc = px.bar(
                favc_obesity,
                barmode='group',
                title='Impacto de Alimentos Altamente Calóricos',
                labels={'value': 'Frequência', 'FAVC': 'Alimentos Calóricos'},
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_favc.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_favc, use_container_width=True)
        
        with col4:
            # Consumo de vegetais
            fcvc_obesity = df_filtered.groupby('Obesity')['FCVC'].mean()
            fcvc_obesity.index = [OBESITY_LEVELS_PT.get(idx, idx) for idx in fcvc_obesity.index]
            
            fig_fcvc = px.bar(
                x=fcvc_obesity.index,
                y=fcvc_obesity.values,
                title='Consumo Médio de Vegetais por Nível de Obesidade',
                labels={'x': 'Nível de Obesidade', 'y': 'Consumo Médio de Vegetais'},
                color=fcvc_obesity.values,
                color_continuous_scale='Greens'
            )
            fig_fcvc.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_fcvc, use_container_width=True)
        
        st.markdown("---")
        
        # Análise de Correlação
        st.header("🔗 Análise de Correlação")
        st.markdown("""
        Esta seção apresenta a análise de correlação entre as variáveis numéricas e suas relações com o nível de obesidade.
        """)
        
        # Preparar dados numéricos para correlação
        numerical_cols = ['Age', 'Height', 'Weight', 'BMI', 'FCVC', 'NCP', 'CH2O', 'FAF', 'TUE']
        numerical_cols = [col for col in numerical_cols if col in df_filtered.columns]
        
        if len(numerical_cols) > 0:
            corr_df = df_filtered[numerical_cols].corr()
            
            # Heatmap de correlação
            fig_corr = go.Figure(data=go.Heatmap(
                z=corr_df.values,
                x=corr_df.columns,
                y=corr_df.columns,
                colorscale='RdBu',
                zmid=0,
                text=corr_df.round(2).values,
                texttemplate='%{text}',
                textfont={"size": 10},
                colorbar=dict(title="Correlação")
            ))
            fig_corr.update_layout(
                title='Matriz de Correlação entre Variáveis Numéricas',
                height=600,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_corr, use_container_width=True)
            
            # Análise de correlações específicas
            st.subheader("📊 Correlações com IMC e Obesidade")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Correlação IMC vs outras variáveis
                if 'BMI' in corr_df.columns:
                    bmi_corr = corr_df['BMI'].sort_values(ascending=False)
                    bmi_corr = bmi_corr[bmi_corr.index != 'BMI']
                    
                    fig_bmi_corr = px.bar(
                        x=bmi_corr.values,
                        y=bmi_corr.index,
                        orientation='h',
                        title='Correlação das Variáveis com IMC',
                        labels={'x': 'Correlação', 'y': 'Variável'},
                        color=bmi_corr.values,
                        color_continuous_scale='RdYlGn',
                        color_continuous_midpoint=0
                    )
                    fig_bmi_corr.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400
                    )
                    st.plotly_chart(fig_bmi_corr, use_container_width=True)
            
            with col2:
                # Tabela de correlações
                st.markdown("**Principais Correlações:**")
                corr_table = []
                for col in numerical_cols:
                    if col != 'BMI' and 'BMI' in corr_df.columns:
                        corr_val = corr_df.loc[col, 'BMI']
                        corr_table.append({
                            'Variável': col,
                            'Correlação com IMC': f"{corr_val:.3f}",
                            'Interpretação': 'Forte' if abs(corr_val) > 0.7 else 'Moderada' if abs(corr_val) > 0.4 else 'Fraca'
                        })
                
                if corr_table:
                    corr_table_df = pd.DataFrame(corr_table).sort_values('Correlação com IMC', key=lambda x: x.str.replace('Correlação com IMC', '').astype(float).abs(), ascending=False)
                    st.dataframe(corr_table_df, use_container_width=True, hide_index=True)
        
        # Conclusão da Análise de Correlação
        with st.expander("📝 Conclusão da Análise de Correlação", expanded=False):
            st.markdown("""
            **Principais Descobertas:**
            
            1. **IMC e Peso/Altura:** Como esperado, há forte correlação positiva entre IMC e Peso, e negativa com Altura.
            
            2. **Atividade Física:** A frequência de atividade física (FAF) geralmente apresenta correlação negativa com IMC, indicando que maior atividade física está associada a menor IMC.
            
            3. **Hábitos Alimentares:** Variáveis como consumo de vegetais (FCVC) e número de refeições (NCP) podem apresentar correlações interessantes com o IMC.
            
            4. **Idade:** A correlação entre idade e IMC pode variar, mas geralmente há uma relação positiva moderada.
            
            **Implicações Clínicas:**
            - Variáveis com alta correlação com IMC são importantes preditores
            - Correlações moderadas podem indicar fatores de risco ou proteção
            - A análise de correlação ajuda a identificar variáveis redundantes ou complementares
            """)
        
        st.markdown("---")
        
        # Análise de Boxplots
        st.header("📦 Análise de Boxplots")
        st.markdown("""
        Os boxplots mostram a distribuição das variáveis numéricas por nível de obesidade, permitindo identificar diferenças, outliers e padrões.
        """)
        
        # Boxplots por nível de obesidade
        boxplot_vars = ['Age', 'BMI', 'Weight', 'Height', 'FAF', 'FCVC']
        boxplot_vars = [var for var in boxplot_vars if var in df_filtered.columns]
        
        if len(boxplot_vars) > 0:
            # Selecionar variáveis para boxplot
            selected_boxplot_vars = st.multiselect(
                "Selecione as variáveis para análise de boxplot:",
                options=boxplot_vars,
                default=boxplot_vars[:4] if len(boxplot_vars) >= 4 else boxplot_vars
            )
            
            if selected_boxplot_vars:
                # Criar boxplots
                num_vars = len(selected_boxplot_vars)
                cols_per_row = 2
                num_rows = (num_vars + cols_per_row - 1) // cols_per_row
                
                for i in range(0, num_vars, cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j, var in enumerate(selected_boxplot_vars[i:i+cols_per_row]):
                        with cols[j]:
                            df_plot = df_filtered.copy()
                            df_plot['Obesity_PT'] = df_plot['Obesity'].map(OBESITY_LEVELS_PT)
                            
                            fig_box = px.box(
                                df_plot,
                                x='Obesity_PT',
                                y=var,
                                title=f'Distribuição de {var} por Nível de Obesidade',
                                color='Obesity_PT',
                                color_discrete_sequence=px.colors.qualitative.Set3
                            )
                            fig_box.update_layout(
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                xaxis_tickangle=-45,
                                showlegend=False,
                                height=400
                            )
                            st.plotly_chart(fig_box, use_container_width=True)
        
        # Conclusão da Análise de Boxplots
        with st.expander("📝 Conclusão da Análise de Boxplots", expanded=False):
            st.markdown("""
            **Principais Observações:**
            
            1. **Distribuição de IMC:** Os boxplots mostram claramente a separação entre diferentes níveis de obesidade, com medianas crescentes conforme o nível aumenta.
            
            2. **Outliers:** A presença de outliers pode indicar casos extremos que requerem atenção especial ou podem ser erros de medição.
            
            3. **Variabilidade:** A amplitude interquartil (IQR) mostra a variabilidade dentro de cada grupo. Grupos com maior IQR têm mais variabilidade.
            
            4. **Diferenças entre Grupos:** Boxplots permitem identificar visualmente diferenças significativas entre os níveis de obesidade para cada variável.
            
            5. **Idade e Outras Variáveis:** A distribuição da idade e outras características pode variar entre os grupos, indicando perfis diferentes.
            
            **Implicações:**
            - Identificação de grupos de risco com características distintas
            - Detecção de outliers que podem necessitar investigação adicional
            - Compreensão da variabilidade dentro de cada categoria de obesidade
            """)
        
        st.markdown("---")
        
        # Análise de Distribuição
        st.header("📊 Análise de Distribuição")
        st.markdown("""
        Esta seção apresenta análises detalhadas das distribuições das variáveis, incluindo histogramas, densidade e estatísticas descritivas.
        """)
        
        # Selecionar variáveis para análise de distribuição
        dist_vars = ['Age', 'BMI', 'Weight', 'Height', 'FAF', 'FCVC', 'NCP', 'CH2O', 'TUE']
        dist_vars = [var for var in dist_vars if var in df_filtered.columns]
        
        if len(dist_vars) > 0:
            selected_dist_var = st.selectbox(
                "Selecione a variável para análise de distribuição:",
                options=dist_vars
            )
            
            if selected_dist_var:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Histograma
                    fig_hist = px.histogram(
                        df_filtered,
                        x=selected_dist_var,
                        nbins=30,
                        title=f'Distribuição de {selected_dist_var}',
                        labels={selected_dist_var: selected_dist_var, 'count': 'Frequência'},
                        color_discrete_sequence=['#4CAF50']
                    )
                    fig_hist.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)
                
                with col2:
                    # Distribuição por nível de obesidade
                    df_plot = df_filtered.copy()
                    df_plot['Obesity_PT'] = df_plot['Obesity'].map(OBESITY_LEVELS_PT)
                    
                    fig_dist = px.histogram(
                        df_plot,
                        x=selected_dist_var,
                        color='Obesity_PT',
                        nbins=30,
                        title=f'Distribuição de {selected_dist_var} por Nível de Obesidade',
                        labels={selected_dist_var: selected_dist_var, 'count': 'Frequência'},
                        barmode='overlay',
                        opacity=0.7
                    )
                    fig_dist.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400
                    )
                    st.plotly_chart(fig_dist, use_container_width=True)
                
                # Estatísticas descritivas
                st.subheader(f"📈 Estatísticas Descritivas - {selected_dist_var}")
                
                stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
                
                with stats_col1:
                    st.metric("Média", f"{df_filtered[selected_dist_var].mean():.2f}")
                
                with stats_col2:
                    st.metric("Mediana", f"{df_filtered[selected_dist_var].median():.2f}")
                
                with stats_col3:
                    st.metric("Desvio Padrão", f"{df_filtered[selected_dist_var].std():.2f}")
                
                with stats_col4:
                    st.metric("Coef. Variação", f"{(df_filtered[selected_dist_var].std() / df_filtered[selected_dist_var].mean() * 100):.2f}%")
                
                # Estatísticas por nível de obesidade
                st.subheader(f"📊 Estatísticas por Nível de Obesidade - {selected_dist_var}")
                
                stats_by_obesity = df_filtered.groupby('Obesity')[selected_dist_var].agg(['mean', 'median', 'std', 'min', 'max']).round(2)
                stats_by_obesity.index = [OBESITY_LEVELS_PT.get(idx, idx) for idx in stats_by_obesity.index]
                stats_by_obesity.columns = ['Média', 'Mediana', 'Desvio Padrão', 'Mínimo', 'Máximo']
                st.dataframe(stats_by_obesity, use_container_width=True)
        
        # Conclusão da Análise de Distribuição
        with st.expander("📝 Conclusão da Análise de Distribuição", expanded=False):
            st.markdown("""
            **Principais Descobertas:**
            
            1. **Normalidade:** A análise de distribuição permite verificar se as variáveis seguem distribuição normal, o que é importante para alguns testes estatísticos.
            
            2. **Assimetria:** Distribuições assimétricas podem indicar que a maioria dos valores está concentrada em uma faixa específica.
            
            3. **Diferenças entre Grupos:** As distribuições por nível de obesidade mostram como cada variável se comporta em diferentes categorias.
            
            4. **Valores Extremos:** A identificação de valores extremos (mínimos e máximos) ajuda a entender a amplitude dos dados.
            
            5. **Variabilidade:** O coeficiente de variação indica a variabilidade relativa dos dados, útil para comparar variáveis com escalas diferentes.
            
            **Implicações:**
            - Compreensão da natureza dos dados e suas características
            - Identificação de padrões e tendências
            - Base para decisões sobre transformações de dados se necessário
            - Suporte para interpretação de resultados do modelo
            """)
        
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
            dominant_gender_pt = 'Feminino' if dominant_gender == 'Female' else 'Masculino'
            
            st.info(f"""
            **Gênero mais afetado:** {dominant_gender_pt}
            - Taxa de sobrepeso/obesidade: {gender_obesity_rate[dominant_gender]:.1f}%
            """)
            
            # Insight 2: Atividade Física
            faf_impact = df_filtered.groupby('FAF')['Obesity'].apply(
                lambda x: (x.str.contains('Obesity|Overweight').sum() / len(x)) * 100
            )
            low_activity = (faf_impact.get(0.0, 0) + faf_impact.get(1.0, 0)) / 2 if (faf_impact.get(0.0, 0) + faf_impact.get(1.0, 0)) > 0 else 0
            high_activity = (faf_impact.get(2.0, 0) + faf_impact.get(3.0, 0)) / 2 if (faf_impact.get(2.0, 0) + faf_impact.get(3.0, 0)) > 0 else 0
            
            st.info(f"""
            **Atividade Física:**
            - Baixa atividade (0-1): {low_activity:.1f}% de sobrepeso/obesidade
            - Alta atividade (2-3): {high_activity:.1f}% de sobrepeso/obesidade
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
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; padding: 2rem;'>
        <p>Sistema desenvolvido para o Tech Challenge 4 - FIAP | Uso exclusivo para fins educacionais</p>
    </div>
    """, unsafe_allow_html=True)
