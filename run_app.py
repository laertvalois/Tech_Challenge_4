"""
Script principal para executar a aplicação Streamlit
"""
import subprocess
import sys
import os

if __name__ == "__main__":
    app_path = os.path.join("app", "app.py")
    if os.path.exists(app_path):
        subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])
    else:
        print(f"Erro: Arquivo {app_path} não encontrado.")

