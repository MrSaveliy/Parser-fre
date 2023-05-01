import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
from postgres import record_db
import time

useragent = UserAgent()

options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={useragent.random}")
options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

parse_list = []
def get_source(url: str, name : str):
    driver_service = Service(executable_path="/chromedriver.exe")
    driver = webdriver.Chrome(service=driver_service,
                              options=options)
    try:
        driver.get(url=url)
        time.sleep(5)
        blocks = driver.find_element(By.CLASS_NAME, "main-news")
        articles = blocks.find_elements(By.TAG_NAME, "article")
        for article in articles:
            title_link = article.find_element(By.CLASS_NAME, "main-news__name").get_attribute("href")
            title_name = article.find_element(By.CLASS_NAME, "main-news__name").get_attribute("text")
            date_article = article.find_element(By.XPATH, '//*[@id="main-container"]/main/main/div[2]/div[3]'
                                                          '/article[1]/div[1]/div/time')
            normal_date_format = date_article.text[:10].replace(".", "-")

            parse_list_1 = [title_link, title_name, normal_date_format]
            parse_list.append(parse_list_1)
    except Exception as ex:
        print(ex, 'Проблема в гет сорс')
    try:
        list_text = []
        for i in range(len(parse_list)):
            driver.get(parse_list[i][0])
            time.sleep(5)
            rows_1 = driver.find_elements(By.CLASS_NAME, "longrid__body")
            rows_2 = driver.find_elements(By.CSS_SELECTOR, '#main-container > main:nth-child(1) > main > div.main__page > article > div:nth-child(3)')
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
        print(ex, 'Проблема в поиске текста')
    try:
        web_site = 'kapital.kz'
        name_2 = name.lower().replace("+", " ")
        for j in range(len(parse_list)):
            parse_list[j].append(list_text[j])
            parse_list[j].append(web_site)
            parse_list[j].append(name_2)
        record_db(parse_list)
        del parse_list[::]
    except Exception as ex:
        print(ex)

def get_source_nex(url: str):
    driver_service = Service(executable_path="/chromedriver.exe")
    driver = webdriver.Chrome(service=driver_service,
                                options=options)
    try:
        driver.get(url=url)
        nex = driver.find_element(By.CSS_SELECTOR, '#main-container > main > main > div.main__page > ul:nth-child(5) > li.next > a')
        if nex:
            return True
        else:
            return False
    except selenium.common.exceptions.NoSuchElementException:
         print('Парсинг закончен')
    finally:
        driver.close()
        driver.quit()
