import csv
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome()

# url = 'https://www.amazon.com'
# driver.get(url)

def get_url(search_term):
    """Generate a URL from a search term"""
    template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss'
    search_term = search_term.replace(' ', '+')
    return template.format(search_term)

url = get_url('basketball')
print(url)

driver.get(url)
