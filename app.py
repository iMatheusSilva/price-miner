#!/usr/bin/python3
# coding: utf-8

from selenium.webdriver.common.keys import Keys
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
import matplotlib.pyplot as plt
from selenium import webdriver
from scipy import stats
from time import sleep
import pandas as pd
import numpy as np
import smtplib
import random
import sys
import pyshorteners
from email.message import EmailMessage


class PriceMiner:

    def __init__(self, item='', max_items='', headless=True):
        self.item = item
        self.max_items = max_items
        self.__browser_init(headless)

    def __setup(self):
        """
        Create or reset attributes used in scraping methods
        Parameters:
        - No parameters

        Return:
        - No return
        """
        self.__name_elements = []
        self.__price_elements = []
        self.__cents_elements = []
        self.__link_elements = []
        self.__name_values = []
        self.__price_values = []
        self.__link_values = []

    def __browser_init(self, headless):
        """
        This method is delegated to configure and start the browser that will serve to
        all the other intern methods.

        Parameters:
        - headless(boolean): Defines the browser visibility. The standard value is True, 
        it means that browser will work in background. If you want to see the browser working, 
        you have to set headless=False 

        Return:
        - browser(object)
        """
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        PROXY = proxies[0].get_address()
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy": PROXY,
            "ftpProxy": PROXY,
            "sslProxy": PROXY,

            "proxyType": "MANUAL",

        }
        if headless:
            options.add_argument("--headless")
        self.browser = webdriver.Chrome(options=options)

    def __do_search(self, url, input_element):
        """ 
        This method is destinated to make a simple search, given the url and the input field
        from any website.

        Paramaters:
        - url(string): Url link from the website 
        - input_element(string): XPATH value from the main search input field.

        Return:
        -boolean
        """
        try:
            self.browser.get(url)
            search_input = self.browser.find_element_by_xpath(input_element)
            search_input.send_keys(self.item)
            search_input.send_keys(Keys.ENTER)
            sleep(2)
            return True
        except:
            return False

    def show_relevants(self, df, precision):
        """
        Remove the dataframe outliers.  

        Parameters:
        - df(dataframe):
        - precision(float): 0..1 values, lower values means stronger filtering. 

        Return:
        - Filtered dataframe
        """
        return df[(np.abs(stats.zscore(df['Preço R$'])) < precision)]

    def scrap(self, sort=True, shortener=True):
        """
        This method performs a web-scrap search on the all avaliable websites .

        -Parameters:
        sort: boolean.

        -Return:
        Dataframe
        """
        df1 = self.shopee()
        df2 = self.mercadolivre()
        df3 = self.amazon()
        df4 = self.magalu()
        dataframes = [df1, df2, df3, df4]
        final_dataframe = pd.concat(dataframes, ignore_index=True)
        if shortener:
            s = pyshorteners.Shortener()
            for i in range(len(final_dataframe)):
                shortener_api = [s.tinyurl.short(final_dataframe['Link'].values[i]),
                                 s.isgd.short(final_dataframe['Link'].values[i]), s.qpsru.short(final_dataframe['Link'].values[i])]
                final_dataframe['Link'].values[i] = shortener_api[random.randint(
                    0, 2)]
        if sort:
            return final_dataframe.sort_values(by=['Preço R$'])
        else:
            return final_dataframe

    def amazon(self):
        """
        This method performs a web-scrap search on the Amazon website

        -Parameters:
        No external parameters needed.

        -Return:
        Dataframe
        """
        self.__setup()
        url = 'http://amazon.com.br'
        place = "Amazon"
        input_element = '//*[@id="twotabsearchtextbox"]'
        b = self.browser
        if self.__do_search(url, input_element):
            self.__name_elements = b.find_elements_by_class_name(
                'a-size-base-plus')
            self.__price_elements = b.find_elements_by_class_name(
                'a-price-whole')
            self.__cents_elements = b.find_elements_by_class_name(
                'a-price-fraction')
            self.__link_elements = b.find_elements_by_class_name(
                's-no-outline')
            for i in range(0, max_items):
                self.__name_values.append(self.__name_elements[i].text)
                self.__cents_elements[i] = int(
                    self.__cents_elements[i].text)/100
                self.__price_values.append(float(self.__price_elements[i].text.replace('.', ''))
                                           + self.__cents_elements[i])
                self.__link_values.append(
                    self.__link_elements[i].get_attribute('href'))
        data = {'Item': self.__name_values, 'Preço R$': self.__price_values,
                "Local": place, 'Link': self.__link_values}
        return pd.DataFrame(data)

    def mercadolivre(self):
        """
        This method performs a web-scrap search on the Mercado Livre website

        -Parameters:
        No external parameters needed.

        -Return:
        Dataframe
        """
        self.__setup()
        url = 'http://mercadolivre.com.br'
        place = "Mercado Livre"
        input_element = '/html/body/header/div/form/input'
        b = self.browser

        if self.__do_search(url, input_element):
            ml_items = b.find_elements_by_class_name('ui-search-layout__item')
            self.__name_elements = b.find_elements_by_class_name(
                'ui-search-item__title')
            self.__price_elements = b.find_elements_by_class_name(
                'price-tag-fraction')
            self.__price_elements = self.__price_elements[::2]
            for i in range(0, len(ml_items)):
                self.__link_elements.append(
                    ml_items[i].find_element_by_class_name('ui-search-link'))
            for i in range(0, max_items):
                self.__name_values.append(self.__name_elements[i].text)
                self.__link_values.append(
                    self.__link_elements[i].get_attribute('href'))
                self.__price_values.append(
                    float(self.__price_elements[i].text.replace('.', '')))
            data = {'Item': self.__name_values, 'Preço R$': self.__price_values,
                    "Local": place, "Link": self.__link_values}
            return pd.DataFrame(data)
        else:
            return False

    def magalu(self):
        """
        This method performs a web-scrap search on the Magazine Luiza website

        -Parameters:
        No external parameters needed.

        -Return:
        Dataframe
        """
        self.__setup()
        url = 'https://www.magazineluiza.com.br'
        place = 'Magazine Luiza'
        input_element = '//*[@id="inpHeaderSearch"]'
        b = self.browser

        if self.__do_search(url, input_element):
            self.__name_elements = b.find_elements_by_class_name(
                'productTitle')
            self.__price_elements = b.find_elements_by_class_name('price')
            self.__link_elements = b.find_elements_by_class_name('product-li')
            del self.__price_elements[0:4]
            for i in range(0, max_items):
                self.__name_values.append(self.__name_elements[i].text)
                aux_price = self.__price_elements[i].text.replace(
                    'à vista', '').replace('R$ ', '').replace(',', '.')
                if aux_price.count('.') > 1:
                    aux_price = aux_price.replace(
                        '.', '', aux_price.count('.')-1)
                self.__price_values.append(float(aux_price))
                self.__link_values.append(
                    self.__link_elements[i].get_attribute('href'))
            data = {'Item': self.__name_values, 'Preço R$': self.__price_values,
                    "Local": place, 'Link': self.__link_values}
            return pd.DataFrame(data)

    def shopee(self):
        """
        This method performs a web-scrap search on the Shopee website

        -Parameters:
        No external parameters needed.

        -Return:
        Dataframe
        """

        self.__setup()
        url = 'https://shopee.com.br'
        place = 'Shopee'
        input_element = '//*[@id="main"]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div/form/input'
        b = self.browser
        if self.__do_search(url, input_element):
            sleep(2)
            for i in range(1, self.max_items+1):
                self.__name_elements.append(b.find_element_by_xpath(
                    f'/html/body/div[1]/div/div[3]/div/div[2]/div/div[2]/div[{i}]/a/div/div/div[2]/div[1]/div[1]/div'))
                self.__price_elements.append(b.find_element_by_xpath(
                    f'/html/body/div[1]/div/div[3]/div/div[2]/div/div[2]/div[{i}]/a/div/div/div[2]/div[2]/div/span[2]'))
                self.__link_elements.append(b.find_element_by_xpath(
                    f'/html/body/div[1]/div/div[3]/div/div[2]/div/div[2]/div[{i}]/a'))

            for i in range(0, max_items):
                self.__name_values.append(self.__name_elements[i].text)
                aux_price = self.__price_elements[i].text.replace(
                    '.', '').replace(',', '.')
                self.__price_values.append(float(aux_price))
                self.__link_values.append(
                    self.__link_elements[i].get_attribute('href'))

            data = {'Item': self.__name_values, 'Preço R$': self.__price_values,
                    "Local": place, 'Link': self.__link_values}
            return pd.DataFrame(data)


