"""
Script principal para executar a aplicação Streamlit Unificada
"""
import subprocess
import sys
import os

if __name__ == "__main__":
    # Tentar app unificado primeiro
    app_path = os.path.join("app", "main.py")
    if not os.path.exists(app_path):
        # Fallback para app.py antigo
        app_path = os.path.join("app", "app.py")
    
    if os.path.exists(app_path):
        subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])
    else:
        print(f"Erro: Arquivo {app_path} não encontrado.")

