import requests
from bs4 import BeautifulSoup
import csv
import os


def parse():
    error_codes = []
    count = 0

    lst = input(
        'Введите данные в формате - "00-01429347, 00-01429349, 00-00526606..."(без кавычек и троеточия!): '
    ).split(', ')

    for item in lst:
        url = 'https://www.autorus.ru/catalog/akkumulyatory-dlya-moto/' + item

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
        }

        req = requests.get(url, headers=headers)
        src = req.text

        try:

            with open("autorus.html", "w") as file:
                file.write(src)

            soup = BeautifulSoup(src, "lxml")

            all_parameters = soup.find("section", id="specifications").find_all("tr")

            table_titles = ['Введенный код', ]
            table_values = [item, ]

            for i in all_parameters:
                table_titles.append(i.find("td").text)
                table_values.append(i.find("th").text)

            data = [table_titles, table_values]

            with open("autorus.csv", "a", encoding="cp1251") as file:
                writer = csv.writer(file)
                for line in data:
                    writer.writerow(line)

            if os.path.isfile('autorus.html'):
                os.remove('autorus.html')

            count += 1

        except AttributeError:
            error_codes.append(item)

    if len(error_codes) > 0:
        print(f'Обработан(о) {count} элемент(а/ов), не обработан(о) {len(error_codes)},'
              f' ошибочн(ый)ые коды: ' + ", ".join(map(str, error_codes)))
    else:
        print(f'Обработано {count} товар(a/ов)')

    parse()


parse()
