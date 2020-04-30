from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import numpy as np
import pymongo
import os
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    

    # Mars News

    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(news_url) 
    time.sleep(8)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    print(f'{news_title} : \n{news_p}')


    #Mars Images

    main_url='https://www.jpl.nasa.gov'
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)
    time.sleep(8)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    main_image_items = soup.find('article', class_="carousel_item")
    main_image= main_image_items['style'].split("'")[1]
    main_image_url=main_url + main_image
    
    print(main_image_url)

    feature_image_items = soup.find('li', class_="slide")
    feature_image = soup.find("img", class_="thumb")["src"]
    feature_image_url = main_url + feature_image

    print(feature_image_url)


    # Mars Facts

    fact_url = "http://space-facts.com/mars/"
    browser.visit(fact_url)
    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    fact_tables = pd.read_html(fact_url)
    df=fact_tables[1]
    df1=df.drop(["Earth"], axis=1)
    
    html_table = df1.to_html(index=False)
    html_table=html_table.replace('\n', '')
    print(html_table)


    # Mars Hemispheres

    hemi_main_url='https://astrogeology.usgs.gov'
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    time.sleep(8)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemispheres_items = soup.find_all('div', class_='item')

    hemisphere_data = []

    for hemisphere in  hemispheres_items:
        # Titles
        hemisphere = hemisphere.find('div', class_="description")
        title = hemisphere.h3.text
        # Links
        hemi_href = hemisphere.a["href"] 
        browser.visit(hemi_main_url + hemi_href)
        time.sleep(5)

        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')

        img_items = image_soup.find('div', class_='downloads')
        img_url = img_items.find('li').a['href']
        
        # Store data in a dictionary
        hemisphere_data.append({"title": title, "img_url": img_url})
        
    print(hemisphere_data)

    # Mars Weather

    weather_url='https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(10)

    mars_weather = soup.find('article').find_all('span')[4].text
    #mars_weather = soup.find_all("span", class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")[27].text

    print(mars_weather)

    # Store data in a dictionary

    mars_data= {
        "news_title": news_title,
        "news_p": news_p,
        "main_image": main_image,
        "main_image_url": main_image_url,
        "feature_image": feature_image,
        "feature_image_url": feature_image_url,
        "mars_weather": mars_weather,
        "html_table": html_table,
        "hemisphere_data": hemisphere_data
        }   


    # Close the browser after scraping
    browser.quit()
    
    return mars_data

if __name__ == "__main__": 
    data = scrape()
    print(data)

   

