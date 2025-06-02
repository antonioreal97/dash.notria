import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Paleta de cores personalizada
COLOR_PRIMARY = '#2F473F'
COLOR_SECONDARY = '#69C655'
COLOR_ACCENT = '#CC4A23'
COLOR_LIST = [COLOR_PRIMARY, COLOR_SECONDARY, COLOR_ACCENT]

# Função para ler e organizar os dados
@st.cache_data
def load_data(path):
    df = pd.read_excel(path, header=[0,1])
    for col in [('Dimensão', ''), ('Subdimensão', '')]:
        if col in df.columns:
            df[col] = df[col].fillna(method='ffill')
    return df

# Função para atualizar os dados
if 'atualizar' not in st.session_state:
    st.session_state['atualizar'] = 0

def atualizar_dados():
    st.session_state['atualizar'] += 1

# Configuração da página
st.set_page_config(page_title='Dashboard Avaliativo', layout='wide', page_icon='📊')

# Estilos customizados
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Yrsa:wght@400;600&display=swap" rel="stylesheet">
    <style>
    :root {
      --font-primary: 'Poppins', sans-serif;
      --font-secondary: 'Yrsa', serif;
      --color-secondary: #69C655;
    }
    html, body, .stApp, [data-testid="stSidebar"] {
        background-color: #fff !important;
        color: #222 !important;
        font-family: var(--font-primary) !important;
    }
    * {
        font-family: var(--font-primary) !important;
    }
    header, .st-emotion-cache-18ni7ap, .st-emotion-cache-1avcm0n, .st-emotion-cache-6qob1r {
        background: #fff !important;
        box-shadow: none !important;
        color: #2F473F !important;
    }
    header * {
        color: #2F473F !important;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3, section[data-testid="stSidebar"] h4 {
        font-size: 2em !important;
        color: #2F473F !important;
        font-weight: 800 !important;
        margin-bottom: 18px !important;
        font-family: var(--font-primary) !important;
    }
    .stMultiSelect, .stSelectbox, .stSlider, .stTextInput, .stNumberInput {
        background-color: #2F473F !important;
        border-radius: 12px !important;
        color: #fff !important;
        border: 1.5px solid #2F473F !important;
        margin-bottom: 12px !important;
        padding: 6px 8px !important;
        font-family: var(--font-primary) !important;
    }
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6, .stMarkdown h3, .stMarkdown h2, .stMarkdown h1 {
        color: #2F473F !important;
        font-weight: 700;
        margin-bottom: 8px;
        font-family: var(--font-primary) !important;
    }
    /* KPIs customizados - borda, sombra e texto verde escuro ultra-específico */
    div[data-testid="metric-container"] {
        border-radius: 12px;
        border: 1.5px solid #2F473F;
        padding: 16px 8px 8px 16px;
        margin-bottom: 8px;
        box-shadow: 0 2px 8px rgba(47,71,63,0.08);
        background: none !important;
    }
    /* Forçar cor do texto dos KPIs (títulos e valores) para verde escuro em todos os elementos internos */
    div[data-testid="metric-container"],
    div[data-testid="metric-container"] *,
    div[data-testid="metric-container"] span,
    div[data-testid="metric-container"] div,
    div[data-testid="metric-container"] strong,
    div[data-testid="metric-container"] p,
    div[data-testid="metric-container"] [data-testid="stMetricLabel"],
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #2F473F !important;
        background: transparent !important;
        text-shadow: none !important;
    }
    /* Botão de atualização */
    .stButton > button {
        background-color: #CC4A23 !important;
        color: #fff !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 10px 24px !important;
        font-size: 1.1em !important;
        margin-bottom: 18px !important;
        box-shadow: 0 2px 8px rgba(204,74,35,0.10);
    }
    .stButton > button:hover {
        background-color: #a53a1a !important;
        color: #fff !important;
    }
    /* Tabela detalhada */
    .stDataFrame, .stTable {
        background: #fff !important;
        color: #222 !important;
        border-radius: 10px !important;
    }
    .stDataFrame th, .stDataFrame td, .stTable th, .stTable td {
        background: #fff !important;
        color: #222 !important;
    }
    /* Avisos (warnings) */
    .stAlert {
        background-color: #FFF9DB !important;
        color: #2F473F !important;
        border-radius: 10px !important;
        border: 1.5px solid #F7D774 !important;
        font-weight: 600 !important;
    }
    .stAlert p {
        color: #2F473F !important;
        font-weight: 600 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título do app
st.title('Dashboard Avaliativo - Ceasas')

# Botão para atualizar os dados
st.button('Atualizar Dados', on_click=atualizar_dados)

# Caminho fixo do arquivo
file_path = 'dashboard_perguntas/Matriz_Avaliativa_Ceasas-Dashboard.xlsx'
# Carrega dados
df = load_data(file_path)

# Sidebar de filtros
st.sidebar.header('Filtros')
dimensoes = df[('Dimensão', 'Unnamed: 0_level_1')].dropna().unique().tolist() if ('Dimensão', 'Unnamed: 0_level_1') in df.columns else []
subdimensoes = df[('Subdimensão', 'Unnamed: 1_level_1')].dropna().unique().tolist() if ('Subdimensão', 'Unnamed: 1_level_1') in df.columns else []
ceasas = ['Belem/PA', 'São Luís/MA', 'CEAGESP/SP', 'Mais Nutrição/CE', 'PRODAL/MG', 'Curitiba/PR', 'GLOBAL']
ceasas = [c for c in ceasas if (c, 'Pontos') in df.columns]
filtro_dim = st.sidebar.multiselect('Dimensão', dimensoes, default=[])
filtro_subdim = st.sidebar.multiselect('Subdimensão', subdimensoes, default=[])
ceasa_sel = st.sidebar.selectbox('Ceasa', [''] + ceasas) if ceasas else None

# Lógica de filtro
if filtro_dim or filtro_subdim:
    mask = pd.Series([True] * len(df))
    if filtro_dim:
        mask &= df[('Dimensão', 'Unnamed: 0_level_1')].isin(filtro_dim)
    if filtro_subdim:
        mask &= df[('Subdimensão', 'Unnamed: 1_level_1')].isin(filtro_subdim)
    df_filt = df[mask]
else:
    df_filt = df

# Exibição de KPIs e gráficos
if ceasa_sel and ceasa_sel != '':
    # Identifica colunas dinâmicas com base na Ceasa selecionada (multi-index)
    col_pontos = (ceasa_sel, 'Pontos')
    col_subdim = (ceasa_sel, '% da Subdimensão')
    col_dim = (ceasa_sel, '% Total da Dimensão')
    col_result = (ceasa_sel, 'Resultado da Matriz')

    total_perguntas = len(df_filt)
    soma_pontos = df_filt[col_pontos].sum() if col_pontos in df_filt.columns else 0
    media_subdim = df_filt[col_subdim].mean() if col_subdim in df_filt.columns else 0
    media_dim = df_filt[col_dim].mean() if col_dim in df_filt.columns else 0
    media_result = df_filt[col_result].mean() if col_result in df_filt.columns else 0

    # KPIs em cards customizados
    st.markdown(
        f'''
        <div style="display: flex; gap: 32px; margin-bottom: 24px;">
            <div style="background: #fff; border: 1.5px solid #2F473F; border-radius: 14px; box-shadow: 0 2px 8px rgba(47,71,63,0.08); padding: 18px 32px; min-width: 180px; text-align: center;">
                <div style="color: #2F473F; font-size: 1.1em; font-weight: 700; margin-bottom: 6px;">Total de Perguntas</div>
                <div style="color: #2F473F; font-size: 2.5em; font-weight: 700;">{total_perguntas}</div>
            </div>
            <div style="background: #fff; border: 1.5px solid #2F473F; border-radius: 14px; box-shadow: 0 2px 8px rgba(47,71,63,0.08); padding: 18px 32px; min-width: 180px; text-align: center;">
                <div style="color: #2F473F; font-size: 1.1em; font-weight: 700; margin-bottom: 6px;">Soma dos Pontos</div>
                <div style="color: #2F473F; font-size: 2.5em; font-weight: 700;">{soma_pontos:.0f}</div>
            </div>
            <div style="background: #fff; border: 1.5px solid #2F473F; border-radius: 14px; box-shadow: 0 2px 8px rgba(47,71,63,0.08); padding: 18px 32px; min-width: 180px; text-align: center;">
                <div style="color: #2F473F; font-size: 1.1em; font-weight: 700; margin-bottom: 6px;">Média % Subdimensão</div>
                <div style="color: #2F473F; font-size: 2.5em; font-weight: 700;">{media_subdim:.2%}</div>
            </div>
            <div style="background: #fff; border: 1.5px solid #2F473F; border-radius: 14px; box-shadow: 0 2px 8px rgba(47,71,63,0.08); padding: 18px 32px; min-width: 180px; text-align: center;">
                <div style="color: #2F473F; font-size: 1.1em; font-weight: 700; margin-bottom: 6px;">Média % Dimensão</div>
                <div style="color: #2F473F; font-size: 2.5em; font-weight: 700;">{media_dim:.2%}</div>
            </div>
            <div style="background: #fff; border: 1.5px solid #2F473F; border-radius: 14px; box-shadow: 0 2px 8px rgba(47,71,63,0.08); padding: 18px 32px; min-width: 180px; text-align: center;">
                <div style="color: #2F473F; font-size: 1.1em; font-weight: 700; margin-bottom: 6px;">Média Resultado Matriz</div>
                <div style="color: #2F473F; font-size: 2.5em; font-weight: 700;">{media_result:.2%}</div>
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )
    # Gráfico por Subdimensão usando a coluna 'Soma (pts)'
    st.markdown('#### Pontuação por Subdimensão')
    col_subdimensao = ('Subdimensão', 'Unnamed: 1_level_1')
    col_soma_pts = (ceasa_sel, 'Soma (pts)')
    if col_subdimensao in df_filt.columns and col_soma_pts in df_filt.columns:
        df_graf = df_filt[[col_subdimensao, col_soma_pts]].copy()
        df_graf.columns = ['Subdimensão', 'Soma (pts)']
        df_graf = df_graf.dropna(subset=['Subdimensão', 'Soma (pts)'])
        fig = px.bar(
            df_graf,
            x='Subdimensão',
            y='Soma (pts)',
            color='Subdimensão',
            title=f'Soma dos Pontos por Subdimensão - {ceasa_sel}',
            color_discrete_sequence=COLOR_LIST,
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    # Tabela detalhada
    st.markdown('### Tabela Detalhada')
    # Exibir todas as perguntas e respostas do Ceasa selecionado
    col_resposta = (ceasa_sel, 'Resposta') if (ceasa_sel, 'Resposta') in df_filt.columns else None
    cols_tabela = [
        ('Dimensão', 'Unnamed: 0_level_1'),
        ('Subdimensão', 'Unnamed: 1_level_1'),
        ('Nº', 'Unnamed: 2_level_1'),
        ('Perguntas', 'Unnamed: 3_level_1'),
    ]
    if col_resposta:
        cols_tabela.append(col_resposta)
    # Adiciona as métricas do Ceasa selecionado
    for c in [col_pontos, col_subdim, col_dim, col_result, col_soma_pts]:
        if c in df_filt.columns:
            cols_tabela.append(c)
    st.dataframe(df_filt[cols_tabela], use_container_width=True)
else:
    # Exibição padrão: gráfico comparando todos os Ceasas
    st.markdown('### Comparativo entre Ceasas')
    ceasa_pontos = []
    for ceasa in ceasas:
        col_pontos = (ceasa, 'Pontos')
        if col_pontos in df.columns:
            soma = df[col_pontos].sum()
            ceasa_pontos.append({'Ceasa': ceasa, 'Soma dos Pontos': soma})
    df_ceasa = pd.DataFrame(ceasa_pontos)
    if not df_ceasa.empty:
        fig = px.bar(df_ceasa, x='Ceasa', y='Soma dos Pontos', color='Ceasa', color_discrete_sequence=COLOR_LIST,
                     title='Soma dos Pontos por Ceasa')
        st.plotly_chart(fig, use_container_width=True)
    # KPIs globais
    total_perguntas = len(df)
    soma_total = sum([df[(ceasa, 'Pontos')].sum() for ceasa in ceasas if (ceasa, 'Pontos') in df.columns])
    st.markdown(
        f'''
        <div style="display: flex; gap: 32px; margin-bottom: 24px;">
            <div style="background: #fff; border: 1.5px solid #2F473F; border-radius: 14px; box-shadow: 0 2px 8px rgba(47,71,63,0.08); padding: 18px 32px; min-width: 180px; text-align: center;">
                <div style="color: #2F473F; font-size: 1.1em; font-weight: 700; margin-bottom: 6px;">Total de Perguntas</div>
                <div style="color: #2F473F; font-size: 2.5em; font-weight: 700;">{total_perguntas}</div>
            </div>
            <div style="background: #fff; border: 1.5px solid #2F473F; border-radius: 14px; box-shadow: 0 2px 8px rgba(47,71,63,0.08); padding: 18px 32px; min-width: 180px; text-align: center;">
                <div style="color: #2F473F; font-size: 1.1em; font-weight: 700; margin-bottom: 6px;">Soma Total dos Pontos</div>
                <div style="color: #2F473F; font-size: 2.5em; font-weight: 700;">{soma_total:.0f}</div>
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )
    st.info('Selecione um Ceasa para visualizar os detalhes.')
