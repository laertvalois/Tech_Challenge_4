"""
Script para instalar todas as dependências do projeto
Tech Challenge - Sistema Preditivo de Obesidade
"""
import subprocess
import sys
import os

def check_and_install():
    """Verifica e instala dependências"""
    print("=" * 60)
    print("📦 Instalando dependências do projeto")
    print("=" * 60)
    print()
    
    requirements_file = "requirements.txt"
    
    if not os.path.exists(requirements_file):
        print(f"❌ Erro: Arquivo {requirements_file} não encontrado.")
        print(f"   Certifique-se de estar na pasta raiz do projeto.")
        return False
    
    print(f"📄 Lendo {requirements_file}...")
    print()
    
    try:
        # Instalar dependências
        print("🔄 Instalando pacotes...")
        print()
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", requirements_file],
            check=True,
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        
        if result.stderr:
            print("⚠️  Avisos:")
            print(result.stderr)
        
        print()
        print("=" * 60)
        print("✅ Dependências instaladas com sucesso!")
        print("=" * 60)
        print()
        print("📋 Pacotes principais instalados:")
        print("   - streamlit (aplicação web)")
        print("   - pandas, numpy (manipulação de dados)")
        print("   - scikit-learn (machine learning)")
        print("   - plotly (visualizações)")
        print("   - reportlab (geração de PDF)")
        print("   - streamlit-option-menu (menu lateral)")
        print()
        print("🚀 Agora você pode executar: python run_app.py")
        print()
        
        return True
        
    except subprocess.CalledProcessError as e:
        print()
        print("=" * 60)
        print("❌ Erro ao instalar dependências")
        print("=" * 60)
        print()
        print(f"Erro: {e}")
        if e.stdout:
            print("Saída:")
            print(e.stdout)
        if e.stderr:
            print("Erros:")
            print(e.stderr)
        print()
        print("💡 Tente executar manualmente:")
        print(f"   pip install -r {requirements_file}")
        return False
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ Erro inesperado")
        print("=" * 60)
        print(f"Erro: {e}")
        return False

if __name__ == "__main__":
    success = check_and_install()
    sys.exit(0 if success else 1)
