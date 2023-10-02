import os
import time
from datetime import datetime
import requests
from typing import Dict
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from bs4 import BeautifulSoup
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException

from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

options = webdriver.ChromeOptions()

options.add_argument("--headless")


def crawl_ipo38():
    browser = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=options
    )

    url = "http://www.ipo38.co.kr/ipo/index.htm?key=6"
    browser.get(url)
    time.sleep(2)

    html = browser.page_source
    browser.quit()

    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"summary": "공모주 청약일정"})

    header = []
    for th in table.find("thead").findAll("th"):
        header.append(th.text.strip())

    data = []
    for row in table.find("tbody").findAll("tr"):
        rowData = []
        for td in row.findAll("td"):
            rowData.append(td.text.strip())
        data.append(rowData)

    df = pd.DataFrame(data, columns=header)

    return df


def fetch_blog_content(link):
    browser = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=options
    )
    time.sleep(2)
    browser.get(link)
    time.sleep(1)
    browser.switch_to.frame("mainFrame")

    try:
        a = browser.find_element(By.CSS_SELECTOR, "div.se-main-container").text
    except NoSuchElementException:
        a = browser.find_element(By.CSS_SELECTOR, "div#content-area").text

    browser.quit()
    return a


def crawl_naver_blog(blog_links):
    contents = []

    with ThreadPoolExecutor() as executor:
        future_to_content = {
            executor.submit(fetch_blog_content, link): link for link in blog_links
        }

        for future in concurrent.futures.as_completed(future_to_content):
            link = future_to_content[future]
            try:
                contents.append(future.result())
            except Exception as e:
                print(f"Exception occurred while fetching blog at {link}: {e}")

    return contents
