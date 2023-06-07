import json
import time

import bs4
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

DATA_URL = 'https://spb.hh.ru/search/vacancy?text=python%2C+django%2C+flask&salary=&area=1&area=2&ored_clusters=true'
def get_vacancy(url, num_of_pages):
  """Функция получения словаря с вакансиями"""
    vacancy = []
    salary_list = []
    link_list = []
    title_list = []
    company_list = []
    city_list = []
    for page in range(num_of_pages):
        headers = Headers(browser='firefox', os='win')
        headers_data = headers.generate()
        response = requests.get(f'{url}&page{page}', headers=headers_data).text
        time.sleep(0.2)
        # print(len(response))
        main_page = bs4.BeautifulSoup(response, 'lxml')
        link_main = main_page.find_all('div', class_='serp-item')
        for tag in link_main:
            link_find = tag.find('a')
            # print(link_find)
            link = link_find['href']
            link_list.append(link)
            salary = tag.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
            title = tag.find('h3').text
            title_list.append(title)
            if salary == None:
                salary_list.append('no salary declared')
                continue
            salary_list.append(salary.text.replace('\u202f', ''))
            company = tag.find('div', class_='bloko-text')
            company_list.append(company.text.replace('\xa0', ' '))
            city = tag.find('div', attrs={'data-qa': "vacancy-serp__vacancy-address"})
            city_list.append(list(city)[0])

        for a, b, c, d, e in zip(title_list, link_list, salary_list, company_list, city_list):
            vacancy.append({'vacancy': a, 'link': b, 'salary': c, 'company': d, 'city': e})
    return vacancy

def json_writes(link, pages):
    """Функция сериализации данных в json файл"""
    vacancy = get_vacancy(link, pages)
    with open('vacancy_list.json', 'w') as file:
        json.dump(vacancy, file)

if __name__ == '__main__':
    json_writes(DATA_URL, 5)
