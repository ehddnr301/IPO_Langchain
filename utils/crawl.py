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
from selenium.common.exceptions import NoSuchElementException

load_dotenv()

# 크롤링 옵션 생성
options = webdriver.ChromeOptions()
# 백그라운드 실행 옵션 추가
options.headless = True


def crawl_ipo38():
    # 웹 페이지 접속
    browser = webdriver.Chrome(options=options)
    url = "http://www.ipo38.co.kr/ipo/index.htm?key=6"  # 실제 테이블이 있는 웹 페이지 URL로 변경해주세요.
    browser.get(url)
    time.sleep(2)  # 페이지가 로드되기를 기다립니다. 필요에 따라 시간을 조정할 수 있습니다.

    # HTML 가져오기
    html = browser.page_source
    browser.quit()  # 브라우저 종료

    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"summary": "공모주 청약일정"})

    # 헤더 추출
    header = []
    for th in table.find("thead").findAll("th"):
        header.append(th.text.strip())

    # 데이터 추출
    data = []
    for row in table.find("tbody").findAll("tr"):
        rowData = []
        for td in row.findAll("td"):
            rowData.append(td.text.strip())
        data.append(rowData)

    # DataFrame으로 변환
    df = pd.DataFrame(data, columns=header)

    return df


def fetch_blog_content(link):
    browser = webdriver.Chrome(options=options)
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
