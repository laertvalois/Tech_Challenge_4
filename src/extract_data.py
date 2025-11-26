"""
Script para extrair dados do banco SQLite e converter para CSV
"""
import sqlite3
import pandas as pd
import os

def extract_sqlite_to_csv(db_path='data/obesity.db', output_path='data/obesity.csv'):
    """
    Extrai dados do banco SQLite e salva como CSV
    
    Args:
        db_path: Caminho para o arquivo SQLite
        output_path: Caminho de saída para o CSV
    """
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect(db_path)
        
        # Listar todas as tabelas
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"Tabelas encontradas: {[table[0] for table in tables]}")
        
        # Se houver tabelas, extrair a primeira (ou a principal)
        if tables:
            table_name = tables[0][0]
            print(f"Extraindo dados da tabela: {table_name}")
            
            # Ler dados da tabela
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            
            # Salvar como CSV
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            df.to_csv(output_path, index=False)
            
            print(f"✅ Dados extraídos com sucesso!")
            print(f"   Total de registros: {len(df)}")
            print(f"   Colunas: {list(df.columns)}")
            print(f"   Arquivo salvo em: {output_path}")
            
            return df
        else:
            print("⚠️ Nenhuma tabela encontrada no banco de dados")
            return None
            
    except sqlite3.Error as e:
        print(f"❌ Erro ao acessar o banco de dados: {e}")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return None
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    extract_sqlite_to_csv()

