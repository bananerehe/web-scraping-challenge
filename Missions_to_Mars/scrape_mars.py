# Dependencies
import time
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # NASA Mars News
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_titles = soup.find(class_='slide')
    news_title = news_titles.find(class_='content_title').text
    news_p = news_titles.find(class_="article_teaser_body").text

    # Featured Image
    url = "https://www.jpl.nasa.gov/images?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)
    browser.links.find_by_partial_text('Image').click()
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_image_url = soup.find('img', class_="BaseImage")['src']

    # Mars Facts
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    df = tables[0]
    df = df.rename(columns={0: "Description", 1: "Mars_Values"})
    mars_table = df.to_dict('records')

    # Mars Hemisphere
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    titles = soup.find_all('h3')
    titles[:] = (title.text for title in titles)
    titles[:] = (title.split(" Enhanced")[0] for title in titles)
    hemisphere_image_urls = []
    for title in titles:
        browser.visit(url)
        browser.links.find_by_partial_text(title).click()
        time.sleep(1)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_url = soup.find('div',class_='downloads').ul.li.a['href']
        hemisphere_image_urls.append({"title": title, "img_url": img_url})

    # Organize data
    mars_data = {"news_title":news_title, "news_p":news_p,"featured_image_url":featured_image_url,"mars_table":mars_table,
                "hemisphere_image_urls":hemisphere_image_urls}

    browser.quit()

    return mars_data