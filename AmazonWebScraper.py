# import csv
# from bs4 import BeautifulSoup
# from selenium import webdriver
#
# driver = webdriver.Chrome()
#
# # url = 'https://www.amazon.com'
# # driver.get(url)
#
# def get_url(search_term):
#     """Generate a URL from a search term"""
#     template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss'
#     search_term = search_term.replace(' ', '+')
#     return template.format(search_term)
#
#
# url = get_url('urltrawide monitor')
# # print(url)
#
# driver.get(url)
#
# # Extract the collection
#
# # soup object which retrieves html contents and uses parser
# # to parse it
# soup = BeautifulSoup(driver.page_source, 'html.parser')
#
# # use soup object to extract all elements in html contents with data-component-type of s-search-result
# results = soup.find_all('div', {'data-component-type': 's-search-result'})
# print(len(results))
#
# # Prototype the record
#
# item = results[0]
# atag = item.h2.a
# description = atag.text.strip()
# url = 'https://www.amazon.com' + atag.get('href')
#
# price_parent = item.find('span', 'a-price')
# price = price_parent.find('span', 'a-offscreen').text
#
# # get i tag found from first item's html contents in results
# rating = item.i.text
#
# review_count = item.find('span', {'class': 'a-size-base', 'class': 's-underline-text'}).text
#
# print(review_count)
#
#
# # Generalize the pattern
# def extract_record(item):
#     """Extract and return data from a single record"""
#
#     # description and url
#     atag = item.h2.a
#     description = atag.text.strip()
#     url = 'https://www.amazon.com' + atag.get('href')
#
#     try:
#         # price
#         price_parent = item.find('span', 'a-price')
#         price = price_parent.find('span', 'a-offscreen').text
#     except AttributeError:
#         return
#
#     try:
#         # rank and rating
#         # get i tag found from first item's html contents in results
#         rating = item.i.text
#         review_count = item.find('span', {'class': 'a-size-base', 'class': 's-underline-text'}).text
#     except AttributeError:
#         rating = ''
#         review_count = ''
#
#     results = (description, price, rating, review_count, url)
#
#     return results
#
#
# records = []
# results = soup.find_all('div', {'data-component-type': 's-search-result'})
#
# for item in results:
#     record = extract_record(item)
#     if record:  # if record has something in it, add it to list
#         records.append(record)
#
# # print prices in records so far
# for row in records:
#     print(row[1])
#
# # Getting the next page
# def get_url(search_term):
#     """Generate a URL from a search term"""
#     template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss'
#     search_term = search_term.replace(' ', '+')
#
#     # add term query to URL
#     url = template.format(search_term)
#
#     #add page query to placeholder
#     url += '&page{}'
#
#     return url

# Putting it all together

import csv
from bs4 import BeautifulSoup
from selenium import webdriver


# Getting the next page
def get_url(search_term):
    """Generate a URL from a search term"""
    template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss'
    search_term = search_term.replace(' ', '+')

    # add term query to URL
    url = template.format(search_term)

    # add page query to placeholder
    url += '&page{}'

    return url


# Generalize the pattern
def extract_record(item):
    """Extract and return data from a single record"""

    # description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')

    try:
        # price
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return

    try:
        # rank and rating
        # get i tag found from first item's html contents in results
        rating = item.i.text
        review_count = item.find('span', {'class': 'a-size-base', 'class': 's-underline-text'}).text
    except AttributeError:
        rating = ''
        review_count = ''

    results = (description, price, rating, review_count, url)

    return results


def main(search_term):
    """Run main program routine"""
    # Startup the webdriver
    driver = webdriver.Chrome()

    records = []
    url = get_url(search_term)

    for page in range(1, 21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})

        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)

    driver.close()

    # Save data to csv file
    with open(search_term + ' results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating', 'ReviewCount', 'Url'])
        writer.writerows(records)


main('Ultrawide monitor')
