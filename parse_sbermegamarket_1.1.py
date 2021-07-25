import csv
import requests
from bs4 import BeautifulSoup
import os


headers = {
    "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
}


def write_product_specs(product_spec_urls):
    for product_spec_url in product_spec_urls:
        req = requests.get(product_spec_url, headers)
        src = req.text

        with open("product_page.html", "w", encoding="utf-8") as file:
            file.write(src)

        soup = BeautifulSoup(src, "lxml")
        # product_data = soup.find_all("table", class_="tbl-typical")
        product_data = soup.find_all("section", class_="prod--chars-group")
        product_name = soup.find("h1").text
        table_titles = ["Наименование товара", ]
        table_values = [product_name, ]

        for table in product_data:
            parameters_in_table = table.find_all("tr")
            for i in parameters_in_table:
                table_titles.append(i.find("td", class_="color-grey").text)
                value = i.find("div", class_="attribute-value")
                if value.find("div", class_="hint-icon"):
                    value.find("div", class_="hint-icon").decompose()
                table_values.append(value.text.strip())

        data = [table_titles, table_values]

        with open("sber_mega_market.csv", "a", encoding="cp1251") as file:
            writer = csv.writer(file)
            for line in data:
                writer.writerow(line)


def get_data():
    try:
        url = input(
            "Введите адрес раздела, например - https://sbermegamarket.ru/catalog/komponenty-sistem-obogreva/ : "
        )

        url_page1 = url + "page-1/"

        req = requests.get(url_page1, headers)
        src = req.text

        with open("section_page.html", "w", encoding="utf-8") as file:
            file.write(src)

        soup = BeautifulSoup(src, "lxml")

        try:
            iteration_count = soup.find("ul", class_="pagination__list").select('li')[-2].text.strip()
            print("Количество страниц в разделе: " + iteration_count)
        except:
            iteration_count = 1
            print("Количество страниц в разделе: 1")

        for i in range(1, int(iteration_count) + 1):
            products_path = url + f"page-{i}/"
            print()

            req = requests.get(products_path, headers)
            src = req.text

            with open("section_page.html", "w", encoding="utf-8") as file:
                file.write(src)

            soup = BeautifulSoup(src, "lxml")

            if soup.find_all("article", class_="card-prod"):
                articles = soup.find_all("article", class_="card-prod")
                product_spec_urls = []
                for article in articles:
                    product_spec_url = "https://sbermegamarket.ru" + \
                                       article.find("a", class_="card-prod--slider ddl_product_link").get("href")
                    product_spec_urls.append(product_spec_url)
                print(
                    "В процессе: " + products_path + " . Количество товаров на странице: " +
                    str(len(product_spec_urls))
                )

                write_product_specs(product_spec_urls)

            else:
                articles = soup.find("div", class_="catalog-listing__items").\
                    find_all("div", class_="catalog-item ddl_product")
                product_spec_urls = []
                for article in articles:
                    product_spec_url = "https://sbermegamarket.ru" + \
                                       article.find("div", class_="item-image").\
                                           find("a", class_="item-image-block ddl_product_link").get("href")
                    product_spec_urls.append(product_spec_url)
                print(
                    "В процессе: " + products_path + " . Количество товаров на странице: " +
                    str(len(product_spec_urls))
                )

                write_product_specs(product_spec_urls)

        if os.path.isfile('product_page.html'):
            os.remove('product_page.html')

        if os.path.isfile('section_page.html'):
            os.remove('section_page.html')

        print("Процесс завершен! Молодец, Саня, славно поработал!)")
        get_data()

    except:
        print(
            "Вероятно введен неверный адрес. Если вы уверены в корректности адреса, но все равно выходит ошибка, "
            "обратитесь к разработчику!"
        )
        get_data()


get_data()
