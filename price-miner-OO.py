#!/usr/bin/env python
# coding: utf-8

# In[171]:


from selenium.webdriver.common.keys import Keys
import matplotlib.pyplot as plt
from selenium import webdriver
from scipy import stats
from time import sleep
import pandas as pd  
import numpy as np


# In[172]:


class PriceMiner:
    
    def __init__(self, item='', max_items='', headless=True):
        self.item = item
        self.max_items = max_items 
        self.browser_init(headless)
        
    def var_reset(self):
        """
        Create or reset global variables used in scraping methods
        Parameters:
        - No parameters
        
        Return:
        - No return
        
        """
        self.__name_elements  = []
        self.__price_elements = []
        self.__cents_elements = []
        self.__link_elements = []
        self.name_values  = []
        self.price_values = []
        self.link_values = []
        
    def browser_init(self, headless):
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
        options.add_argument("--start-maximized")
        if headless:
            options.add_argument("--headless")
        self.browser = webdriver.Chrome(options=options)
    
    def do_search(self, url, input_element):
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
            sleep(1)
            return True
        except:
            return False
        
        
    def show_relevants(self, df, precision):
        """
        Remove the dataframe outliers.  
        
        Parameters:
        - df(dataframe):
        - precision(float):
        
        Return:
        - 
        """
        return df[(np.abs(stats.zscore(df['Preço R$'])) < precision)]  
        
        
    def amazon(self):
        """
        
        
        """
        self.var_reset()
        url = 'http://amazon.com.br'
        place = "Amazon"
        input_element = '//*[@id="twotabsearchtextbox"]'
        b = self.browser
        if self.do_search(url, input_element):
            self.__name_elements  = b.find_elements_by_class_name('a-size-base-plus')
            self.__price_elements = b.find_elements_by_class_name('a-price-whole')
            self.__cents_elements = b.find_elements_by_class_name('a-price-fraction')
            self.__link_elements  = b.find_elements_by_class_name('s-no-outline')
            for i in range(0, max_items):
                self.name_values.append(self.__name_elements[i].text)
                self.__cents_elements[i] = int(self.__cents_elements[i].text)/100
                self.price_values.append(float(self.__price_elements[i].text.replace('.',''))
                                         + self.__cents_elements[i])
                self.link_values.append(self.__link_elements[i].get_attribute('href'))
            data = {'Item':self.name_values, 'Preço R$': self.price_values, "Local": place, 'Link': self.link_values}
        return pd.DataFrame(data, index=list(range(max_items)))
    
    def mercadolivre(self):
        """
        
        """
        self.var_reset()
        url = 'http://mercadolivre.com.br'
        place = "Mercado Livre"
        input_element = '/html/body/header/div/form/input'
        b = self.browser

        if self.do_search(url, input_element):  
            ml_items = b.find_elements_by_class_name('ui-search-layout__item') 
            self.__name_elements  = b.find_elements_by_class_name('ui-search-item__title')
            self.__price_elements = b.find_elements_by_class_name('price-tag-fraction')
            self.__price_elements = self.__price_elements[::2]
            for i in range(0, len(ml_items)):
                self.__link_elements.append(ml_items[i].find_element_by_class_name('ui-search-link')) 
            for i in range(0, max_items):
                self.name_values.append(self.__name_elements[i].text)
                self.link_values.append(self.__link_elements[i].get_attribute('href'))
                self.price_values.append(float(self.__price_elements[i].text.replace('.','')))
            data = {'Item':self.name_values, 'Preço R$': self.price_values, "Local": place, "Link": self.link_values}        
            return pd.DataFrame(data, index=list(range(max_items, max_items*2)))
        else:
            return False
    
    def magalu(self):
        """
        
        """
        self.var_reset()
        url   = 'https://www.magazineluiza.com.br'
        place = 'Magazine Luiza'
        input_element = '//*[@id="inpHeaderSearch"]'
        b = self.browser
        
        if self.do_search(url, input_element):
            self.__name_elements  = b.find_elements_by_class_name('productTitle')
            self.__price_elements = b.find_elements_by_class_name('price')
            self.__link_elements  = b.find_elements_by_class_name('product-li')
            del self.__price_elements[0:4]  
            for i in range(0, max_items):
                self.name_values.append(self.__name_elements[i].text)
                aux_price = self.__price_elements[i].text.replace('à vista', '').replace('R$ ', '').replace(',','.')
                if aux_price.count('.') > 1:
                    aux_price = aux_price.replace('.','', aux_price.count('.')-1)
                self.price_values.append(float(aux_price))
                self.link_values.append(self.__link_elements[i].get_attribute('href'))
            data = {'Item':self.name_values, 'Preço R$': self.price_values, "Local": place, 'Link': self.link_values}
        return pd.DataFrame(data, index=list(range(max_items*2, max_items*3)))


# In[ ]:





# In[173]:


if __name__ == '__main__':
    item = 'Memória Ram DDR4'
    max_items = 10        
    x = PriceMiner(item, max_items, headless=False)
    magalu = x.magalu()
    display(magalu)
    x.browser.close()
    #amazon = x.amazon()
    #mercadolivre = x.mercadolivre()
    #display(amazon)
    #display(mercadolivre)
    #display(x.show_relevants(amazon, 1))
    #display(x.show_relevants(mercadolivre, 1))
 

