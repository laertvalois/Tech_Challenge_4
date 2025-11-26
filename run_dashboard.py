"""
Script principal para executar o dashboard Streamlit
"""
import subprocess
import sys
import os

if __name__ == "__main__":
    dashboard_path = os.path.join("dashboard", "dashboard.py")
    if os.path.exists(dashboard_path):
        subprocess.run([sys.executable, "-m", "streamlit", "run", dashboard_path])
    else:
        print(f"Erro: Arquivo {dashboard_path} não encontrado.")

