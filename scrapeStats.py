from selenium import webdriver
from time import sleep
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import html5lib
from gazpacho import Soup
import html
from contextlib import contextmanager
from lbcLinkGen import gen 

sourcecode_path = r"C:\Users\Théo\Documents\Python projects\LBC Scraper\sourcecode.html"
# Put you sourcecode.html file


nbPage=1

def dataframe_to_excel(dataframe,filePath):
    dataframe.to_excel(filePath, index=False)

def calculer_moyenne(dataframe):
    dataframe.iloc[:,2] = pd.to_numeric(dataframe.iloc[:,2], errors='coerce')
    moyenne = dataframe.iloc[:,2].mean()
    return moyenne

def set_nbPage(value):
    global nbPage  # Utilisez la variable globale pour mettre à jour la valeur de nbPage
    nbPage = value

def remove(string):
    return "".join(string.split())

def scrape_leboncoin(driver,nom,page,ville,prix_min,prix_max):
    global combined_df 
    combined_df = pd.DataFrame()

    #Ce qu'on veut scrap
    url=gen(nom,page,ville,prix_min,prix_max)

    #Précautions (attente + resize fenêtre)
    driver.set_window_size(1285, 1024)

    #Connection au site
    driver.get(url)
    sleep(0.2)

    #Prend un screen du site pour vérifier qu'il n'y a pas de captcha

    #Récupère le code source et le traite
    codePage=driver.page_source

    codePageTxt = open(sourcecode_path, "w", encoding="utf-8")
    for line in codePage:
        codePageTxt.write(line)

    #Récupère les infos importantes
    soup2 = BeautifulSoup(codePage, 'lxml')
    ls2=[]
    all_items2 = soup2.find_all("p")
    for item in all_items2:
        ls2.append(item.text)

    new_list = []
    temp_sublist = []

    #Trouve le nombre d'annonces et de pages
    global nbPage

    ls3=[]
    nbAnnonce = soup2.find("h2").text[:-8]
    nbAnnonce=remove(nbAnnonce)
    if int(nbAnnonce)>38:
        nbPage = int(nbAnnonce) // 38
    else:
        nbPage = 1
    if nbPage>100:
        nbPage=100
    
    set_nbPage(nbPage)

    #Trie les infos importantes
    for item in ls2:
        if ':' in item or "2023" in item:
            if temp_sublist:
                new_list.append(temp_sublist)
                temp_sublist = []
            temp_sublist.append(item)
        else:
            temp_sublist.append(item)

    if temp_sublist:
        new_list.append(temp_sublist)
    del new_list[-1]

    #Créé un data frame avec les infos
    df = pd.DataFrame(new_list)

    combined_df = pd.concat([combined_df,df],ignore_index = True)
    return combined_df