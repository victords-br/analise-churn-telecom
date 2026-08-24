# app.py
# Coloque este arquivo na raiz do projeto: /Projects/Data-Science/analyse-churn-telecom/
# Execute com: streamlit run app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Churn - Telecom",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS customizado
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 0.5rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
    }
    .insight-box {
        background-color: #e8f4f8;
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }
    .risk-high {
        background-color: #ffebee;
        border-left: 4px solid #e53935;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }
    .risk-medium {
        background-color: #fff3e0;
        border-left: 4px solid #fb8c00;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }
    .risk-low {
        background-color: #e8f5e9;
        border-left: 4px solid #43a047;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# ============ FUNÇÕES DE CARREGAMENTO ============

@st.cache_data
def load_data():
    """Carrega e prepara os dados"""
    # Caminho correto para o arquivo CSV na pasta dados/
    file_path = os.path.join('dados/processed', 'telco_churn_cleaned.csv')
    
    if not os.path.exists(file_path):
        st.error(f"Arquivo não encontrado: {file_path}")
        st.info("Verifique se o arquivo telco_churn_cleaned.csv está na pasta 'dados/'")
        return None
    
    df = pd.read_csv(file_path)
    
    # Converter colunas para tipos corretos
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    
    # Criar colunas adicionais se não existirem
    if 'Churn_Num' not in df.columns:
        df['Churn_Num'] = df['Churn'].map({'Yes': 1, 'No': 0})
    
    if 'TenureGroup' not in df.columns:
        bins = [0, 6, 12, 24, 72]
        labels = ['0-6 meses', '7-12 meses', '13-24 meses', '25+ meses']
        df['TenureGroup'] = pd.cut(df['tenure'], bins=bins, labels=labels, right=False)
    
    if 'MonthlyGroup' not in df.columns:
        bins_mensalidade = [0, 30, 50, 80, 120]
        labels_mensalidade = ['Baixo (<30)', 'Médio (30-50)', 'Alto (50-80)', 'Premium (>80)']
        df['MonthlyGroup'] = pd.cut(df['MonthlyCharges'], bins=bins_mensalidade, labels=labels_mensalidade)
    
    return df

# ============ FUNÇÕES DE ANÁLISE ============

def calculate_metrics(df):
    """Calcula métricas principais"""
    total = len(df)
    churned = df[df['Churn'] == 'Yes'].shape[0]
    churn_rate = churned / total if total > 0 else 0
    
    # Receita média por cliente
    avg_monthly = df['MonthlyCharges'].mean()
    avg_total = df['TotalCharges'].mean()
    
    # Receita perdida
    lost_revenue = df[df['Churn'] == 'Yes']['MonthlyCharges'].sum()
    
    # Tempo médio de cliente
    avg_tenure = df['tenure'].mean()
    
    return {
        'total': total,
        'churned': churned,
        'churn_rate': churn_rate,
        'avg_monthly': avg_monthly,
        'avg_total': avg_total,
        'lost_revenue': lost_revenue,
        'avg_tenure': avg_tenure
    }

def create_churn_by_category(df, category):
    """Cria dataframe de churn por categoria"""
    result = df.groupby(category).agg({
        'Churn_Num': ['mean', 'count'],
        'customerID': 'count'
    }).reset_index()
    result.columns = [category, 'churn_rate', 'count', 'total']
    result['churn_rate'] = result['churn_rate'].round(4)
    result['churn_percent'] = (result['churn_rate'] * 100).round(1)
    result['percentage_of_total'] = (result['count'] / result['count'].sum() * 100).round(1)
    return result.sort_values('churn_rate', ascending=False)

# ============ CARREGAR DADOS ============

df = load_data()

if df is None:
    st.stop()

metrics = calculate_metrics(df)

# ============ SIDEBAR ============

with st.sidebar:
    st.image("https://img.icons8.com/color/96/000001/data-configuration.png", width=80)
    
    st.title("🎯 Filtros")
    st.markdown("---")
    
    # Filtros
    contract_types = ['Todos'] + sorted(df['Contract'].unique().tolist())
    selected_contract = st.selectbox("📋 Tipo de Contrato", contract_types)
    
    internet_types = ['Todos'] + sorted(df['InternetService'].unique().tolist())
    selected_internet = st.selectbox("🌐 Tipo de Internet", internet_types)
    
    payment_methods = ['Todos'] + sorted(df['PaymentMethod'].unique().tolist())
    selected_payment = st.selectbox("💳 Forma de Pagamento", payment_methods)
    
    # Slider para tenure
    min_tenure = int(df['tenure'].min())
    max_tenure = int(df['tenure'].max())
    tenure_range = st.slider(
        "⏱️ Tempo de Cliente (meses)",
        min_value=min_tenure,
        max_value=max_tenure,
        value=(min_tenure, max_tenure)
    )
    
    st.markdown("---")
    
    # Aplicar filtros
    filtered_df = df.copy()
    
    if selected_contract != 'Todos':
        filtered_df = filtered_df[filtered_df['Contract'] == selected_contract]
    
    if selected_internet != 'Todos':
        filtered_df = filtered_df[filtered_df['InternetService'] == selected_internet]
    
    if selected_payment != 'Todos':
        filtered_df = filtered_df[filtered_df['PaymentMethod'] == selected_payment]
    
    filtered_df = filtered_df[
        (filtered_df['tenure'] >= tenure_range[0]) & 
        (filtered_df['tenure'] <= tenure_range[1])
    ]
    
    filtered_metrics = calculate_metrics(filtered_df)
    
    st.markdown("### 📊 Resumo")
    st.metric("Total de Clientes", f"{filtered_metrics['total']:,}")
    st.metric("Clientes com Churn", f"{filtered_metrics['churned']:,}")
    st.metric("Taxa de Churn", f"{filtered_metrics['churn_rate']:.1%}")

# ============ HEADER PRINCIPAL ============

st.markdown('<div class="main-header">📊 Análise de Churn - Telecom</div>', unsafe_allow_html=True)

# ============ MÉTRICAS PRINCIPAIS ============

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{filtered_metrics['churn_rate']:.1%}</div>
            <div class="metric-label">📉 Taxa de Churn</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{filtered_metrics['churned']:,}</div>
            <div class="metric-label">🚪 Clientes Perdidos</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${filtered_metrics['avg_monthly']:.0f}</div>
            <div class="metric-label">💰 Mensalidade Média</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${filtered_metrics['lost_revenue']:,.0f}</div>
            <div class="metric-label">💸 Receita Mês Perdida</div>
        </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{filtered_metrics['avg_tenure']:.1f} meses</div>
            <div class="metric-label">⏱️ Tempo Cliente</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============ ALERTA DE ALTO RISCO ============

high_risk_pct = filtered_df[filtered_df['tenure'] <= 6]['Churn_Num'].mean() if len(filtered_df[filtered_df['tenure'] <= 6]) > 0 else 0

if high_risk_pct > 0.4:
    st.warning(f"⚠️ **Alerta:** {high_risk_pct:.1%} dos clientes com menos de 6 meses estão cancelando! Considere um programa de onboarding.")

# ============ GRÁFICOS PRINCIPAIS ============

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Visão Geral", 
    "📊 Churn por Categoria", 
    "📉 Análise Temporal",
    "📋 Dados Detalhados"
])

# ============ TAB 1: VISÃO GERAL ============

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribuição de Churn")
        churn_counts = filtered_df['Churn'].value_counts().reset_index()
        churn_counts.columns = ['Churn', 'Count']
        
        # GRÁFICO DE PIZZA CORRIGIDO - VERSÃO ALTERNATIVA
        fig = px.pie(
            churn_counts,
            values='Count',
            names='Churn',
            color='Churn',
            color_discrete_map={'Yes': '#ff6b6b', 'No': '#4ecdc4'},
            hole=0.4,
            title='Distribuição de Churn'
        )
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            insidetextorientation='radial'
        )
        fig.update_layout(
            height=400,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Distribuição por Tipo de Contrato")
        contract_dist = filtered_df['Contract'].value_counts().reset_index()
        contract_dist.columns = ['Contract', 'Count']
        
        fig = px.bar(
            contract_dist,
            x='Contract',
            y='Count',
            color='Contract',
            text='Count',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(height=400, showlegend=False)
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

# ============ TAB 2: CHURN POR CATEGORIA ============

with tab2:
    st.subheader("Análise Detalhada de Churn por Categoria")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Categorias selecionáveis
        category_options = {
            'Contract': 'Tipo de Contrato',
            'PaymentMethod': 'Forma de Pagamento',
            'InternetService': 'Tipo de Internet',
            'TenureGroup': 'Tempo de Cliente',
            'MonthlyGroup': 'Faixa de Mensalidade',
            'gender': 'Gênero',
            'SeniorCitizen': 'Idoso (1=Sim, 0=Não)',
            'Partner': 'Tem Parceiro',
            'Dependents': 'Tem Dependentes',
            'PaperlessBilling': 'Fatura Digital'
        }
        
        selected_category = st.selectbox(
            "Selecione uma categoria para análise:",
            options=list(category_options.keys()),
            format_func=lambda x: category_options[x]
        )
    
    with col2:
        # Ordenação
        sort_order = st.radio(
            "Ordenar por:",
            options=['Taxa de Churn (maior para menor)', 'Taxa de Churn (menor para maior)', 'Quantidade de Clientes'],
            horizontal=True
        )
    
    # Gerar gráfico
    churn_data = create_churn_by_category(filtered_df, selected_category)
    
    if sort_order == 'Taxa de Churn (maior para menor)':
        churn_data = churn_data.sort_values('churn_rate', ascending=False)
    elif sort_order == 'Taxa de Churn (menor para maior)':
        churn_data = churn_data.sort_values('churn_rate', ascending=True)
    else:
        churn_data = churn_data.sort_values('count', ascending=False)
    
    # Gráfico de barras com duas séries
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Taxa de Churn', 'Distribuição de Clientes'),
        specs=[[{'secondary_y': False}, {'secondary_y': False}]]
    )
    
    # Taxa de Churn
    fig.add_trace(
        go.Bar(
            x=churn_data[selected_category],
            y=churn_data['churn_percent'],
            name='Taxa de Churn (%)',
            marker_color='#ff6b6b',
            text=churn_data['churn_percent'],
            texttemplate='%{text}%',
            textposition='outside'
        ),
        row=1, col=1
    )
    
    # Distribuição
    fig.add_trace(
        go.Bar(
            x=churn_data[selected_category],
            y=churn_data['percentage_of_total'],
            name='% do Total',
            marker_color='#4ecdc4',
            text=churn_data['percentage_of_total'],
            texttemplate='%{text}%',
            textposition='outside'
        ),
        row=1, col=2
    )
    
    fig.update_layout(height=450, showlegend=False)
    fig.update_xaxes(title_text=category_options[selected_category], row=1, col=1)
    fig.update_xaxes(title_text=category_options[selected_category], row=1, col=2)
    fig.update_yaxes(title_text='Taxa de Churn (%)', row=1, col=1)
    fig.update_yaxes(title_text='% do Total', row=1, col=2)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabela de dados
    with st.expander("📊 Ver dados detalhados"):
        display_cols = [selected_category, 'count', 'total', 'churn_percent', 'percentage_of_total']
        display_df = churn_data[display_cols].copy()
        display_df.columns = ['Categoria', 'Clientes com Churn', 'Total', 'Taxa de Churn (%)', '% do Total']
        st.dataframe(display_df, use_container_width=True)

# ============ TAB 3: ANÁLISE TEMPORAL ============

with tab3:
    st.subheader("Análise Temporal do Churn")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Distribuição por tempo de cliente
        tenure_bins = pd.cut(filtered_df['tenure'], bins=range(0, 75, 6))
        tenure_churn = filtered_df.groupby(tenure_bins, observed=False).agg({
            'Churn_Num': ['mean', 'count'],
            'customerID': 'count'
        }).reset_index()
        tenure_churn.columns = ['Tenure', 'churn_rate', 'churn_count', 'total']
        tenure_churn['churn_percent'] = (tenure_churn['churn_rate'] * 100).round(1)
        
        # Converter intervalos para string
        tenure_churn['Tenure'] = tenure_churn['Tenure'].astype(str)
        
        fig = px.bar(
            tenure_churn,
            x='Tenure',
            y='churn_percent',
            text='churn_percent',
            title='Taxa de Churn por Período de Cliente (6 meses)',
            labels={'churn_percent': 'Taxa de Churn (%)', 'Tenure': 'Período (meses)'},
            color='churn_percent',
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=400)
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📈 Insights Temporais")
        
        high_risk = filtered_df[filtered_df['tenure'] <= 6]['Churn_Num'].mean() if len(filtered_df[filtered_df['tenure'] <= 6]) > 0 else 0
        medium_risk = filtered_df[(filtered_df['tenure'] > 6) & (filtered_df['tenure'] <= 12)]['Churn_Num'].mean() if len(filtered_df[(filtered_df['tenure'] > 6) & (filtered_df['tenure'] <= 12)]) > 0 else 0
        low_risk = filtered_df[filtered_df['tenure'] > 12]['Churn_Num'].mean() if len(filtered_df[filtered_df['tenure'] > 12]) > 0 else 0
        
        st.markdown(f"""
            <div class="risk-high" style="color: #666">
                <b>🔴 Primeiros 6 meses:</b> {high_risk:.1%} de churn
            </div>
            <div class="risk-medium" style="color: #666">
                <b>🟡 7-12 meses:</b> {medium_risk:.1%} de churn
            </div>
            <div class="risk-low" style="color: #666">
                <b>🟢 Mais de 1 ano:</b> {low_risk:.1%} de churn
            </div>
        """, unsafe_allow_html=True)
        
        if high_risk > 0:
            reduction = (1 - low_risk/high_risk) * 100 if high_risk > 0 else 0
            st.markdown(f"""
                <div style="color: #666; background-color: #fff3cd; padding: 1rem; border-radius: 8px; border: 1px solid #ffc107;">
                    <b>💡 Conclusão:</b><br>
                    Os primeiros 6 meses são críticos. Clientes que passam desse período têm 
                    <b>{reduction:.0f}% menos chance</b> de cancelar.
                </div>
            """, unsafe_allow_html=True)

# ============ TAB 4: DADOS DETALHADOS ============

with tab4:
    st.subheader("📋 Dados Detalhados")
    
    # Seleção de colunas para exibir
    default_cols = ['customerID', 'gender', 'SeniorCitizen', 'tenure', 'Contract', 
                    'PaymentMethod', 'MonthlyCharges', 'TotalCharges', 'Churn']
    
    all_cols = filtered_df.columns.tolist()
    selected_cols = st.multiselect(
        "Selecione as colunas para visualizar:",
        options=all_cols,
        default=[col for col in default_cols if col in all_cols]
    )
    
    if selected_cols:
        # Paginação
        page_size = st.number_input("Linhas por página:", min_value=5, max_value=100, value=20)
        total_pages = (len(filtered_df) + page_size - 1) // page_size if len(filtered_df) > 0 else 1
        page = st.number_input("Página:", min_value=1, max_value=total_pages, value=1)
        
        start_idx = (page - 1) * page_size
        end_idx = min(start_idx + page_size, len(filtered_df))
        
        display_df = filtered_df[selected_cols].iloc[start_idx:end_idx]
        st.dataframe(display_df, use_container_width=True)
        
        st.caption(f"Mostrando {start_idx + 1} - {end_idx} de {len(filtered_df)} registros")

# ============ INSIGHTS FINAIS ============

st.markdown("---")
st.markdown("## 💡 Principais Insights e Recomendações")

col1, col2, col3 = st.columns(3)

# Calcular métricas para insights
churn_contract = create_churn_by_category(df, 'Contract')
churn_payment = create_churn_by_category(df, 'PaymentMethod')
churn_tenure = create_churn_by_category(df, 'TenureGroup')

monthly_rate = churn_contract[churn_contract['Contract'] == 'Month-to-month']['churn_percent'].values[0] if 'Month-to-month' in churn_contract['Contract'].values else 0
one_year_rate = churn_contract[churn_contract['Contract'] == 'One year']['churn_percent'].values[0] if 'One year' in churn_contract['Contract'].values else 0
electronic_check_rate = churn_payment[churn_payment['PaymentMethod'] == 'Electronic check']['churn_percent'].values[0] if 'Electronic check' in churn_payment['PaymentMethod'].values else 0
credit_card_rate = churn_payment[churn_payment['PaymentMethod'] == 'Credit card (automatic)']['churn_percent'].values[0] if 'Credit card (automatic)' in churn_payment['PaymentMethod'].values else 0
early_churn = churn_tenure[churn_tenure['TenureGroup'] == '0-6 meses']['churn_percent'].values[0] if '0-6 meses' in churn_tenure['TenureGroup'].values else 0
late_churn = churn_tenure[churn_tenure['TenureGroup'] == '25+ meses']['churn_percent'].values[0] if '25+ meses' in churn_tenure['TenureGroup'].values else 0

# Card 1
with col1:
    st.markdown("#### 🔴 Contrato Mensal")
    st.markdown(f"""
        <div style="background-color: #ffebee; padding: 1.2rem; border-radius: 10px; border: 1px solid #ef9a9a; height: 100%;">
            <p style="font-size: 2rem; font-weight: 700; color: #c62828; margin: 0;">{monthly_rate:.1f}%</p>
            <p style="color: #666;">de taxa de churn</p>
            <p style="color: #666;">Clientes com contrato mensal têm <b>{monthly_rate/one_year_rate:.1f}x mais</b> chance de cancelar</p>
            <p style="color: #666; background-color: #fff; padding: 0.5rem; border-radius: 4px; margin-top: 0.5rem;">
                ✅ <b>Recomendação:</b> Oferecer desconto para migração para plano anual
            </p>
        </div>
    """, unsafe_allow_html=True)

# Card 2
with col2:
    st.markdown("#### &#x1F4B3; Forma Pagamentos")
    st.markdown(f"""
        <div style="background-color: #fff3e0; padding: 1.2rem; border-radius: 10px; border: 1px solid #ffcc80; height: 100%;">
            <p style="font-size: 2rem; font-weight: 700; color: #e65100; margin: 0;">{electronic_check_rate:.1f}%</p>
            <p style="color: #666;">de churn com boleto eletrônico</p>
            <p style="color: #666;">Débito automático tem apenas <b>{credit_card_rate:.1f}%</b> de churn</p>
            <p style="color: #666; background-color: #fff; padding: 0.5rem; border-radius: 4px; margin-top: 0.5rem;">
                &#x2705; <b>Recomendação:</b> Oferecer cashback/desconto para débito automático
            </p>
        </div>
    """, unsafe_allow_html=True)

# Card 3
with col3:
    st.markdown("#### ⏱️ Primeiros Meses")
    st.markdown(f"""
        <div style="background-color: #e8f5e9; padding: 1.2rem; border-radius: 10px; border: 1px solid #a5d6a7; height: 100%;">
            <p style="font-size: 2rem; font-weight: 700; color: #2e7d32; margin: 0;">{early_churn:.1f}%</p>
            <p style="color: #666;">de churn nos primeiros 6 meses</p>
            <p style="color: #666;">Após o período de 1 ano, churn cai para <b>{late_churn:.1f}%</b></p>
            <p style="color: #666; background-color: #fff; padding: 0.5rem; border-radius: 4px; margin-top: 0.5rem;">
                ✅ <b>Recomendação:</b> Programa de onboarding e suporte intensivo no início
            </p>
        </div>
    """, unsafe_allow_html=True)

# ============ DOWNLOAD ============

st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("📥 Baixar Dados Filtrados (CSV)", use_container_width=True):
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="✅ Clique para baixar",
            data=csv,
            file_name="churn_analysis_filtered.csv",
            mime="text/csv",
            use_container_width=True
        )

st.markdown("---")
st.caption("📊 Dashboard desenvolvido com Streamlit | Dados: Telco Customer Churn Dataset")

# Rodapé com informações
with st.expander("ℹ️ Sobre o Dashboard"):
    st.markdown("""
        ### Sobre este Dashboard
        
        Este dashboard foi desenvolvido para análise de churn de clientes de telecomunicações.
        
        **Fonte dos dados:** Telco Customer Churn Dataset (IBM)
        
        **Principais funcionalidades:**
        - Filtros interativos para segmentação de clientes
        - Visualização de métricas principais
        - Análise de churn por diferentes categorias
        - Análise temporal de churn
        - Exportação de dados filtrados
        
        **Tecnologias utilizadas:**
        - Streamlit
        - Pandas
        - Plotly
    """)