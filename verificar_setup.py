"""
Script de verificação do setup do projeto
Verifica se todos os componentes estão prontos
"""
import os
import sys

def verificar_arquivos():
    """Verifica se todos os arquivos necessários existem"""
    arquivos_necessarios = [
        'data/obesity.csv',
        'data/obesity.db',
        'models/obesity_model.joblib',
        'models/preprocessor.joblib',
        'app/app.py',
        'dashboard/dashboard.py',
        'src/data_preprocessing.py',
        'src/train_model.py',
        'src/load_model.py',
        'requirements.txt',
        'README.md'
    ]
    
    print("=" * 60)
    print("VERIFICAÇÃO DE ARQUIVOS")
    print("=" * 60)
    
    todos_ok = True
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo} - FALTANDO")
            todos_ok = False
    
    return todos_ok

def verificar_imports():
    """Verifica se os imports estão funcionando"""
    print("\n" + "=" * 60)
    print("VERIFICAÇÃO DE IMPORTS")
    print("=" * 60)
    
    try:
        import pandas as pd
        print("✅ pandas")
    except ImportError:
        print("❌ pandas - NÃO INSTALADO")
        return False
    
    try:
        import numpy as np
        print("✅ numpy")
    except ImportError:
        print("❌ numpy - NÃO INSTALADO")
        return False
    
    try:
        import sklearn
        print("✅ scikit-learn")
    except ImportError:
        print("❌ scikit-learn - NÃO INSTALADO")
        return False
    
    try:
        import streamlit
        print("✅ streamlit")
    except ImportError:
        print("❌ streamlit - NÃO INSTALADO")
        return False
    
    try:
        import plotly
        print("✅ plotly")
    except ImportError:
        print("❌ plotly - NÃO INSTALADO")
        return False
    
    return True

def verificar_modelo():
    """Verifica se o modelo pode ser carregado"""
    print("\n" + "=" * 60)
    print("VERIFICAÇÃO DO MODELO")
    print("=" * 60)
    
    try:
        sys.path.append('src')
        from load_model import load_trained_model, load_preprocessor
        
        if os.path.exists('models/obesity_model.joblib'):
            model = load_trained_model('models/obesity_model.joblib')
            print("✅ Modelo carregado com sucesso")
        else:
            print("❌ Modelo não encontrado - Execute train_model.py primeiro")
            return False
        
        if os.path.exists('models/preprocessor.joblib'):
            preprocessor = load_preprocessor('models/preprocessor.joblib')
            print("✅ Pré-processador carregado com sucesso")
        else:
            print("❌ Pré-processador não encontrado")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Erro ao carregar modelo: {e}")
        return False

def main():
    """Função principal"""
    print("\n🔍 VERIFICAÇÃO DO SETUP DO PROJETO\n")
    
    arquivos_ok = verificar_arquivos()
    imports_ok = verificar_imports()
    modelo_ok = verificar_modelo()
    
    print("\n" + "=" * 60)
    print("RESUMO")
    print("=" * 60)
    
    if arquivos_ok and imports_ok and modelo_ok:
        print("✅ TUDO PRONTO! O projeto está configurado corretamente.")
        print("\nPróximos passos:")
        print("1. Execute: streamlit run app/app.py (para aplicação)")
        print("2. Execute: streamlit run dashboard/dashboard.py (para dashboard)")
        return True
    else:
        print("❌ ALGUNS PROBLEMAS ENCONTRADOS")
        if not arquivos_ok:
            print("   - Alguns arquivos estão faltando")
        if not imports_ok:
            print("   - Execute: pip install -r requirements.txt")
        if not modelo_ok:
            print("   - Execute: python src/train_model.py")
        return False

if __name__ == "__main__":
    main()

