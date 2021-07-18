from os import read
import streamlit as st
import pandas as pd
from tabula import read_pdf
import base64
from io import BytesIO
import app


def header_intro():
    col1, col3 = st.beta_columns([1, 1])
    with col1:
        st.header('Price Miner')
        st.text('version 0.1 - Last update 17/07/2022')
    with col3:
        st.image('dados/miner.png', width=150)


def header_intro_2():
    st.write("Minerador de preços voltado para buscas em lojas brasileiras, digite o nome do produto que deseja pesquisar e receba o resultado da busca em seu e-mail. ")
    st.write("A quantidade de itens pesquisados pode variar, pois são retirados itens promocionais ou não relevantes à busca. Serão retornados no máximo 25 itens de cada loja, por busca realizada.")


def side_bar_credis():

    st.sidebar.write('Contact:')
    st.sidebar.write('**Matheus Teixeira Silva**')
    st.sidebar.write('mailto:matheusts@id.uff.br')
    st.sidebar.markdown(
        "[![GitHub](https://i.stack.imgur.com/tskMh.png) Github](https://github.com/iMatheusSilva)")
    st.sidebar.markdown(
        "[![Linkedin](https://i.stack.imgur.com/gVE0j.png) LinkedIn](https://www.linkedin.com/in/matheus-silva-8509b21a6/)")


if __name__ == "__main__":
    st.set_page_config(page_icon='dados/miner.png',
                       page_title="Price Miner", )
    header_intro()
    side_bar_credis()
    header_intro_2()

    user_input = st.text_input("Qual produto você deseja pesquisar?")
    user_email = st.text_input("Seu E-mail")
    if st.button("Pesquisar"):
        st.write("teste")
