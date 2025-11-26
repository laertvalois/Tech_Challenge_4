"""
Pré-processamento de Dados
Tech Challenge - Sistema Preditivo de Obesidade
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os

class DataPreprocessor:
    """Classe para pré-processamento dos dados"""
    
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_names = None
        
    def load_data(self, filepath='data/obesity.csv'):
        """Carrega os dados"""
        df = pd.read_csv(filepath)
        return df
    
    def create_bmi(self, df):
        """Cria feature IMC (Índice de Massa Corporal)"""
        if 'Height' in df.columns and 'Weight' in df.columns:
            df['BMI'] = df['Weight'] / (df['Height'] ** 2)
        return df
    
    def handle_missing_values(self, df):
        """Trata valores faltantes"""
        # Verificar valores faltantes
        missing = df.isnull().sum()
        if missing.sum() > 0:
            print(f"Valores faltantes encontrados:\n{missing[missing > 0]}")
            # Preencher com moda para categóricas e mediana para numéricas
            for col in df.columns:
                if df[col].isnull().sum() > 0:
                    if df[col].dtype == 'object':
                        df[col].fillna(df[col].mode()[0], inplace=True)
                    else:
                        df[col].fillna(df[col].median(), inplace=True)
        return df
    
    def encode_categorical(self, df, fit=True):
        """Codifica variáveis categóricas"""
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        # Remover variável alvo se estiver presente
        if 'Obesity' in categorical_cols:
            categorical_cols.remove('Obesity')
        
        for col in categorical_cols:
            if fit:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                self.label_encoders[col] = le
            else:
                if col in self.label_encoders:
                    # Para dados novos, usar transform existente
                    # Valores não vistos serão tratados
                    try:
                        df[col] = self.label_encoders[col].transform(df[col].astype(str))
                    except ValueError:
                        # Se houver valor novo, usar o mais comum
                        df[col] = df[col].map(
                            lambda x: self.label_encoders[col].transform([x])[0] 
                            if x in self.label_encoders[col].classes_ 
                            else 0
                        )
        return df
    
    def prepare_features(self, df, target_col='Obesity'):
        """Prepara features e target"""
        # Criar IMC
        df = self.create_bmi(df)
        
        # Separar features e target
        X = df.drop(columns=[target_col])
        y = df[target_col]
        
        # Salvar nomes das features
        self.feature_names = X.columns.tolist()
        
        return X, y
    
    def scale_features(self, X, fit=True):
        """Normaliza features numéricas"""
        if fit:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = self.scaler.transform(X)
        
        # Converter de volta para DataFrame
        X_scaled = pd.DataFrame(X_scaled, columns=self.feature_names, index=X.index)
        return X_scaled
    
    def preprocess(self, df, target_col='Obesity', fit=True, scale=True):
        """
        Pipeline completo de pré-processamento
        
        Args:
            df: DataFrame com os dados
            target_col: Nome da coluna alvo
            fit: Se True, ajusta os encoders/scalers (treinamento)
            scale: Se True, normaliza as features
        """
        # Tratar valores faltantes
        df = self.handle_missing_values(df)
        
        # Codificar categóricas
        df = self.encode_categorical(df, fit=fit)
        
        # Preparar features e target
        X, y = self.prepare_features(df, target_col=target_col)
        
        # Normalizar
        if scale:
            X = self.scale_features(X, fit=fit)
        
        return X, y
    
    def save_preprocessor(self, filepath='models/preprocessor.joblib'):
        """Salva o pré-processador"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump({
            'label_encoders': self.label_encoders,
            'scaler': self.scaler,
            'feature_names': self.feature_names
        }, filepath)
        print(f"✅ Pré-processador salvo em {filepath}")
    
    def load_preprocessor(self, filepath='models/preprocessor.joblib'):
        """Carrega o pré-processador"""
        preprocessor_data = joblib.load(filepath)
        self.label_encoders = preprocessor_data['label_encoders']
        self.scaler = preprocessor_data['scaler']
        self.feature_names = preprocessor_data['feature_names']
        print(f"✅ Pré-processador carregado de {filepath}")

def split_data(X, y, test_size=0.2, random_state=42):
    """Divide os dados em treino e teste"""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    print(f"✅ Dados divididos:")
    print(f"   Treino: {X_train.shape[0]} amostras")
    print(f"   Teste: {X_test.shape[0]} amostras")
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    # Teste do pré-processador
    preprocessor = DataPreprocessor()
    df = preprocessor.load_data('data/obesity.csv')
    X, y = preprocessor.preprocess(df, fit=True, scale=True)
    preprocessor.save_preprocessor()
    
    print(f"\nShape final: {X.shape}")
    print(f"Features: {list(X.columns)}")
    print(f"Target classes: {y.unique()}")

