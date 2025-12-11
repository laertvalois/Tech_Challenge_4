# Tech Challenge - Sistema Preditivo de Obesidade

## 📋 Sobre o Projeto

Este projeto foi desenvolvido como parte do Tech Challenge, com o objetivo de criar um sistema de Machine Learning para auxiliar médicos e médicas a prever se uma pessoa pode ter obesidade.

## 🎯 Objetivos

- Desenvolver um modelo preditivo com assertividade acima de 75%
- Criar uma aplicação Streamlit para predição em tempo real
- Construir um dashboard analítico com insights sobre obesidade
- Fornecer ferramentas para auxiliar a tomada de decisão da equipe médica

## 📊 Dados

O arquivo CSV (`data/obesity.csv`) contém informações sobre:
- Características demográficas (Gênero, Idade)
- Medidas físicas (Altura, Peso)
- Histórico familiar
- Hábitos alimentares
- Atividade física
- Uso de tecnologia
- Nível de obesidade (variável alvo)

**Total de registros:** 2.111  
**Variáveis de entrada:** 16  
**Variável alvo:** Obesity (7 classes)

## 🏗️ Estrutura do Projeto

```
tech_challenge/
├── data/               # Dados
│   └── obesity.csv     # Dataset principal
├── src/                # Código fonte (pipeline ML, feature engineering)
│   ├── data_preprocessing.py
│   ├── train_model.py
│   └── load_model.py
├── notebooks/          # Análise exploratória
│   └── 01_analise_exploratoria.py
├── app/                # Aplicação Streamlit (unificada: predição + dashboard)
│   └── app.py          # Aplicação principal com 3 páginas
├── models/             # Modelos treinados salvos
│   ├── obesity_model.joblib
│   └── preprocessor.joblib
└── requirements.txt    # Dependências do projeto
```

## 🚀 Como Usar

### Instalação

```bash
pip install -r requirements.txt
```

### Preparação dos Dados

1. Os dados já estão disponíveis em `data/obesity.csv`

2. Treinar o modelo:
```bash
python src/train_model.py
```

**Nota:** O modelo já está treinado e salvo em `models/`. Você pode usar diretamente a aplicação sem retreinar.

### Executar Aplicação Streamlit

**Opção 1:** Usando script auxiliar
```bash
python run_app.py
```

**Opção 2:** Diretamente
```bash
streamlit run app/app.py
```

**Nota:** O dashboard analítico está integrado na aplicação principal. Acesse a página "Insights e Métricas" no menu lateral.

## 📊 Resultados do Modelo

- **Algoritmo:** Random Forest
- **Acurácia:** 98.58%
- **F1-Score:** 98.58%
- **Precision:** 98.59%
- **Recall:** 98.58%
- **Status:** ✅ Requisito atendido (acima de 75%)

**Observação:** O modelo foi treinado com validação cruzada e está pronto para uso em produção.

## 📝 Requisitos Entregues

- ✅ Pipeline completo de Machine Learning com feature engineering
- ✅ Modelo com assertividade > 75% (98.58%)
- ✅ Deploy no Streamlit (aplicação preditiva unificada)
- ✅ Dashboard analítico com insights integrado na aplicação
- ✅ Código no GitHub
- ✅ Documentação completa

## 📋 Estrutura da Aplicação Streamlit

A aplicação (`app/app.py`) possui três páginas principais:

1. **Início:** Apresentação do sistema, objetivos e informações técnicas
2. **Predição de Obesidade:** Formulário completo para entrada de dados e predição em tempo real
3. **Insights e Métricas:** Dashboard analítico com:
   - Análise de correlação (heatmap)
   - Boxplots por nível de obesidade
   - Análise de distribuição
   - Filtros interativos
   - Métricas e estatísticas descritivas

## 🎯 Funcionalidades Principais

### Sistema Preditivo
- Formulário completo com todas as 16 variáveis
- Predição em tempo real
- Exibição de probabilidades por classe
- Exportação de relatório em PDF
- Campos opcionais para profissional e paciente

### Dashboard Analítico
- Visualizações interativas (Plotly)
- Filtros por gênero, nível de obesidade e faixa etária
- Análises estatísticas detalhadas
- Insights para equipe médica
- Download de dados filtrados

## 📚 Documentação Adicional

- `ANALISE_REQUISITOS.md` - Análise detalhada dos requisitos
- `RESUMO_PROJETO.md` - Resumo executivo do projeto
- `ENTREGA_TECH_CHALLENGE.md` - Documento de entrega detalhado
- `DOCUMENTO_ENTREGA_FINAL.md` - Documento consolidado de entrega
- `LINKS_ENTREGA.txt` - Template para links de entrega

## 👥 Autores

Este projeto foi desenvolvido como parte do Tech Challenge - FIAP pelos alunos:

**Alysson Tenório**
- alyssontr@bnb.gov.br

**Erico Leopoldino Mota**
- erico_mota@hotmail.com

**Henrique Bruno Oliveira Lima**
- henriquebol@bnb.gov.br

**Joao Paulo Pinheiro Aguiar**
- joaopaulop.aguiar@gmail.com

**Laert Valois Rios Carneiro**
- laertvalois@bnb.gov.br

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais.

