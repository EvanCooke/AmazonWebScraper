import csv
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome()

url = 'https://www.amazon.com'
driver.get(url)