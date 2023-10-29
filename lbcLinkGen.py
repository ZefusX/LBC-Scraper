def gen(nom,page,ville,prix_min,prix_max):
    """nom -> Pas obligatoire
    page -> Pas obligatoire, page > page présent LBC impossible
    ville -> Ville ou code postal   """


    lien="https://www.leboncoin.fr"
    if nom != None:
        lien+="/recherche?text="+str(nom)
    if page != None:
        lien+="&page="+str(page)
    if ville != None:
        lien+="&locations="+str(ville)

    if prix_min != None and prix_max == None:
        lien+="&price="+str(prix_min)+"-max"
    elif prix_min == None and prix_max!= None:
        lien+="&price=min-"+str(prix_max)
    elif prix_min != None and prix_max != None:
        lien+="&price="+str(prix_min)+"-"+str(prix_max)

    return lien
