#!/usr/bin/env python
# coding: utf-8

# In[68]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd  

def browser_init():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    browser = webdriver.Chrome(options=options)
    browser.minimize_window()
    return browser 


def do_search(browser, url, input_element, item):
    browser.get(url)
    search_input = browser.find_element_by_xpath(input_element)
    search_input.send_keys(item)
    search_input.send_keys(Keys.ENTER)
    sleep(1)
    
    
def mercadolivre(item, max_items):
    filtered_prices, names, formatted_prices, filtered_links, place = [], [], [], [], [] 
    url = 'http://mercadolivre.com.br'
    aux_links = []
    aux = ''
    input_element = '/html/body/header/div/form/input'
    browser = browser_init()
    do_search(browser, url, input_element, item)
    #for i in range(2, 0, -1):
    #    browser.find_element_by_xpath('//*[@id="root-app"]/div/div[1]/section/div[1]/div/div/div[2]/div[1]/div/div/button').click()
    #   browser.find_element_by_xpath(f'//*[@id="root-app"]/div/div[1]/section/div[1]/div/div/div[2]/div[1]/div/div/div/ul/li[{i}]').click() 
    name_elements  = browser.find_elements_by_class_name('ui-search-item__title')
    price_elements = browser.find_elements_by_class_name('price-tag-fraction')
    link_elements  = browser.find_elements_by_class_name('ui-search-link')
    place = "Mercado Livre"
    filtered_prices = price_elements[::2] 
    for i in range(0, len(link_elements)):
        aux = link_elements[i].get_attribute('href')
        if (aux is not None) and ("https://produto" in aux):
            aux_links.append(aux)
            
    aux_links =  aux_links[::2]
    for i in range(0, max_items):
        names.append(name_elements[i].text)
        formatted_prices.append(int(filtered_prices[i].text.replace('.','')))
        filtered_links.append(aux_links[i])
        
    data = {'Item':names, 'Preço R$': formatted_prices, "Local": place, "Link": filtered_links}        
    browser.close()
    return pd.DataFrame(data, index=list(range(max_items, max_items*2)))


def kabum(item, max_items):
    names, formatted_prices, filtered_links = [], [], []
    url = 'http://kabum.com.br'
    input_element = '/html/body/div[2]/header/div[1]/div/div[4]/form/input[1]'
    browser = browser_init()
    do_search(browser, url, input_element, item)
    name_elements = browser.find_elements_by_class_name('item-nome')
    price_elements = browser.find_elements_by_class_name('sc-fznWqX')
    for i in range(0, max_items):
        names.append(name_elements[i].text)
        formatted_prices.append(price_elements[i].texttext.replace('.',''))
        filtered_links.append(name_elements[i].get_attribute('href'))    
    data = {'Item':names, 'Preço': formatted_prices, 'Links': filtered_links}  
    browser.close()
    return pd.DataFrame(data)

    
def amazon(item, max_items):
    names, formatted_prices, link_elements ,filtered_links = [], [], [], []
    url = 'http://amazon.com.br'
    input_element = '//*[@id="twotabsearchtextbox"]'
    browser = browser_init()
    do_search(browser, url, input_element, item)    
    name_elements = browser.find_elements_by_class_name('a-size-base-plus')
    price_elements = browser.find_elements_by_class_name('a-price-whole')
    cents_elements = browser.find_elements_by_class_name('a-price-fraction')
    link_elements = browser.find_elements_by_class_name('s-no-outline')
    place = "Amazon"
    for i in range(0, max_items):
        names.append(name_elements[i].text)
        cents_elements[i] = int(cents_elements[i].text)/100
        formatted_prices.append(int(price_elements[i].text.replace('.','')) + cents_elements[i])
        filtered_links.append(link_elements[i].get_attribute('href'))
    data = {'Item':names, 'Preço R$': formatted_prices, "Local": place, 'Link': filtered_links}
    browser.close()
    return pd.DataFrame(data, index=list(range(max_items)))


item = 'Placa mãe asus TUF'
max_items = 5

#display(kabum(item, max_items))

df_amazon = amazon(item, max_items)
df_mercadolivre = mercadolivre(item, max_items)
frames = [df_amazon, df_mercadolivre]
final_table = pd.concat(frames)
display(final_table.sort_values(by=['Preço R$']))

final_table.to_excel('pesquisa.xlsx')


# In[ ]:





# In[ ]:




