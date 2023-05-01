from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
from datetime import date
from postgres import update_db
import time

useragent = UserAgent()

options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={useragent.random}")
options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)



today = date.today().strftime('%d-%m-%Y')


total_list =[['Vladimir Kim','Владимир Ким', 'kaz minerals limited',
              'nova resources b.v.',
              'Vostok Cooper B.V.', 'Vostok Holdings Ltd',
              'Folin Universal Trust','ТОО «Корпорация Казахмыс»'],
             ['Timur Kulibaev','Тимур Кулибаев','Joint Resources',
              'Кристалл Менеджмент', 'Каспий нефть', 'Шубарколь Премиум'],
             ['Dinara Kulibaeva','Динара Кулибаева','Холдинговая Группа Алмэкс',
              'Astana IT University','ШубаркольПремиум'],
             ['Vyacheslav Kim','Вячеслав Ким', 'Алсеко', 'Астана-ЕРЦ', 'Kaspi.kz'],
             ['Nurlan Smagulov','Нурлан Смагулов', 'Астана Групп', 'Астана Моторс',
              'ТРЦ MEGA', 'MEGA Alma-Ata', 'MEGA Park', 'MEGA Silk Way'],
             ['Alexandr Mashkevich','Александр Машкевич', 'Eurasian National Resources corporation',
             'Евразийская финансовая компания', 'Евразийский банк']]
parse_list = []
def get_source_html(url: str, name_2: str, asset: str):
    driver_service = Service(executable_path="/chromedriver.exe")
    driver = webdriver.Chrome(service=driver_service,
                              options=options)

    try:
        driver.get(url=url)
        time.sleep(3)
        blocks = driver.find_element(By.CLASS_NAME, "main-news")
        articles = blocks.find_elements(By.TAG_NAME, "article")
        for article in articles:
            title_link = article.find_element(By.CLASS_NAME, "main-news__name").get_attribute("href")
            title_name = article.find_element(By.CLASS_NAME, "main-news__name").get_attribute("text")
            date_article = article.find_element(By.CLASS_NAME, "information-article__date")
            normal_date_format = date_article.text[:10].replace(".","-")
            if normal_date_format == today:
                parse_list_1 = [title_link, title_name, normal_date_format]
                parse_list.append(parse_list_1)

        if parse_list == []:
            print("Новостей по запоросу", "'", asset,"'", "на дату:" , today, "не обнаружено")
        else:
            print("Новостей по запоросу", "'", asset, "'", "на дату:", today, "обнаружено:", len(parse_list))
    except Exception as ex:
        print(ex)
    try:
        list_text = []
        for i in range(len(parse_list)):
            driver.get(parse_list[i][0])
            time.sleep(2)
            date_article_1 = driver.find_element(By.XPATH, '//*[@id="main-container"]/main[1]/main/div[3]/article/header/div/time')
            normal_date_format_1 = date_article_1.text[:10].replace(".","-")
            if normal_date_format_1 != today:
                break
            rows_1 = driver.find_elements(By.CLASS_NAME, "longrid__body")
            rows_2 = driver.find_elements(By.CSS_SELECTOR,
                                          '#main-container > main:nth-child(1) > main > div.main__page > article > div:nth-child(3)')
            if rows_1 == [] and rows_2 != []:
                for row_2 in rows_2:
                    texts = row_2.find_elements(By.TAG_NAME, "p")
                    text = ''
                    for t in texts:
                        text += t.text
                    list_text.append(text)
            if rows_2 == [] and rows_1 != []:
                for row_1 in rows_1:
                    texts = row_1.find_elements(By.XPATH, '//*[@id="main-container"]/main/article/div[1]/div[1]/p')
                    text = ''
                    for t in texts:
                        text += t.text
                    list_text.append(text)
    except Exception as ex:
        print(ex)
    try:
        web_site = 'kapital.kz'
        name_table = name_2.lower().replace(" ", "_")
        for j in range(len(parse_list)):
            parse_list[j].append(list_text[j])
            parse_list[j].append(web_site)
            parse_list[j].append(asset.lower())
        update_db(parse_list, name_table=name_table)
        del parse_list[::]
    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()

def main():
    start = time.time()
    for i in range(len(total_list)):
        index_list = len(total_list[i])
        name_table = total_list[i][0]
        for index in range(index_list):
            get_source_html(url=f'https://kapital.kz/search/default/index?q={total_list[i][index]}&page=1&per-page=10',
                            name_2 = name_table, asset= total_list[i][index])
    end = time.time()
    total = round((end - start) / 60, 1)
    print('Время выполнения парса =', total, 'минут')

if __name__ == "__main__":
    main()