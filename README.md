# Tech Challenge - Sistema Preditivo de Obesidade

## 📋 Sobre o Projeto

Este projeto foi desenvolvido como parte do Tech Challenge, com o objetivo de criar um sistema de Machine Learning para auxiliar médicos e médicas a prever se uma pessoa pode ter obesidade.

## 🎯 Objetivos

- Desenvolver um modelo preditivo com assertividade acima de 75%
- Criar uma aplicação Streamlit para predição em tempo real
- Construir um dashboard analítico com insights sobre obesidade
- Fornecer ferramentas para auxiliar a tomada de decisão da equipe médica

## 📊 Dados

O banco de dados SQLite (`data/obesity.db`) contém informações sobre:
- Características demográficas (Gênero, Idade)
- Medidas físicas (Altura, Peso)
- Histórico familiar
- Hábitos alimentares
- Atividade física
- Uso de tecnologia
- Nível de obesidade (variável alvo)

## 🏗️ Estrutura do Projeto

```
tech_challenge/
├── data/               # Dados (SQLite e CSV)
├── src/                # Código fonte (pipeline ML, feature engineering)
├── notebooks/          # Análise exploratória e experimentação
├── app/                # Aplicação Streamlit (sistema preditivo)
├── dashboard/          # Dashboard analítico
├── models/             # Modelos treinados salvos
└── requirements.txt    # Dependências do projeto
```

## 🚀 Como Usar

### Instalação

```bash
pip install -r requirements.txt
```

### Preparação dos Dados

1. Extrair dados do SQLite (se necessário):
```bash
python src/extract_data.py
```

2. Treinar o modelo:
```bash
python src/train_model.py
```

### Executar Aplicação Streamlit

**Opção 1:** Usando script auxiliar
```bash
python run_app.py
```

**Opção 2:** Diretamente
```bash
streamlit run app/app.py
```

### Executar Dashboard Analítico

**Opção 1:** Usando script auxiliar
```bash
python run_dashboard.py
```

**Opção 2:** Diretamente
```bash
streamlit run dashboard/dashboard.py
```

## 📊 Resultados do Modelo

- **Algoritmo:** Random Forest
- **Acurácia:** 98.58%
- **F1-Score:** 98.58%
- **Precision:** 98.59%
- **Recall:** 98.58%
- **Status:** ✅ Requisito atendido (acima de 75%)

## 📝 Requisitos Entregues

- ✅ Pipeline completo de Machine Learning
- ✅ Feature Engineering
- ✅ Modelo com assertividade > 75%
- ✅ Deploy no Streamlit (aplicação preditiva)
- ✅ Dashboard analítico com insights
- ✅ Código no GitHub

## 👥 Autores

[Seu nome/equipe]

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais.

