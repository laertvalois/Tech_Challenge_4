"""
Utilitário para carregar modelo e pré-processador
"""
import joblib
import os

def load_trained_model(model_path='models/obesity_model.joblib'):
    """Carrega o modelo treinado"""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modelo não encontrado em {model_path}. Execute train_model.py primeiro.")
    return joblib.load(model_path)

def load_preprocessor(preprocessor_path='models/preprocessor.joblib'):
    """Carrega o pré-processador"""
    if not os.path.exists(preprocessor_path):
        raise FileNotFoundError(f"Pré-processador não encontrado em {preprocessor_path}.")
    return joblib.load(preprocessor_path)

