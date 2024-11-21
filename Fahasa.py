import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,  TimeoutException, StaleElementReferenceException
import time
from tqdm import tqdm
import json
import re
import pymongo
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def initialize_mongodb():
    #econnect = str(os.environ['Mongo_HOST'])
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
    #client = pymongo.MongoClient('mongodb://'+econnect+':27017')
    db = client['Fahasa']
    collection = db['Fahasa']
    return collection

def get_course_links(driver, pages):
    with open('Fahasa.txt', 'a') as file:
        for i in tqdm(range(1, pages + 1), desc="Pages Are Loading"):
            url = f"https://www.fahasa.com/sach-trong-nuoc.html?order=num_orders&limit=48&p={i}&stages=1176195_1176194_1176193_1177707&reading_level=1176192_1176181_1176184_1176190_1176188_1176191_1176187_1176185_1176189_1176186_1176183_1176182"
            driver.get(url)
            
            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//*[@class="product-name-no-ellipsis p-name-list"]/a')) 
                )
            except TimeoutException:
                print(f"Error! Page {i} not recognized.")
                continue

            elements = driver.find_elements(By.XPATH, '//*[@class="product-name-no-ellipsis p-name-list"]/a')
            for element in elements:
                try:
                    link = element.get_attribute("href")
                    if 'https://www.fahasa.com' not in link:
                        link = 'https://www.fahasa.com' + link
                    file.write(link + '\n')
                except StaleElementReferenceException:
                    print(f"Page {i} does not exist!")
                    continue

def extract_course_data(driver, links):
    list_title = []
    list_code = []
    list_author = []
    list_publisher = []
    list_supplier = []
    list_yearpublish = []
    list_grade = []
    list_level = []
    list_price = []
    list_sold = []
    list_vote = []
    list_rate = []
    list_describe = []


    for link in tqdm(links, desc="Links Are Loading"):
        print(f"Link: {link}")
        driver.get(link)
        time.sleep(2)

        try:
            title = driver.find_element(By.XPATH, '//*[@id="product_view_kasitoo"]/div/div[2]/div[1]/div[2]/h1').text
        except NoSuchElementException:
            title = None
        print(f"Title: {title}")

        try:
            code = driver.find_element(By.XPATH, '//*[@id="product_view_info"]/div[2]/div[1]/table[1]/tbody/tr[1]/td/div').text
        except NoSuchElementException:
            code = None
        print(f"Code: {code}")
        
        try:
            author = driver.find_element(By.XPATH, '//*[@id="product_view_info"]/div[2]/div[1]/table[1]/tbody/tr[5]/td/div').text
        except NoSuchElementException:
            author = None
        print(f"Author: {author}")
                
        try:
            publisher = driver.find_element(By.XPATH, '//*[@id="product_view_info"]/div[2]/div[1]/table[1]/tbody/tr[6]/td/div').text
        except NoSuchElementException:
            publisher = None
        print(f"Publisher: {publisher}")
        
        try:
            supplier = driver.find_element(By.XPATH, '//*[@id="product_view_info"]/div[2]/div[1]/table[1]/tbody/tr[4]/td/div/a').text
        except NoSuchElementException:
            supplier = None
        print(f"Supplier: {supplier}")

        try:
            level = driver.find_element(By.XPATH, '//*[@id="product_view_info"]/div[2]/div[1]/table[1]/tbody/tr[2]/td/div').text
        except NoSuchElementException:
            level = None
        print(f"Level: {level}")

        try:
            grade = driver.find_element(By.XPATH, '//*[@id="product_view_info"]/div[2]/div[1]/table[1]/tbody/tr[3]/td/div').text
        except NoSuchElementException:
            grade = None
        print(f"Grade: {grade}")
                
        try:
            yearpublish = driver.find_element(By.XPATH, '//*[@id="product_view_info"]/div[2]/div[1]/table[1]/tbody/tr[7]/td/div').text
        except NoSuchElementException:
            yearpublish = None
        print(f"YearPublish: {yearpublish}")
        
        try:
            price = driver.find_element(By.XPATH, '//*[@id="catalog-product-details-price"]/div/p[1]').text.replace('.', '')
        except NoSuchElementException:
            price = None
        print(f"Price: {price}")
        
        try:
            sold = driver.find_element(By.XPATH, '//*[@id="product_view_kasitoo"]/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/div').text
        except NoSuchElementException:
            sold = None
        print(f"Sold: {sold}")
        
        try:
            vote = driver.find_element(By.XPATH, '//*[@id="product_view_kasitoo"]/div/div[2]/div[1]/div[2]/div[2]/div/div[1]/div/table[1]/tbody/tr/td[2]/p/a').text
        except NoSuchElementException:
            vote = None
        print(f"Vote: {vote}")
        
        try:
            rate = driver.find_element(By.XPATH, '//*[@id="product_view_tab_content_review"]/div[1]/div/div[1]/div[1]/div/div[1]').text
        except NoSuchElementException:
            rate = None
        print(f"Rate: {rate}")

        try:
            describe = driver.find_element(By.XPATH, '//*[@id="desc_content"]').text.replace('\n', ' ')
            describe = describe[:1000]
        except NoSuchElementException:
            describe = None
        print(f"Describe: {describe}")

        list_title.append(title)
        list_code.append(code)
        list_author.append(author)
        list_publisher.append(publisher)
        list_supplier.append(supplier)
        list_level.append(level)
        list_grade.append(grade)
        list_yearpublish.append(yearpublish)
        list_price.append(price)
        list_sold.append(sold)
        list_vote.append(vote)
        list_rate.append(rate)
        list_describe.append(describe)

    return {
        'Link': links,
        'Title': list_title,
        'Code': list_code,
        'Author': list_author,
        'Publisher': list_publisher,
        'Supplier': list_supplier,
        'Level': list_level,
        'Grade': list_grade,
        'YearPublish': list_yearpublish,
        'Price': list_price,
        'Sold': list_sold,
        'Vote': list_vote,
        'Rate': list_rate,
        'Describe': list_describe
    }

def clean_string(value):
    if isinstance(value, str):
        return ''.join(c for c in value if c.isprintable())
    return value

def save_to_csv(data, filename='Fahasa.csv'):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"The data has been stored in a file '{filename}'")

def save_to_json(data, filename='Fahasa.json'):
    df = pd.DataFrame(data)
    with open(filename, 'a', encoding='utf-8') as file:
        json.dump(df.to_dict(orient='records'), file, ensure_ascii=False, indent=4)
    print(f"The data has been stored in a file '{filename}'")

def save_to_mongodb(data, collection):
    df = pd.DataFrame(data)
    json_data = df.to_json(orient='records', force_ascii=False)
    records = json.loads(json_data)
    collection.insert_many(records)
    print(f"The data has been stored in mongosh")

def main():
    driver = initialize_driver()
    collection = initialize_mongodb()

    try:
        pages = 42
        get_course_links(driver, pages)
        with open('Fahasa.txt', 'r', encoding='utf-8') as file:
            links = file.read().splitlines()
        data = extract_course_data(driver, links)
        save_to_csv(data)
        save_to_json(data)
        save_to_mongodb(data, collection)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
