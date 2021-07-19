from os import read
import streamlit as st
from streamlit import caching
import pandas as pd
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
    user_email = st.text_input("Seu E-mail:")
    max_items = st.text_input("Quantidade de itens por loja: máx = 25")
    st.write("A quantidade final de itens pesquisados pode variar, pois são retirados itens aqueles não relevantes à busca.")
    encurtar = st.checkbox(
        "Encurtar links? (Aumenta razoávelmente o tempo de processamento)")
    if st.button("Pesquisar"):
        st.markdown(
            "<img src='https://i.ibb.co/v4ckXms/search.gif' width='20px'> Pesquisando...</img>", unsafe_allow_html=True)
        item = user_input
        max_items = 10
        pesquisa_preco = app.PriceMiner(item, max_items)
        produtos = pesquisa_preco.show_relevants(
            pesquisa_preco.scrap(), 1)
        st.markdown(
            "<img src='https://i.ibb.co/wYkr0SH/circles-menu-1.gif' width='15px'> Salvando arquivo...</img>", unsafe_allow_html=True)
        produtos.to_html(f"{item}.html", index=False)
        st.markdown(
            "<img src='https://i.ibb.co/z6gH7yQ/177-envelope-mail-send-outline.gif' width='20px'> Enviando e-mail...</img>", unsafe_allow_html=True)
        if app.send_email(user_email, user_input):
            st.markdown(
                "<img src='https://i.ibb.co/fMvwVnh/check-circle.gif' width='20px'> Email enviado com sucesso !</img>", unsafe_allow_html=True)
