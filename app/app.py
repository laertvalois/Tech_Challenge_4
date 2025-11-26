"""
Aplicação Streamlit - Sistema Preditivo de Obesidade
Tech Challenge
"""
import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

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

# Título principal
st.title("🏥 Sistema Preditivo de Obesidade")
st.markdown("---")
st.markdown("""
Este sistema utiliza Machine Learning para auxiliar médicos e médicas na previsão do nível de obesidade de pacientes.
Preencha os dados abaixo para obter uma predição.
""")

# Sidebar com informações
with st.sidebar:
    st.header("ℹ️ Sobre o Sistema")
    st.markdown("""
    Este sistema foi desenvolvido como parte do Tech Challenge.
    
    **Funcionalidades:**
    - Predição do nível de obesidade
    - Análise de probabilidades por classe
    - Recomendações baseadas nos dados
    
    **Modelo:**
    - Algoritmo: Random Forest
    - Acurácia: > 75%
    """)
    
    st.markdown("---")
    st.markdown("**Desenvolvido para auxiliar profissionais de saúde**")

# Função para criar formulário
def create_input_form():
    """Cria formulário de entrada de dados"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Dados Demográficos")
        gender = st.selectbox("Gênero", ["Male", "Female"])
        age = st.number_input("Idade", min_value=1, max_value=120, value=30)
        height = st.number_input("Altura (metros)", min_value=0.5, max_value=2.5, value=1.70, step=0.01)
        weight = st.number_input("Peso (kg)", min_value=10.0, max_value=300.0, value=70.0, step=0.1)
        
        # Calcular IMC
        if height > 0:
            bmi = weight / (height ** 2)
            st.info(f"**IMC Calculado:** {bmi:.2f}")
    
    with col2:
        st.subheader("🍽️ Hábitos Alimentares")
        family_history = st.selectbox("Histórico familiar de excesso de peso", ["yes", "no"])
        favc = st.selectbox("Come alimentos altamente calóricos com frequência?", ["yes", "no"])
        fcvc = st.number_input("Frequência de consumo de vegetais (1-3)", min_value=1.0, max_value=3.0, value=2.0, step=0.1)
        ncp = st.number_input("Número de refeições principais diárias (1-4)", min_value=1.0, max_value=4.0, value=3.0, step=0.1)
        caec = st.selectbox("Come algo entre as refeições?", ["no", "Sometimes", "Frequently", "Always"])
        ch2o = st.number_input("Quantidade de água diária (1-3)", min_value=1.0, max_value=3.0, value=2.0, step=0.1)
        scc = st.selectbox("Monitora as calorias ingeridas?", ["yes", "no"])
    
    st.markdown("---")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("🏃 Estilo de Vida")
        smoke = st.selectbox("Fuma?", ["yes", "no"])
        faf = st.number_input("Frequência de atividade física (0-3)", min_value=0.0, max_value=3.0, value=1.0, step=0.1)
        tue = st.number_input("Tempo em dispositivos tecnológicos (0-2)", min_value=0.0, max_value=2.0, value=1.0, step=0.1)
        calc = st.selectbox("Frequência de consumo de álcool", ["no", "Sometimes", "Frequently"])
    
    with col4:
        st.subheader("🚗 Transporte")
        mtrans = st.selectbox("Meio de transporte", [
            "Public_Transportation",
            "Automobile",
            "Walking",
            "Motorbike",
            "Bike"
        ])
    
    return {
        'Gender': gender,
        'Age': age,
        'Height': height,
        'Weight': weight,
        'family_history': family_history,
        'FAVC': favc,
        'FCVC': fcvc,
        'NCP': ncp,
        'CAEC': caec,
        'SMOKE': smoke,
        'CH2O': ch2o,
        'SCC': scc,
        'FAF': faf,
        'TUE': tue,
        'CALC': calc,
        'MTRANS': mtrans
    }

# Função para fazer predição
def make_prediction(input_data):
    """Faz predição usando o modelo treinado"""
    try:
        # Carregar modelo e pré-processador
        model = load_trained_model('models/obesity_model.joblib')
        preprocessor_data = load_preprocessor('models/preprocessor.joblib')
        
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

# Interface principal
st.header("📝 Formulário de Entrada")

# Criar formulário
input_data = create_input_form()

# Botão de predição
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

with col_btn2:
    predict_button = st.button("🔮 Fazer Predição", type="primary", use_container_width=True)

# Fazer predição
if predict_button:
    with st.spinner("Processando predição..."):
        prediction, probabilities, classes = make_prediction(input_data)
        
        if prediction is not None:
            st.markdown("---")
            st.header("📊 Resultado da Predição")
            
            # Resultado principal
            prediction_pt = OBESITY_LEVELS_PT.get(prediction, prediction)
            
            # Container para resultado
            result_container = st.container()
            with result_container:
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown(f"### 🎯 Nível de Obesidade Previsto:")
                    st.markdown(f"# {prediction_pt}")
                    
                    # Probabilidade da classe predita
                    pred_idx = list(classes).index(prediction)
                    confidence = probabilities[pred_idx] * 100
                    st.progress(confidence / 100)
                    st.caption(f"Confiança: {confidence:.2f}%")
            
            # Probabilidades por classe
            st.markdown("---")
            st.subheader("📈 Probabilidades por Classe")
            
            # Criar DataFrame com probabilidades
            prob_df = pd.DataFrame({
                'Nível de Obesidade': [OBESITY_LEVELS_PT.get(c, c) for c in classes],
                'Probabilidade (%)': [p * 100 for p in probabilities]
            }).sort_values('Probabilidade (%)', ascending=False)
            
            # Gráfico de barras
            st.bar_chart(prob_df.set_index('Nível de Obesidade'))
            
            # Tabela
            st.dataframe(prob_df, use_container_width=True, hide_index=True)
            
            # Recomendações
            st.markdown("---")
            st.subheader("💡 Recomendações")
            
            if 'Obesity' in prediction or 'Overweight' in prediction:
                st.warning("""
                **Atenção:** O modelo indica risco de sobrepeso/obesidade. Recomenda-se:
                - Consultar um profissional de saúde
                - Avaliar hábitos alimentares
                - Aumentar atividade física regular
                - Monitorar peso e IMC periodicamente
                """)
            elif prediction == 'Normal_Weight':
                st.success("""
                **Peso Normal:** Mantenha hábitos saudáveis:
                - Continue com alimentação balanceada
                - Mantenha atividade física regular
                - Monitore peso periodicamente
                """)
            else:
                st.info("""
                **Peso Insuficiente:** Consulte um nutricionista para:
                - Avaliar necessidades nutricionais
                - Desenvolver plano alimentar adequado
                - Monitorar ganho de peso saudável
                """)

# Rodapé
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Sistema desenvolvido para o Tech Challenge | Uso exclusivo para fins educacionais</p>
</div>
""", unsafe_allow_html=True)

