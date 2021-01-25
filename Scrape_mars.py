# import all dependencies
import time
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
import pymongo
from pymongo import MongoClient

#create a database
conn = 'mongodb://localhost:27017'
client = MongoClient(conn)
db = client.mars_db
collection = db.mars


# Function to choose the executable path to driver
def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scraper():
    collection.drop()
    
# Run init_browser/driver.
    browser = init_browser()

# Visit Nasa news url.
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)

# HTML Object.
    html = browser.html

# Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, "html.parser")

    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text
    



# Run init_browser/driver.
    browser = init_browser()

# Visit the url for JPL Featured Space Image.
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

# HTML object
    html = browser.html

# Parse with Beautiful Soup 
    soup = BeautifulSoup(html, "html.parser")

    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image

   

 #Visit the url for Mars facts
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

# Use Panda's `read_html` to parse the URL.
    mars_data = pd.read_html(facts_url)

#Use Pandas to convert the data to a HTML table string.
    mars_data = pd.DataFrame(mars_data[0])
    mars_facts = mars_data.to_html(header = False, index = False)
    



# Create list of dictionaries called hemisphere_image_urls.
# Iterate through all URLs saved in hemis_url.
# Concatenate each with the main_astrogeo_url.
# Confirm the concat worked properly: confirmed.
# Visit each URL.

    
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})




    mars_hemisphere

    data={
        'news_title': news_title,
        'news_p' : news_p,
        'featured_image_url' : featured_image_url,
        'mars_facts' : mars_facts,
        'mars_hemispheres' : mars_hemispheres,
        }
    
    collection.insert(data)