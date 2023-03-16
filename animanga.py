import streamlit as st
import pandas as pd
import plotly.express as px
import codecs

DATA_URL = ('manga.csv')
st.set_page_config(page_title="Anime Complete List",
                   page_icon="logo.jpg")

st.title("Mangas")

st.sidebar.image("logo.jpg")
st.sidebar.markdown("##")
st.sidebar.header("Autor:")
st.sidebar.header("*Magdyel Aguilar Cid*")
st.sidebar.write("S20020309")
sidebar= st.sidebar

@st.cache
def load_data(nrows):
    f = codecs.open(DATA_URL,'r', encoding='utf-8')
    data=pd.read_csv(f,nrows=nrows)
    return data

def filtro_manga(manga):
    manga_filter = data[data['title'].str.upper().str.contains(manga)]
    return manga_filter

def filtro_estado(status):
    status_filter = data[data['status'] == status]
    return status_filter

data_load_state= st.text("Loading data...")
data= load_data(5000)
data_load_state.text("Done!")

agree=sidebar.checkbox("Mostrar todos los mangas")
if agree:
    st.header("Todos los Mangas")
    st.dataframe(data)

#Busqueda por titulo del manga
tituloManga = st.sidebar.text_input('Titulo del Manga :')
botonBuscar = st.sidebar.button('Buscar Manga')

if (botonBuscar):
   manga = filtro_manga(tituloManga.upper())
   count_row = manga.shape[0]
   st.header("Mangas")
   st.write(f"Total de Mangas mostrados : {count_row}")
   st.write(manga)

#Filtro por status
statusManga = st.sidebar.selectbox("Estado del Manga", data['status'].unique())
botonFiltroEstatus = st.sidebar.button('Filtrar por Estado')

if (botonFiltroEstatus):
   status = filtro_estado(statusManga)
   count_row = status.shape[0]
   st.write(f"Total de mangas por estado: {count_row}")
   st.dataframe(status)


#Histograma volumenes
agreeHistogram=sidebar.checkbox("Mostrar histograma")
if agreeHistogram:
    fig_volumes = px.histogram(data,
                       x="volumes",
                       title="Numero de volumenes por manga",
                       color_discrete_sequence=["#634a71"],
                       template="plotly_white"
                       )
    fig_volumes.update_layout(xaxis_title='Volumenes',yaxis_title='Numero de titulos')
    fig_volumes.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.header("Histograma de volumenes")
    st.plotly_chart(fig_volumes)
    st.write("Se muestra el numero de titulos que cuentan con las distintas cantidades de volumenes, en donde predominan los titulos con un solo volumen siendo 1123")

#Grafica de barras
agreeBar=sidebar.checkbox("Mostrar Barras")
if agreeBar:
    scoredBytype=(
        data.groupby(by=['type']).sum()['scored_by']
        )
    fig_type=px.bar(scoredBytype,
                    x=scoredBytype.index,
                    y="scored_by",
                    title="Puntuaciones hechas a cada una de las categorias de manga",
                    color_discrete_sequence=["#f86749"],
                    template="plotly_white")
    fig_type.update_layout(xaxis_title='Categoria',yaxis_title='Puntuaciones hechas')
    fig_type.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.header("Grafica de barras")
    st.plotly_chart(fig_type)
    st.write("Se muestra la cantidad de personas que han puntuado las distintas categorias de manga, siendo el manga la que mas personas han puntuado")

#Grafica de scatter
agreeScatter=sidebar.checkbox("Mostrar Scatter")
if agreeScatter:
    volumes=data['volumes']
    chapters=data['chapters']
    tipe=data['type']
    fig_scatter=px.scatter(data,
                             x=volumes,
                             y=chapters,
                             color=tipe,
                             labels=dict(volumes='Numero de volumenes',chapters="Capitulos", type="Categoria"),
                             title="Capitulos por cantidad de volumenes",
                             template="plotly_white")
    fig_scatter.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.header("Grafica de Scatter")
    st.plotly_chart(fig_scatter)
    st.write("Se muestra la relacion entre la cantidad de volumenes de cierta categoria de manga con su cantidad de capitulos")
