from bs4 import BeautifulSoup 
from requests import get
import sqlite3
from sys import argv
#zamiana ceny na liczbe zmiennoprzecinkową (tekst na float)
def parse_price(price):
    return float(price.replace(' ',  '').replace('zł', '').replace(',','.'))
#baza danych
db = sqlite3.connect('dane.db')
cursor = db.cursor()
#utworzenie tabeli (python web_scraper.py setup)
if len(argv) > 1 and argv[1] == 'setup':
    cursor.execute('''CREATE TABLE offers (name TEXT, price REAL, city TEXT)''')
    quit
#url strony, którą będziemy przeszukiwać
url = "https://www.olx.pl/motoryzacja/samochody/podkarpackie/?search%5Bfilter_enum_petrol%5D%5B0%5D=diesel" 
#pobieranie zawartości html strony w zmiennej url
page = get(url)
#przypisanie zawartosci strony do zmiennej wykorzystujac bs
bs = BeautifulSoup(page.content, "html.parser") 
#pobranie wszystkich divów o class offer-wrapper
for offer in bs.find_all('div', class_ = "offer-wrapper"):
    footer = offer.find('td', class_ = "bottom-cell")
    #pobranie class zawierające nazwy miejscowości z formatowaniem na samo wyświetlenie nazwy
    location = footer.find('small', class_ = "breadcrumb").get_text().strip() 
    #pobranie class zawierające tytuły ogłoszeń z formatowaniem na samo wyświetlenie nazwy
    title = offer.find('strong').get_text().strip()
    #pobranie class zawierające ceny ogłoszeń z formatowaniem na samo wyświetlenie nazwy
    price = parse_price(offer.find('p', class_="price").get_text().strip())    
    #wyświetlenie ogłoszeń (Lokalizacja Tytuł_ogłoszenia Cena)
    print(location, title, price)
    #uzupełnienie tabeli bazy danych
    cursor.execute('INSERT INTO offers VALUES (?,?,?)', (title,price,location))
    db.commit()
db.close()
