# 📋 Documento de Entrega - Tech Challenge
## Sistema Preditivo de Obesidade

---

## ✅ Checklist de Requisitos

### 1. Pipeline de Machine Learning ✅
- **Localização:** `src/`
- **Arquivos principais:**
  - `data_preprocessing.py` - Pré-processamento e feature engineering
  - `train_model.py` - Treinamento de múltiplos modelos com validação cruzada
  - `load_model.py` - Utilitário para carregar modelos salvos
- **Feature Engineering implementado:**
  - Criação de IMC (Índice de Massa Corporal)
  - Encoding de variáveis categóricas (LabelEncoder)
  - Normalização de features numéricas (StandardScaler)
  - Tratamento de valores faltantes
  - Seleção e preparação de features

### 2. Modelo com Assertividade > 75% ✅
- **Modelo selecionado:** Random Forest
- **Métricas de desempenho:**
  - **Acurácia:** 98.58% ✅ (muito acima do requisito de 75%)
  - **F1-Score:** 98.58%
  - **Precision:** 98.59%
  - **Recall:** 98.58%
- **Validação:** Validação cruzada implementada
- **Modelo salvo em:** `models/obesity_model.joblib`
- **Pré-processador salvo em:** `models/preprocessor.joblib`

### 3. Deploy no Streamlit (Aplicação Preditiva) ✅
- **Localização:** `app/app.py`
- **Funcionalidades implementadas:**
  - ✅ Formulário completo com todas as 16 variáveis do dicionário
  - ✅ Predição em tempo real
  - ✅ Exibição de probabilidades por classe
  - ✅ Recomendações baseadas no resultado
  - ✅ Exportação de relatório em PDF
  - ✅ Campos opcionais para profissional e paciente
  - ✅ Interface amigável e profissional
  - ✅ Navegação por menu lateral com 3 páginas
- **Como executar:**
  ```bash
  streamlit run app/app.py
  # ou
  python run_app.py
  ```

### 4. Dashboard Analítico com Insights ✅
- **Localização:** Integrado em `app/app.py` (página "Insights e Métricas")
- **Visualizações implementadas:**
  - ✅ Distribuição de níveis de obesidade (gráfico de barras e pizza)
  - ✅ Análise por gênero (tabelas e gráficos)
  - ✅ Análise por faixa etária
  - ✅ Scatter plot: Idade vs IMC
  - ✅ Impacto de atividade física
  - ✅ Impacto de histórico familiar
  - ✅ Impacto de hábitos alimentares
  - ✅ Consumo médio de vegetais por nível de obesidade
  - ✅ Análise de correlação (heatmap)
  - ✅ Boxplots por nível de obesidade (variáveis selecionáveis)
  - ✅ Análise de distribuição (histogramas e estatísticas descritivas)
- **Funcionalidades:**
  - ✅ Filtros interativos (Gênero, Nível de Obesidade, Faixa Etária)
  - ✅ Métricas principais (Total de registros, IMC médio, Taxa de sobrepeso/obesidade)
  - ✅ Insights e recomendações para equipe médica
  - ✅ Download de dados filtrados (CSV)
  - ✅ Estatísticas descritivas detalhadas

### 5. Links e Documentação ✅
- **Repositório GitHub:** https://github.com/laertvalois/Tech_Challenge_4
- **Arquivo de links:** `LINKS_ENTREGA.txt` (preencher com links do deploy)
- **Documentação completa:**
  - `README.md` - Documentação principal
  - `ANALISE_REQUISITOS.md` - Análise detalhada dos requisitos
  - `RESUMO_PROJETO.md` - Resumo executivo
  - `ENTREGA_TECH_CHALLENGE.md` - Este documento

### 6. Vídeo de Apresentação 📹
- **Duração sugerida:** 4-10 minutos
- **Conteúdo recomendado:**
  1. Introdução (1min): Problema e objetivo
  2. Estratégia (2-3min): Abordagem e metodologia
  3. Sistema Preditivo (2-3min): Demo do app Streamlit
  4. Dashboard (2-3min): Insights e análises
  5. Conclusão (1min): Resultados e próximos passos
