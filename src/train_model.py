"""
Treinamento do Modelo de Machine Learning
Tech Challenge - Sistema Preditivo de Obesidade
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    f1_score, precision_score, recall_score
)
from sklearn.model_selection import cross_val_score, GridSearchCV
import joblib
import os
from data_preprocessing import DataPreprocessor, split_data

class ModelTrainer:
    """Classe para treinamento de modelos"""
    
    def __init__(self):
        self.models = {}
        self.best_model = None
        self.best_score = 0
        self.preprocessor = DataPreprocessor()
        
    def load_data(self, filepath='data/obesity.csv'):
        """Carrega e pré-processa os dados"""
        df = self.preprocessor.load_data(filepath)
        X, y = self.preprocessor.preprocess(df, fit=True, scale=True)
        return X, y
    
    def train_models(self, X_train, y_train, X_test, y_test):
        """Treina múltiplos modelos e seleciona o melhor"""
        
        models_to_test = {
            'RandomForest': RandomForestClassifier(
                n_estimators=100,
                max_depth=20,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            ),
            'GradientBoosting': GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            ),
            'LogisticRegression': LogisticRegression(
                max_iter=1000,
                random_state=42,
                solver='lbfgs'
            ),
            'SVM': SVC(
                kernel='rbf',
                probability=True,
                random_state=42
            )
        }
        
        results = {}
        
        print("=" * 60)
        print("TREINANDO MODELOS")
        print("=" * 60)
        
        for name, model in models_to_test.items():
            print(f"\n🔹 Treinando {name}...")
            
            # Treinar modelo
            model.fit(X_train, y_train)
            
            # Predições
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)
            
            # Métricas
            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average='weighted')
            precision = precision_score(y_test, y_pred, average='weighted')
            recall = recall_score(y_test, y_pred, average='weighted')
            
            # Validação cruzada
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
            
            results[name] = {
                'model': model,
                'accuracy': accuracy,
                'f1_score': f1,
                'precision': precision,
                'recall': recall,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std()
            }
            
            print(f"   Acurácia: {accuracy:.4f}")
            print(f"   F1-Score: {f1:.4f}")
            print(f"   CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
            
            self.models[name] = model
        
        # Selecionar melhor modelo (baseado em F1-Score)
        best_model_name = max(results, key=lambda x: results[x]['f1_score'])
        self.best_model = results[best_model_name]['model']
        self.best_score = results[best_model_name]['f1_score']
        
        print("\n" + "=" * 60)
        print(f"🏆 MELHOR MODELO: {best_model_name}")
        print("=" * 60)
        print(f"Acurácia: {results[best_model_name]['accuracy']:.4f}")
        print(f"F1-Score: {results[best_model_name]['f1_score']:.4f}")
        print(f"Precision: {results[best_model_name]['precision']:.4f}")
        print(f"Recall: {results[best_model_name]['recall']:.4f}")
        
        # Relatório detalhado do melhor modelo
        y_pred_best = self.best_model.predict(X_test)
        print("\n" + "=" * 60)
        print("RELATÓRIO DE CLASSIFICAÇÃO")
        print("=" * 60)
        print(classification_report(y_test, y_pred_best))
        
        print("\n" + "=" * 60)
        print("MATRIZ DE CONFUSÃO")
        print("=" * 60)
        print(confusion_matrix(y_test, y_pred_best))
        
        return results
    
    def tune_hyperparameters(self, X_train, y_train, model_name='RandomForest'):
        """Ajusta hiperparâmetros do modelo"""
        print(f"\n🔧 Ajustando hiperparâmetros para {model_name}...")
        
        if model_name == 'RandomForest':
            param_grid = {
                'n_estimators': [100, 200],
                'max_depth': [15, 20, 25],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }
            base_model = RandomForestClassifier(random_state=42, n_jobs=-1)
        else:
            return None
        
        grid_search = GridSearchCV(
            base_model,
            param_grid,
            cv=5,
            scoring='f1_weighted',
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        
        print(f"Melhores parâmetros: {grid_search.best_params_}")
        print(f"Melhor score: {grid_search.best_score_:.4f}")
        
        return grid_search.best_estimator_
    
    def save_model(self, model, filepath='models/obesity_model.joblib'):
        """Salva o modelo treinado"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(model, filepath)
        print(f"✅ Modelo salvo em {filepath}")
    
    def save_preprocessor(self, filepath='models/preprocessor.joblib'):
        """Salva o pré-processador"""
        self.preprocessor.save_preprocessor(filepath)

def main():
    """Função principal"""
    print("Iniciando treinamento do modelo...")
    
    # Inicializar trainer
    trainer = ModelTrainer()
    
    # Carregar e pré-processar dados
    X, y = trainer.load_data('data/obesity.csv')
    
    # Dividir dados
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    # Treinar modelos
    results = trainer.train_models(X_train, y_train, X_test, y_test)
    
    # Verificar se atende requisito de 75%
    best_accuracy = max(r['accuracy'] for r in results.values())
    if best_accuracy >= 0.75:
        print(f"\n✅ Requisito atendido! Acurácia: {best_accuracy:.2%} >= 75%")
    else:
        print(f"\n⚠️ Acurácia abaixo do requisito: {best_accuracy:.2%} < 75%")
        print("Considerando ajuste de hiperparâmetros...")
    
    # Salvar melhor modelo e pré-processador
    trainer.save_model(trainer.best_model)
    trainer.save_preprocessor()
    
    print("\n✅ Treinamento concluído!")

if __name__ == "__main__":
    main()

