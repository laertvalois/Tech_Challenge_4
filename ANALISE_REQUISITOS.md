# 📊 Análise dos Requisitos - Tech Challenge

## 🎯 Objetivo Principal
Desenvolver um sistema de Machine Learning para prever obesidade e auxiliar médicos na tomada de decisão.

## ✅ Requisitos Obrigatórios

### 1. Pipeline de Machine Learning
**O que precisa:**
- Feature Engineering completo
- Pré-processamento de dados
- Treinamento do modelo
- Validação e avaliação

**Tecnologias sugeridas:**
- `pandas` para manipulação de dados
- `scikit-learn` para pipeline e modelos
- `imbalanced-learn` (se houver desbalanceamento)

**Estrutura sugerida:**
```
src/
├── data_preprocessing.py    # Limpeza e transformação
├── feature_engineering.py   # Criação de features
├── train_model.py           # Treinamento
└── evaluate_model.py        # Avaliação
```

### 2. Modelo com Assertividade > 75%
**O que precisa:**
- Acurácia ou F1-Score acima de 75%
- Validação cruzada
- Métricas de avaliação (precision, recall, F1, confusion matrix)

**Modelos a testar:**
- Random Forest
- XGBoost
- Logistic Regression
- SVM
- Ensemble methods

### 3. Deploy no Streamlit (Aplicação Preditiva)
**O que precisa:**
- Interface web interativa
- Formulário para entrada de dados
- Exibição da predição
- Visualização dos resultados

**Estrutura implementada:**
```
app/
└── app.py                  # Aplicação principal unificada
    - Menu lateral com 3 páginas:
      * Início
      * Predição de Obesidade
      * Insights e Métricas (Dashboard)
```

**Funcionalidades:**
- Input de todas as variáveis do dicionário de dados
- Botão de predição
- Exibição do nível de obesidade previsto
- Probabilidades por classe
- Explicação do resultado

### 4. Dashboard Analítico
**O que precisa:**
- Visualizações interativas
- Insights sobre obesidade
- Estatísticas descritivas
- Análise de correlações
- Distribuições das variáveis

**Estrutura implementada:**
```
app/
└── app.py                  # Dashboard integrado na página "Insights e Métricas"
    - Filtros interativos
    - Visualizações Plotly
    - Análises estatísticas
    - Download de dados
```

**Visualizações sugeridas:**
- Distribuição de obesidade por gênero
- Relação entre idade e obesidade
- Impacto de atividade física
- Hábitos alimentares vs obesidade
- Heatmap de correlações
- Distribuições de IMC

### 5. Links e Documentação
**O que precisa:**
- Link do app Streamlit Cloud
- Link do dashboard
- Link do repositório GitHub
- Arquivo .doc ou .txt com todos os links

**Estrutura do arquivo de links:**
```
LINKS_ENTREGA.txt ou LINKS_ENTREGA.doc
```

### 6. Vídeo de Apresentação (4-10 min)
**O que precisa:**
- Apresentação da estratégia
- Demonstração do sistema preditivo
- Apresentação do dashboard
- Visão de negócio (não apenas técnica)

## 📋 Dicionário de Dados

### Variáveis de Entrada:
1. **Gender** - Gênero (categórica)
2. **Age** - Idade (numérica)
3. **Height** - Altura em metros (numérica)
4. **Weight** - Peso em kgs (numérica)
5. **family_history** - Histórico familiar (categórica)
6. **FAVC** - Alimentos altamente calóricos (categórica)
7. **FCVC** - Consumo de vegetais (numérica/ordinal)
8. **NCP** - Número de refeições principais (numérica)
9. **CAEC** - Comer entre refeições (categórica)
10. **SMOKE** - Fumar (categórica)
11. **CH2O** - Consumo de água (numérica/ordinal)
12. **SCC** - Monitorar calorias (categórica)
13. **FAF** - Frequência de atividade física (numérica/ordinal)
14. **TUE** - Tempo usando dispositivos eletrônicos (numérica/ordinal: 0=0-2h/dia, 1=3-5h/dia, 2=>5h/dia)
15. **CALC** - Frequência de consumo de álcool (categórica: no, Sometimes, Frequently, Always)
16. **MTRANS** - Meio de transporte (categórica: Public_Transportation, Automobile, Walking, Motorbike, Bike)

### Variável Alvo:
- **Obesity** - Nível de obesidade (categórica - multiclasse: 7 classes)

## 🔄 Fluxo de Trabalho Sugerido

### Fase 1: Análise Exploratória
1. Extrair dados do SQLite
2. Análise exploratória (EDA)
3. Identificar missing values
4. Análise de distribuições
5. Análise de correlações

### Fase 2: Feature Engineering
1. Tratamento de valores faltantes
2. Encoding de variáveis categóricas
3. Normalização/Padronização
4. Criação de features derivadas (ex: IMC)
5. Seleção de features

### Fase 3: Modelagem
1. Divisão train/test
2. Testar múltiplos algoritmos
3. Tuning de hiperparâmetros
4. Validação cruzada
5. Seleção do melhor modelo
6. Salvar modelo treinado

### Fase 4: Desenvolvimento da Aplicação
1. Criar app Streamlit para predição
2. Integrar modelo salvo
3. Criar interface amigável
4. Adicionar validações de input

### Fase 5: Dashboard Analítico
1. Criar visualizações interativas
2. Adicionar filtros
3. Criar insights relevantes
4. Design profissional

### Fase 6: Deploy e Documentação
1. Deploy no Streamlit Cloud
2. Criar repositório GitHub
3. Documentar código
4. Criar arquivo com links
5. Gravar vídeo de apresentação

## 🛠️ Tecnologias e Bibliotecas

### Core ML:
- pandas, numpy
- scikit-learn
- imbalanced-learn

### Visualização:
- matplotlib
- seaborn
- plotly

### Deploy:
- streamlit
- streamlit-option-menu
- streamlit-aggrid

### Utilitários:
- joblib (salvar modelos)
- sqlite3 (banco de dados)

## 📈 Métricas de Sucesso

1. ✅ Acurácia > 75%
2. ✅ Pipeline completo e documentado
3. ✅ App Streamlit funcional e intuitivo
4. ✅ Dashboard com insights relevantes
5. ✅ Código limpo e organizado
6. ✅ Documentação completa
7. ✅ Vídeo de apresentação profissional

## 🎬 Dicas para o Vídeo

1. **Introdução (1min):** Problema e objetivo
2. **Estratégia (2-3min):** Abordagem e metodologia
3. **Sistema Preditivo (2-3min):** Demo do app Streamlit
4. **Dashboard (2-3min):** Insights e análises
5. **Conclusão (1min):** Resultados e próximos passos

**Foco em negócio:**
- Como o sistema ajuda médicos?
- Quais insights são mais relevantes?
- Impacto na tomada de decisão
- Valor agregado para o hospital

