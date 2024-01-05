import pandas as pd
import streamlit as st
import plotly.express as px


# Titulo
st.set_page_config(page_title="graficando", 
                   page_icon="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Map-circle-blue.svg/1024px-Map-circle-blue.svg.png",
                   initial_sidebar_state="expanded", layout="wide"
                   )
st.title('Informações Básicas sobre Agências Bancárias')

try_hidden = """
            <style>
            [data-testid="stToolbar"] {visibility: hidden !important;}
            #MainMenu {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            header {visibility: hidden !important;}
            a {display: none !important;}
            </style>
            """


data = pd.read_csv('./dataset/202311bccags.csv', sep=';', encoding='utf-8-sig')

#primary_clr = st.get_option("theme.primaryColor")

# Side Menu
with st.sidebar:
    st.write('Selecione os filtros de preferência para particionar os dados.')
    col1, col2 = st.columns(2)
    with col1:
        check_box_ufs = st.checkbox('All UFs:', value=False)
    with col2:
        check_box_bancos = st.checkbox('All Bancos:', value=False)
    
    uf = st.multiselect("UF", list(set(data['uf'])), ['SP'])
    instituicao = st.multiselect("Instituição", list(set(data['Instituição'])), ['BANCO BRADESCO S.A.'])
    codigo = st.slider('Agência Código', min(data['Código']), max(data['Código']), (0, 1000))

# Filter chack box Data
if not check_box_ufs:
    cond_uf = (data['uf'].isin(uf))
    data = data[cond_uf]
if not check_box_bancos:
    cond_instituicao = (data['Instituição'].isin(instituicao))
    data = data[cond_instituicao]

cond_cod = (data['Código'] >= codigo[0]) & (data['Código'] <= codigo[1])
data = data[cond_cod]

# Center
table, locals, bars = st.tabs(["🏦 Agências", "📈 Quantidades", "📊 Top 7"])
with bars:
    st.write("Bancos com maior quantidades de agências.")
    data_full = pd.read_csv('./dataset/202311bccags.csv', sep=';', encoding='utf-8-sig', usecols=['Instituição', 'uf'])
    if not check_box_ufs:
        data_full = data_full[data_full['uf'].isin(uf)]
    # Counts
    contagem_classes = data_full['Instituição'].value_counts().reset_index(name='Qnt')
    contagem_classes = contagem_classes.sort_values(by='Qnt', ascending=False).head(7)
    # Graph
    color = st.color_picker('', '#FF2600')
    color_scale = [(0.0, '#EFEFEF'), (1.0, color)]
    fig = px.bar(contagem_classes, x='Qnt', y='Instituição', orientation='h', labels={'x': 'Qnt', 'y': 'Instituição'}, color='Qnt', color_continuous_scale=color_scale, opacity=0.8)
    
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, config={"displayModeBar": False})

with table:
    st.write("🎲 Dados")
    st.write(f"{data.shape[0]} Agências encontradas.")
    st.dataframe(data, hide_index=True)

with locals:
    groups = data[['Bairro', 'uf', 'Município']].groupby(['Bairro', 'uf', 'Município']).value_counts().reset_index(name='Qnt Agências')
    st.write("Quantidade de agências agrupadas por uf, município e bairro.") 
    st.dataframe(groups, hide_index=True)