- **Foco:** Visão de negócio (como o sistema ajuda médicos)

---

## 📊 Dados do Projeto

- **Fonte:** `data/obesity.csv`
- **Total de registros:** 2.111
- **Variáveis de entrada:** 16
- **Variável alvo:** Obesity (7 classes)
  - Insufficient_Weight (Peso Insuficiente)
  - Normal_Weight (Peso Normal)
  - Overweight_Level_I (Sobrepeso Nível I)
  - Overweight_Level_II (Sobrepeso Nível II)
  - Obesity_Type_I (Obesidade Tipo I)
  - Obesity_Type_II (Obesidade Tipo II)
  - Obesity_Type_III (Obesidade Tipo III)
- **Divisão treino/teste:** 80/20 (1.688/423)

---

## 🏗️ Estrutura do Projeto

```
tech_challenge/
├── data/                    # Dados
│   └── obesity.csv          # Dataset principal
├── src/                     # Código fonte (Pipeline ML)
│   ├── data_preprocessing.py # Pré-processamento e feature engineering
│   ├── train_model.py       # Treinamento de modelos
│   ├── load_model.py        # Carregamento de modelos
│   └── extract_data.py      # Utilitário de extração (se necessário)
├── notebooks/               # Análise exploratória
│   └── 01_analise_exploratoria.py
├── app/                     # Aplicação Streamlit (unificada)
│   └── app.py              # App principal (predição + dashboard)
├── models/                  # Modelos treinados
│   ├── obesity_model.joblib
│   └── preprocessor.joblib
├── requirements.txt         # Dependências
├── README.md               # Documentação principal
├── ANALISE_REQUISITOS.md   # Análise detalhada
├── RESUMO_PROJETO.md       # Resumo executivo
├── ENTREGA_TECH_CHALLENGE.md # Este documento
├── LINKS_ENTREGA.txt       # Links de entrega
├── run_app.py              # Script auxiliar para executar app
└── run_dashboard.py         # Script auxiliar (legado)
```

---

## 🔧 Tecnologias Utilizadas

### Machine Learning
- **scikit-learn** - Pipeline ML, modelos e métricas
- **Random Forest** - Modelo final selecionado
- **joblib** - Persistência de modelos

### Visualização e Análise
- **pandas** - Manipulação de dados
- **numpy** - Operações numéricas
- **plotly** - Visualizações interativas
- **matplotlib** - Gráficos estáticos (se necessário)
- **seaborn** - Visualizações estatísticas (se necessário)

### Deploy e Interface
- **streamlit** - Framework web para aplicação
- **streamlit-option-menu** - Menu lateral
- **reportlab** - Geração de PDFs

---

## 🚀 Como Executar

### Instalação
```bash
pip install -r requirements.txt
```

### Treinar Modelo (opcional - já treinado)
```bash
python src/train_model.py
```

### Executar Aplicação
```bash
# Opção 1: Script auxiliar
python run_app.py

# Opção 2: Diretamente
streamlit run app/app.py
```

A aplicação abrirá automaticamente no navegador em `http://localhost:8501`

---

## 📈 Métricas e Resultados

### Desempenho do Modelo
- **Acurácia:** 98.58% ✅
- **F1-Score:** 98.58%
- **Precision:** 98.59%
- **Recall:** 98.58%

### Validação
- Validação cruzada implementada
- Divisão treino/teste: 80/20
- Estratificação por classe mantida

---

## 🎯 Funcionalidades da Aplicação

### Página: Início
- Apresentação do sistema
- Objetivos e como usar
- Informações técnicas (acurácia, total de registros, variáveis)

