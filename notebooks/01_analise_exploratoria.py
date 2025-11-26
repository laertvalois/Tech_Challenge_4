"""
Análise Exploratória de Dados (EDA)
Tech Challenge - Sistema Preditivo de Obesidade
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configurações
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
pd.set_option('display.max_columns', None)

def load_data():
    """Carrega os dados"""
    df = pd.read_csv('../data/obesity.csv')
    return df

def basic_info(df):
    """Informações básicas sobre o dataset"""
    print("=" * 60)
    print("INFORMAÇÕES BÁSICAS DO DATASET")
    print("=" * 60)
    print(f"\nShape: {df.shape}")
    print(f"\nColunas: {list(df.columns)}")
    print(f"\nTipos de dados:\n{df.dtypes}")
    print(f"\nValores faltantes:\n{df.isnull().sum()}")
    print(f"\nEstatísticas descritivas:\n{df.describe()}")
    print(f"\nPrimeiras linhas:\n{df.head()}")
    
def target_distribution(df):
    """Distribuição da variável alvo"""
    print("\n" + "=" * 60)
    print("DISTRIBUIÇÃO DA VARIÁVEL ALVO (Obesity)")
    print("=" * 60)
    print(df['Obesity'].value_counts())
    print(f"\nPercentual:\n{df['Obesity'].value_counts(normalize=True) * 100}")
    
    # Gráfico
    fig, ax = plt.subplots(figsize=(12, 6))
    df['Obesity'].value_counts().plot(kind='bar', ax=ax)
    ax.set_title('Distribuição dos Níveis de Obesidade', fontsize=14, fontweight='bold')
    ax.set_xlabel('Nível de Obesidade', fontsize=12)
    ax.set_ylabel('Frequência', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('../dashboard/images/target_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

def numerical_analysis(df):
    """Análise de variáveis numéricas"""
    print("\n" + "=" * 60)
    print("ANÁLISE DE VARIÁVEIS NUMÉRICAS")
    print("=" * 60)
    
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    print(f"\nVariáveis numéricas: {numerical_cols}")
    
    # Criar IMC
    if 'Height' in df.columns and 'Weight' in df.columns:
        df['BMI'] = df['Weight'] / (df['Height'] ** 2)
        print(f"\nIMC criado - Estatísticas:\n{df['BMI'].describe()}")
    
    return df

def categorical_analysis(df):
    """Análise de variáveis categóricas"""
    print("\n" + "=" * 60)
    print("ANÁLISE DE VARIÁVEIS CATEGÓRICAS")
    print("=" * 60)
    
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    categorical_cols.remove('Obesity')  # Remover variável alvo
    
    for col in categorical_cols:
        print(f"\n{col}:")
        print(df[col].value_counts())
        print(f"Valores únicos: {df[col].nunique()}")

def correlation_analysis(df):
    """Análise de correlações"""
    print("\n" + "=" * 60)
    print("ANÁLISE DE CORRELAÇÕES")
    print("=" * 60)
    
    # Selecionar apenas numéricas
    numerical_df = df.select_dtypes(include=[np.number])
    
    if 'BMI' in df.columns:
        numerical_df['BMI'] = df['BMI']
    
    corr_matrix = numerical_df.corr()
    print(corr_matrix)
    
    # Heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title('Matriz de Correlação', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('../dashboard/images/correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """Função principal"""
    print("Iniciando Análise Exploratória de Dados...")
    
    # Carregar dados
    df = load_data()
    
    # Análises
    basic_info(df)
    target_distribution(df)
    df = numerical_analysis(df)
    categorical_analysis(df)
    correlation_analysis(df)
    
    # Salvar dataset com IMC
    df.to_csv('../data/obesity_with_bmi.csv', index=False)
    print("\n✅ Análise concluída! Dataset salvo com IMC calculado.")
    
    return df

if __name__ == "__main__":
    import os
    os.makedirs('../dashboard/images', exist_ok=True)
    df = main()

