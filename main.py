import pandas as pd
from gazpacho import Soup
import html
from lbcLinkGen import gen 
from emailsend import send_email
from scrapeStats import *

#Chemins d'accès FF. Modify with your FF driver/profile path
cheminDriver=r"C:\Users\Théo\Documents\Python projects\LBC Scraper\geckodriver.exe"
cheminProfil=r"C:\Users\Théo\AppData\Roaming\Mozilla\Firefox\Profiles\f8fiz4b9.default-release"

chemin_stat_fichier = r"C:\Users\Théo\Documents\Python projects\LBC Scraper\leboncoin_data_func.txt"
chemin_excel = r"C:\Users\Théo\Documents\Python projects\LBC Scraper\leboncoin_data.xlsx"
#Démarre Firefox en headless
ffOptions = Options()
ffOptions.headless = True

#Désactive des paramètres cramés par les antibots
profile = webdriver.FirefoxProfile(cheminProfil)
profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False)
profile.update_preferences()

#Initialise FF
driver = webdriver.Firefox(options=ffOptions, firefox_profile=profile)




if __name__ == "__main__":
    # Option de scrap : # Change with what you want to scrap
    objet=str(input("Que voulez vous acheter ? / What do you want to buy : \n")) # Put here what you want to scrap
    page_numbers_to_scrape=list(range(1,2))
    ville=None
    prix_min=None
    prix_max=None
    envoiMail=False
    envoiDiscord=False
    statExcel=True
    statFichierText = False

    combined_df = pd.DataFrame()
    dfTotal = pd.DataFrame()
    for page_number in page_numbers_to_scrape:
        combined_df = scrape_leboncoin(driver,objet,page_number,ville,prix_min,prix_max)
        dfTotal = pd.concat([dfTotal,combined_df],ignore_index = True)
        print("Page", page_number, "scrapé")

    driver.quit()

    #Enlève les lettres présentes dans la colonne des prix
    dfTotal.iloc[:,2] = dfTotal.iloc[:,2].apply(lambda x: ''.join(filter(str.isdigit, str(x))))

    # Stats
    resultatMoyen = calculer_moyenne(dfTotal)
    resultatMin = dfTotal.iloc[:,2].min()
    resultatMax = dfTotal.iloc[:,2].max()
    print("Moyenne de l'objet", resultatMoyen)
    print("Prix minimum", resultatMin)
    print("Prix maximum", resultatMax)


    # ----------------------------------------------------------------------------------------------------------------
    if statFichierText == True:
        with open(chemin_stat_fichier, "w") as f:
            f.write(f"Moyenne de l'objet {resultatMoyen} \n")
            f.write(f"Prix minimum {resultatMin} \n")
            f.write(f"Prix maximum {resultatMax} \n")

    if statExcel == True:
        dataframe_to_excel(dfTotal,chemin_excel)
        print("Excel créé")

    if envoiMail == True: # Change if you want to have an email of the results
        email_sender=""
        email_password=""
        email_receiver=""

        subject = "Prix leboncoin"+" "+str(objet)
        body = f"""Moyenne de l'objet = {resultatMoyen} \n
        Prix minimum = {resultatMin} \n
        Prix maximum = {resultatMax} \n
        """
        send_email(email_sender,email_password,email_receiver,subject,body)
        print("Mail envoyé")