def send_email():
    try:
        email_from = "kronenautobots@gmail.com"
        email_to = sys.argv[2]
        smtp = "smtp.gmail.com"
        excel_file = f"{item}.html"
        msg = EmailMessage()
        msg['Subject'] = f"Resultado de Pesquisa por: {item}"
        msg['From'] = email_from
        msg['To'] = email_to
        msg.set_content(
            f"""
            Segue em anexo os resultados da pesquisa pelo produto: {item} nos formatos solicitados. 
            """)

        with open(excel_file, 'rb') as f:
            file_data = f.read()

        msg.add_attachment(file_data, maintype="application",
                           subtype="html", filename=excel_file)
        server = smtplib.SMTP(smtp, 587)
        server.starttls()
        server.login(email_from, open('config.txt').read().strip())
        server.send_message(msg)
        server.quit()
        print('Email-enviado com sucesso')
    except:
        print('Erro ao enviar e-mail')


if __name__ == '__main__':

    req_proxy = RequestProxy()
    proxies = req_proxy.get_proxy_list()
    item = sys.argv[1]
    max_items = 10
    pesquisa_preco = PriceMiner(item, max_items)
    produtos = pesquisa_preco.show_relevants(pesquisa_preco.scrap(), 1)
    produtos.to_html(f"{item}.html", index=False)
    send_email()
    pesquisa_preco.browser.quit()
