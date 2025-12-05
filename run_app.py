"""
Script principal para executar a aplicação Streamlit Unificada
Tech Challenge - Sistema Preditivo de Obesidade
"""
import subprocess
import sys
import os

def main():
    """Executa a aplicação Streamlit"""
    # Caminho do arquivo principal da aplicação
    app_path = os.path.join("app", "app.py")
    
    # Verificar se o arquivo existe
    if not os.path.exists(app_path):
        print(f"❌ Erro: Arquivo {app_path} não encontrado.")
        print(f"   Certifique-se de estar na pasta raiz do projeto (tech_challenge/)")
        sys.exit(1)
    
    # Verificar se as dependências estão instaladas
    missing_modules = []
    
    try:
        import streamlit
    except ImportError:
        missing_modules.append("streamlit")
    
    try:
        import reportlab
    except ImportError:
        missing_modules.append("reportlab")
    
    try:
        import pandas
    except ImportError:
        missing_modules.append("pandas")
    
    try:
        from streamlit_option_menu import option_menu
    except ImportError:
        missing_modules.append("streamlit-option-menu")
    
    if missing_modules:
        print("❌ Erro: Módulos não encontrados:")
        for module in missing_modules:
            print(f"   - {module}")
        print()
        print("💡 Para instalar todas as dependências, execute:")
        print("   pip install -r requirements.txt")
        print()
        print("   Ou use o script de instalação:")
        print("   python install_dependencies.py")
        sys.exit(1)
    
    # Verificar se a porta está em uso e encontrar porta alternativa
    import socket
    
    def is_port_in_use(port):
        """Verifica se uma porta está em uso"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0
    
    def find_free_port(start_port=8501, max_attempts=10):
        """Encontra uma porta livre"""
        for i in range(max_attempts):
            port = start_port + i
            if not is_port_in_use(port):
                return port
        return None
    
    base_port = 8501
    port = base_port
    
    if is_port_in_use(base_port):
        print("⚠️  Porta 8501 já está em uso.")
        free_port = find_free_port(base_port)
        if free_port:
            port = free_port
            print(f"   Usando porta alternativa: {port}")
        else:
            print("❌ Não foi possível encontrar uma porta livre.")
            print("   Feche outras instâncias do Streamlit ou reinicie o computador.")
            sys.exit(1)
        print()
    
    print("=" * 50)
    print("🚀 Iniciando Sistema Preditivo de Obesidade")
    print("=" * 50)
    print(f"📁 Arquivo: {app_path}")
    print(f"🌐 A aplicação abrirá automaticamente no navegador")
    print(f"   URL: http://localhost:{port}")
    print("=" * 50)
    print()
    
    # Executar Streamlit
    try:
        subprocess.run([
            sys.executable, 
            "-m", 
            "streamlit", 
            "run", 
            app_path,
            "--server.headless", "false",
            "--server.port", str(port)
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar a aplicação: {e}")
        print()
        print("💡 Possíveis soluções:")
        print("   1. Feche outras instâncias do Streamlit em execução")
        print("   2. Execute manualmente: streamlit run app/app.py --server.port 8502")
        print("   3. Reinicie o terminal e tente novamente")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n✅ Aplicação encerrada pelo usuário.")
        sys.exit(0)

if __name__ == "__main__":
    main()

