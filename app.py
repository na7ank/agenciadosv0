import pandas as pd
import streamlit as st
import plotly.express as px

# Titulo
st.set_page_config(page_title="graficando", 
                   page_icon="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Map-circle-blue.svg/1024px-Map-circle-blue.svg.png",
                   initial_sidebar_state="expanded", layout="wide"
                   )
st.title('Informações Básicas sobre Agências Bancárias')

hidden = """
            <style>
            .reportview-container .main footer {visibility: hidden;}
            #MainMenu {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            footer {display: none !important;}
            header {visibility: hidden !important;}
            </style>
            """
st.markdown(hidden, unsafe_allow_html=True)

# Load data, formats
data = pd.read_csv('./dataset/202312bccags.csv', sep=';', encoding='ISO-8859-1')
data['Código'] = data['Código'].astype(str) 

# Side Menu
with st.sidebar:
    st.write('Selecione os filtros de preferência para particionar os dados.')

    col1, col2 = st.columns(2)
    with col1:
        check_box_ufs = st.checkbox('All UFs:', value=False)
    with col2:
        check_box_bancos = st.checkbox('All Bancos:', value=False)
    
    uf = st.multiselect("UF", list(set(data['uf'])))
    municipio = st.multiselect("Municípios", list(set(data['Município'])), [])
    bairro = st.multiselect("Bairros", list(set(data['Bairro'])), [])
    
    instituicao = st.multiselect("Instituição", list(set(data['Instituição'])), ['BANCO BRADESCO S.A.'])
    check_box_codigos = st.checkbox('All Códigos:', value=True)
    codigo = st.number_input('Código específico:', min_value=0, step=1)

# Filter check box Data
if not check_box_ufs:
    cond_uf = (data['uf'].isin(uf))
    data = data[cond_uf]
if not check_box_bancos:
    cond_instituicao = (data['Instituição'].isin(instituicao))
    data = data[cond_instituicao]
if not check_box_codigos:
    data = data[data['Código'] == str(codigo)]
if bairro != []:
    data = data[data['Bairro'].isin(bairro)]
if municipio != []:
    data = data[data['Município'].isin(municipio)]

# Center
table, locals, bars = st.tabs(["🏦 Agências", "📈 Quantidades", "📊 Top 7"])
with bars:
    data_full = pd.read_csv('./dataset/202312bccags.csv', sep=';', encoding='ISO-8859-1', usecols=['Instituição', 'uf'])
    st.write(f"Bancos com maior quantidade de agências. Total **{data_full.shape[0]}** agências.")
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
    st.write(f"**{data.shape[0]}** Agências encontradas.")
    st.dataframe(data, hide_index=True, width = 1280)

with locals:
    groups = data[['Bairro', 'uf', 'Município']].groupby(['Bairro', 'uf', 'Município']).value_counts().reset_index(name='Qnt Agências')
    st.write("Quantidade de agências agrupadas por uf, município e bairro.") 
    st.dataframe(groups, hide_index=True, width = 1280)


#python -m streamlit run app.py