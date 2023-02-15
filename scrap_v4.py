import requests
from bs4 import BeautifulSoup
from pprint import pprint
import csv

def user_url(energie, marque, kms_max, kms_min, page, prix_max, prix_min, annees_max, annees_min) : 
    """
    Fonction qui affiche et renvoie l’url
    Grâce au format l’utilisateur peut choisir ce qu'il veut précisément sur le site
    """
    url_lacentrale = 'https://www.lacentrale.fr/listing?energies={energie_url}&makesModelsCommercialNames={marque_url}&mileageMax={kms_max_url}&mileageMin={kms_min_url}&page={page_url}&priceMax={prix_max_url}&priceMin={prix_min_url}&yearMax={annees_max_url}&yearMin={annees_min_url}'
    url = url_lacentrale.format(energie_url = energie, marque_url = marque, kms_max_url = kms_max, kms_min_url = kms_min, page_url = page, prix_max_url = prix_max, prix_min_url = prix_min, annees_max_url = annees_max, annees_min_url = annees_min)
    print(url)
    return url

    

def scrap_listing(url) :   
    """
    Fonction qui reprend l’url et renvois le code html
    """
    result = requests.get(url)
    return result.text


def scrap_card(html_page, csv_writer): 
    """
    Fonction qui permet d'obtenir toutes les informations des cartes des voitures
    Elle écrit également les informations dans le file.csv
    """
    soup = BeautifulSoup(html_page, "html.parser")  
    for card in soup.find_all("div", "searchCard"): 
        car_name = card.find('h3')  
        car_name_var = car_name.get_text()  
       
        
        i = 0
        p = ""
        car_model_var = ""
        while car_name_var[i]!= " ": #parcourt car_name_var avec des positions et s'arrête quand il y a un espace et renvois la marque
            p += car_name_var[i]    #ajoute dans p chaque lettre de car_name_var grace à la position dans car_name_var
            i +=1
        car_brand_var = p
        print(car_brand_var)
        for a in range(i+1, len(car_name_var)): 
            car_model_var += car_name_var[a]   
        print(car_model_var)
        card_motor = card.find('div', 'Text_Text_text Vehiculecard_Vehiculecard_subTitle Text_Text_body2') 
        car_motor_var = card_motor.get_text()
        print(car_motor_var)
        car_price = card.find('span','Text_Text_text Vehiculecard_Vehiculecard_price Text_Text_subtitle2') 
        car_price_var = car_price.get_text() 
        print(car_price_var)
        car_price_new = car_price_var.replace(" ", "").replace("€", '') 
        car_price_var = int(car_price_new)
        
        list = []
        for elem in card.find_all('div', 'Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2'):   
            list.append(elem.get_text())   
            print(elem.get_text()) 
        list[0] =int(list[0]) 
        car_price_new = list[1].replace(" ", "").replace("km", '').replace("\xa0", '') 
        list[1]= int(car_price_new)
        csv_writer.writerow([car_brand_var, car_model_var, car_motor_var, list[0], list[1], list[3], list[2], car_price_new])
            
    
def main() :
    """
    Fonction qui permet d'ouvrir le file csv et de le fermer
    Elle exécute toutes les autres fonctions: user_url/scrap_listing/scrap_card
    Grâce au while elle permet de parcourir 10 pages max
    """
    fd = open("file.csv", "w")
    csv_writer = csv.writer(fd)
    csv_writer.writerow(['brand', 'model', 'motor', 'year', 'mileage', 'fuel', 'type', 'price'])
    page = 1
    
    url_request = user_url('dies', 'RENAULT', '100000', '9000', str(page), '16600', '10300', '2016', '2014') 
    html_page = scrap_listing(url_request)
    soup = BeautifulSoup(html_page, "html.parser")
    nb_ads = soup.find('span', 'Text_Text_text Text_Text_headline2')
    nb_ads_text = int(nb_ads.get_text())
    #print(nb_ads_text)
    if nb_ads_text > 0 :
        while page != 10:
            url_request = user_url('dies', 'RENAULT', '100000', '9000', str(page), '16600', '10300', '2016', '2014') 
            html_page = scrap_listing(url_request)  
            scrap_card(html_page, csv_writer)    
            page +=1
    else :
       print(" erreur 0 annonces")
    fd.close()
main()