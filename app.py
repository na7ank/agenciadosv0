import pandas as pd
import streamlit as st
import plotly.express as px


# Titulo
st.set_page_config(layout="wide")
st.title('Informações Básicas sobre Agências Bancárias')


data = pd.read_csv('./dataset/202311bccags.csv', sep=';', encoding='utf-8-sig')

# Side Menu
with st.sidebar:
    st.write('Selecione os filtros de preferência para particionar os dados.')
    uf = st.multiselect("UF", list(set(data['uf'])), ['SP'])
    instituicao = st.multiselect("Instituição", list(set(data['Instituição'])), ['BANCO DO BRASIL S.A.'])
    codigo = st.slider('Agência Código', min(data['Código']), max(data['Código']), (0, 1000))

# Filter Data
cond = (data['uf'].isin(uf)) & (data['Instituição'].isin(instituicao))
cond_cod = (data['Código'] >= codigo[0]) & (data['Código'] <= codigo[1])
data = data[cond]  # Make sure to convert option to int if it's supposed to be a number
data = data[cond_cod]

# Center
table, locals, bars = st.tabs(["🏦 Agências", "📈 Quantidades", "📊 Top 7"])
with bars:
    st.write("Bancos com maior quantidades de agências.")
    data_full = pd.read_csv('./dataset/202311bccags.csv', sep=';', encoding='utf-8-sig', usecols=['Instituição', 'uf'])
    data_full = data_full[data_full['uf'].isin(uf)]
    # Counts
    contagem_classes = data_full['Instituição'].value_counts().reset_index(name='Qnt')
    contagem_classes = contagem_classes.sort_values(by='Qnt', ascending=False).head(7)
    # Graph
    fig = px.bar(contagem_classes, x='Qnt', y='Instituição', orientation='h', labels={'x': 'Qnt', 'y': 'Instituição'}, color='Qnt', color_continuous_scale='reds', opacity=0.8)
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, config={"displayModeBar": False})

with table:
    st.write("🎲 Dados")
    st.dataframe(data, hide_index=True)

with locals:
    st.write("Locais com maior número de Agências.")
    groups = data[['Bairro', 'uf', 'Município']].groupby(['Bairro', 'uf', 'Município']).value_counts().reset_index(name='Qnt Agências')
    st.dataframe(groups, hide_index=True)

#python -m streamlit run app.py