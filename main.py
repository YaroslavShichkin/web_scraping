import bs4
import requests
import fake_headers as fk
import json

url = 'https://spb.hh.ru/search/vacancy?area=1&ored_clusters=true&text=Python+django+flask&order_by=publication_time'
headers = fk.Headers(browser='firefox', os='win').generate()
response = requests.get(url, headers=headers).text
soup = bs4.BeautifulSoup(response, 'lxml')
step = soup.find_all('div', class_='serp-item')
number = 1

result = {}
for vacancy in step:
    body_tag = vacancy.find('div', class_='vacancy-serp-item-body__main-info')
    a_tag = body_tag.find('a')
    link = a_tag['href']
    description_response = requests.get(link, headers=headers).text
    description_soup = bs4.BeautifulSoup(description_response, 'lxml')
    description = description_soup.find('div', class_="g-user-content").text

    salary = vacancy.find("span", class_="bloko-header-section-2")
    if salary == None:
        salary_el = "ВЕЛИКАЯ ТАЙНА (Зарплатная вилка не указана) :("
    else:
        salary_el = salary.text

    city_tag = body_tag.find('div', class_='vacancy-serp-item-company')
    city_tag2 = city_tag.find('div', class_='vacancy-serp-item__info')
    city_tag3 = city_tag2.find_all('div', class_='bloko-text')
    city = city_tag3[1].text
    company_a_tag = city_tag2.find('a')
    company = company_a_tag.text

    result[number]={'Ссылка на вакансию': link, 'Зп': salary_el, 'Компания': company, 'Город': city}
    number += 1

with open('vacancies.json', 'w') as f:
    json.dump(result, f)

with open('vacancies.json', 'r', encoding='utf-8') as f:
    text = json.load(f)
    print(text)