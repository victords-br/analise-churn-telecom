<div align="center">

# 📊 Análise de Churn - Telecom

### Identificação de padrões de cancelamento e recomendações para redução de churn

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org/)
[![Metabase](https://img.shields.io/badge/Metabase-509EE3?style=for-the-badge&logo=metabase&logoColor=white)](https://www.metabase.com/)
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

</div>

---

## 📌 Sobre o Projeto

Este projeto foi desenvolvido como parte do meu portfólio de análise de dados. O objetivo é **identificar padrões de cancelamento** (churn) em uma empresa de telecomunicações e **fornecer recomendações acionáveis** para redução da taxa de evasão de clientes.

### 🎯 Problema de Negócio

A empresa estava perdendo clientes sem entender:
- **Quem** está cancelando?
- **Por que** cancelam?
- **Quando** cancelam?
- **O que fazer** para reverter?

### 💡 Solução Proposta

Análise completa dos dados com:
- Limpeza e tratamento usando Python/Pandas
- Criação de novas variáveis (feature engineering)
- Dashboard interativo no Metabase
- Insights acionáveis e recomendações estratégicas

---

## 📁 Fonte dos Dados

| Propriedade | Detalhe |
|-------------|---------|
| **Dataset** | Telco Customer Churn |
| **Fonte** | Kaggle |
| **Link** | [Clique aqui](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) |
| **Registros** | 7.043 clientes |
| **Colunas** | 21 variáveis |
| **Período** | Dados anuais anonimizados |
| **Licença** | Uso educacional |

---

## 🛠️ Tecnologias Utilizadas

### 📓 Análise e Tratamento

| Ferramenta | Finalidade |
|------------|------------|
| **Python 3.12** | Linguagem principal |
| **Pandas** | Manipulação e limpeza de dados |
| **NumPy** | Operações matemáticas |
| **Matplotlib** | Visualizações iniciais |
| **Jupyter Notebook** | Ambiente de desenvolvimento |

### 🗄️ Banco de Dados

| Ferramenta | Finalidade |
|------------|------------|
| **Supabase** | Banco de dados na nuvem (PostgreSQL) |
| **SQL** | Queries para análise |

### 📊 Dashboard

| Ferramenta | Finalidade |
|------------|------------|
| **Metabase** | Criação de dashboard interativo |
| **Public Link** | Compartilhamento do dashboard |

---

## 📈 Principais Resultados

### Métricas Gerais

<div align="center">

| Métrica | Valor |
|:--------|------:|
| **📊 Taxa de Churn Geral** | **26,6%** |
| 👥 Clientes ativos | 5.163 (73,4%) |
| ❌ Clientes cancelados | 1.869 (26,6%) |
| 📉 Perda mensal média | 156 clientes |
| 📆 Churn mensal equivalente | 2,2% |

</div>

### 🔍 Insights-Chave

<div align="center">

| # | Insight | Dado que comprova |
|---|---------|-------------------|
| 1️⃣ | **Contrato mensal é o maior problema** | 88,6% dos cancelamentos |
| 2️⃣ | **Primeiros 6 meses são críticos** | Churn de 45% neste período |
| 3️⃣ | **Pagamento por boleto tem maior risco** | Taxa 2x > que débito automático |
| 4️⃣ | **Perfil de maior risco** | Mensal + Boleto + 0-6 meses = 68% |

</div>

---

## 📊 Dashboard Interativo

<div align="center">

### 🔗 Acesse o Dashboard

> ⚠️ **Nota:** O dashboard está rodando localmente no Metabase (porta 3000). Para acessá-lo, o Metabase precisa estar em execução no seu computador.

**Link local:** `http://localhost:3000/public/dashboard/7cc54f1b-bd5c-4817-8dfd-c7f9a8c5d409`

</div>

### Componentes do Dashboard

| Card | Tipo de Visualização | Finalidade |
|------|---------------------|------------|
| 01 | Número grande (KPI) | Taxa de Churn: 26,6% |
| 02 | Gráfico de barras | Churn por tipo de contrato |
| 03 | Gráfico de barras | Churn por forma de pagamento |
| 04 | Gráfico de barras | Churn por tempo de uso |
| 05 | Tabela ordenada | Perfil de risco (top 10) |
| 06 | Texto formatado | Insights e recomendações |

---

## 💡 Recomendações de Negócio

<div align="center">

| Prioridade | Ação | Impacto Esperado |
|:----------:|------|------------------|
| 🔴 **Alta** | Criar onboarding reforçado nos primeiros 6 meses | Reduzir churn inicial |
| 🔴 **Alta** | Oferecer desconto para migrar de mensal para anual | Fidelizar clientes |
| 🟡 **Média** | Incentivar débito automático (cashback/desconto) | Reduzir churn em 50% neste segmento |
| 🟡 **Média** | Identificar e agir preventivamente sobre perfis de risco | Aumentar retenção |

</div>

### 📌 Próximos Passos Sugeridos

- [ ] Analisar churn por canal de aquisição
- [ ] Criar alertas automáticos para clientes com perfil de risco
- [ ] Testar campanhas de retenção no 3º mês de contrato
- [ ] Implementar NPS para identificar insatisfação precoce

---

## 📁 Estrutura do Projeto
📦 analise-churn-telecom/
│
├── 📁 dashboard/
│ ├── 📄 dashboard_churn.pdf # PDF do dashboard interativo
│ └── 📄 analise_churn_notebook.pdf # PDF da análise técnica (opcional)
│
├── 📁 dados/
│ ├── 📁 raw/
│ │ └── 📄 WA_Fn-UseC_-Telco-Customer-Churn.csv
│ └── 📁 processed/
│ └── 📄 telco_churn_cleaned.csv
│
├── 📁 notbooks/
│ └── 📓 01_limpeza_tratamento.ipynb # Notebook original (recomendado)
│
├── 📁 image/
│ └── 🖼️ dashboard_preview.png
│
├── 📄 README.md
└── 📄 requirements.txt

---

## 📎 Links e Downloads

### 📓 Análise Técnica (Notebook)

| Formato | Ação | Vantagem |
|---------|------|----------|
| **📓 Notebook (.ipynb)** | [🔍 Visualizar no GitHub](https://github.com/VictorDevAgencia74/analise-churn-telecom/blob/main/notbooks/01_limpeza_tratamento.ipynb) | Código executável, melhor para recrutadores |
| **📄 PDF do Notebook** | [⬇️ Baixar PDF](https://raw.githubusercontent.com/VictorDevAgencia74/analise-churn-telecom/main/dashboard/analise_churn_notebook.pdf) | Para leitura rápida, sem código |

### 📊 Dashboard

| Formato | Ação |
|---------|------|
| **📄 PDF do Dashboard** | [🔍 Visualizar](https://github.com/VictorDevAgencia74/analise-churn-telecom/blob/main/dashboard/dashboard_churn.pdf) / [⬇️ Baixar](https://raw.githubusercontent.com/VictorDevAgencia74/analise-churn-telecom/main/dashboard/dashboard_churn.pdf) |

### 🚀 Dashboard Interativo (Metabase)

> ⚠️ Rodando localmente. Para acessar, o Metabase precisa estar em execução.

**Link local:** `http://localhost:3000/public/dashboard/7cc54f1b-bd5c-4817-8dfd-c7f9a8c5d409`

### 📁 Dados e Código

| Recurso | Link |
|---------|------|
| 📦 **Dataset original** | [Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) |
| 📄 **Dataset tratado (CSV)** | `./dados/processed/telco_churn_cleaned.csv` |

---

## 👤 Autor

<div align="center">

**Victor Xavier**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/seu-perfil)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/VictorDevAgencia74)
[![Portfólio](https://img.shields.io/badge/Portfólio-FF5722?style=for-the-badge&logo=google-chrome&logoColor=white)](https://seu-site.com)

</div>

---

## 📄 Licença

Este projeto é de **uso educacional** e para **fins de portfólio**. O dataset utilizado é público e disponível no Kaggle.

---

<div align="center">

### ⭐ Gostou do projeto? Deixe uma estrela no GitHub! ⭐

</div>