### Página: Predição de Obesidade
- Formulário completo com 16 variáveis:
  - Dados demográficos (Gênero, Idade)
  - Medidas (Altura, Peso, IMC calculado)
  - Histórico familiar
  - Hábitos alimentares (FAVC, FCVC, NCP, CAEC)
  - Hidratação (CH2O, SCC)
  - Estilo de vida (SMOKE, FAF, TUE)
  - Outros (CALC, MTRANS)
- Campos opcionais: Nome do Profissional, Registro do Conselho, Nome do Paciente
- Predição em tempo real
- Exibição de:
  - Nível de obesidade previsto
  - Confiança da predição
  - Probabilidades por classe (gráfico e tabela)
  - Recomendações personalizadas
- Exportação de relatório em PDF

### Página: Insights e Métricas
- **Métricas principais:**
  - Total de registros
  - IMC médio
  - Idade média
  - Taxa de sobrepeso/obesidade
- **Filtros interativos:**
  - Gênero
  - Nível de Obesidade
  - Faixa Etária
- **Visualizações:**
  - Distribuição de níveis de obesidade
  - Análise por gênero
  - Análise por faixa etária
  - Scatter plot: Idade vs IMC
  - Impacto de atividade física
  - Impacto de histórico familiar
  - Impacto de hábitos alimentares
  - Consumo médio de vegetais
- **Análises avançadas:**
  - Análise de correlação (heatmap)
  - Boxplots por nível de obesidade
  - Análise de distribuição (histogramas e estatísticas)
- **Insights e recomendações:**
  - Análise de gênero mais afetado
  - Impacto de atividade física
  - Recomendações para equipe médica
- **Download de dados filtrados (CSV)**

---

## 📝 Dicionário de Dados

### Variáveis de Entrada (16)
1. **Gender** - Gênero (Female, Male)
2. **Age** - Idade em anos (14-61)
3. **Height** - Altura em metros
4. **Weight** - Peso em kg
5. **family_history** - Histórico familiar de excesso de peso (yes, no)
6. **FAVC** - Consumo frequente de alimentos altamente calóricos (yes, no)
7. **FCVC** - Frequência de consumo de vegetais (1-3: 1=raramente, 2=às vezes, 3=sempre)
8. **NCP** - Número de refeições principais (1-4)
9. **CAEC** - Consumo entre refeições (no, Sometimes, Frequently, Always)
10. **SMOKE** - Hábito de fumar (yes, no)
11. **CH2O** - Consumo diário de água (1-3: 1=<1L/dia, 2=1-2L/dia, 3=>2L/dia)
12. **SCC** - Monitora ingestão calórica diária (yes, no)
13. **FAF** - Frequência semanal de atividade física (0-3: 0=nenhuma, 1=1-2×/sem, 2=3-4×/sem, 3=5×/sem ou mais)
14. **TUE** - Tempo diário usando dispositivos eletrônicos (0-2: 0=0-2h/dia, 1=3-5h/dia, 2=>5h/dia)
15. **CALC** - Frequência de consumo de álcool (no, Sometimes, Frequently, Always)
16. **MTRANS** - Meio de transporte (Public_Transportation, Automobile, Walking, Motorbike, Bike)

### Variável Alvo
- **Obesity** - Nível de obesidade (7 classes)

---

## ✅ Checklist Final de Entrega

- [x] Pipeline completo de Machine Learning
- [x] Feature Engineering implementado
- [x] Modelo treinado e salvo
- [x] Modelo com assertividade > 75% (98.58%)
- [x] Aplicação Streamlit funcional
- [x] Dashboard analítico integrado
- [x] Código no GitHub
- [x] Documentação completa
- [ ] Deploy no Streamlit Cloud (preencher link em LINKS_ENTREGA.txt)
- [ ] Vídeo de apresentação gravado (preencher link em LINKS_ENTREGA.txt)

---

## 📞 Informações de Contato

**Repositório GitHub:** https://github.com/laertvalois/Tech_Challenge_4

**Projeto desenvolvido para:** Tech Challenge - FIAP  
**Finalidade:** Educacional

---

**Status do Projeto:** ✅ COMPLETO E PRONTO PARA ENTREGA
