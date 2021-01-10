from bs4 import BeautifulSoup as bs
import requests
import db

'''
    "Должность": str(),
    "Фамилия": str(),
    "Имя": str(),
    "Отчество": str(),
    "Адрес": str(),
    "Телефон": str(),
    "Почта": str()
'''
db.collection.drop()


def rector_info(url):
    dic_name = {'Должность': '', "Фамилия": '', "Имя": '', "Отчество": ''}
    page_rec = requests.get(url,
                            headers={'user-agent': 'your-own-user-agent/0.0.1'}).text
    soup = bs(page_rec, 'html.parser')
    name = soup.find("div", class_='author-name h1').text.split(' ')
    dolj = soup.find('div', class_='author-dolj h3 mt-0 mb-4').text.split(',')[0]
    name.insert(0, dolj)
    i = 0
    for key in dic_name:
        dic_name[key] = name[i]
        i += 1

    dic_info = dic_name.copy()
    rector_info = soup.find('div', class_='mission mb-4')
    dic_info["Адрес"] = rector_info.find('div', class_='block-address').text
    dic_info['Телефон'] = rector_info.find('div', class_='block-phone').text.split(';')[0]
    dic_info['Почта'] = rector_info.find('div', class_='block-email').text
    return dic_info


recrtor = rector_info("https://www.dvfu.ru/about/rectorate/5520/")
prorecSTUDY = rector_info("https://www.dvfu.ru/about/rectorate/4915/")
prorecNAYKA = rector_info("https://www.dvfu.ru/about/rectorate/288/")
prorecRAZV = rector_info("https://www.dvfu.ru/about/rectorate/4925/")
prorecMEJD = rector_info("https://www.dvfu.ru/about/rectorate/4917/")
prorecOBWAK = rector_info("https://www.dvfu.ru/about/rectorate/32416/")
prorecNEWPROJ = rector_info("https://www.dvfu.ru/about/rectorate/4921/")
prorecKEPMYS = rector_info("https://www.dvfu.ru/about/rectorate/37260/")
prorecMED = rector_info("https://www.dvfu.ru/about/rectorate/4923/")
prorecEKONOM = rector_info("https://www.dvfu.ru/about/rectorate/33014/")
prorecBUG = rector_info("https://www.dvfu.ru/about/rectorate/26549/")
prorecANALIT = rector_info("https://www.dvfu.ru/about/rectorate/4913/")
parc = [recrtor, prorecSTUDY, prorecNAYKA, prorecRAZV, prorecMEJD, prorecOBWAK, prorecNEWPROJ, prorecKEPMYS]
parc1 = [prorecMED, prorecEKONOM, prorecBUG, prorecANALIT]
db.create_many(parc)
db.create_many(parc1)
