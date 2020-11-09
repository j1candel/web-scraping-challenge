# Import Modules
from bs4 import BeautifulSoup as bs
import requests 
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd 

# Setting up splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless = False)

# Setting url
mars_url = 'https://mars.nasa.gov/news/'

# Visit mars_url 
browser.visit(mars_url)

# Scrape page into soup
html = browser.html
mars_soup = bs(html, 'html.parser')

# Getting the news title
news_title = mars_soup.find_all('div', class_='content_title')[0].text

# Getting the description 
news_p = mars_soup.find_all('div', class_='article_teaser_body')[0].text

#Setting url
jpg_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

#Visit jpg_url
browser.visit(jpg_url)

#Scraping the description 
html = browser.html
jpg_soup = bs(html, 'html.parser')

#Finding the url string
url_string = jpg_soup.find_all('img')[3]['src']

#Adding both urls together to get full url
featured_image_url = jpg_url + url_string
featured_image_url

#Findint the table url
table_url = 'https://space-facts.com/mars/'

#Bringing in the table
tables = pd.read_html(table_url)

#Displaying the table 
tables

#Setting the table to type 2
mars_facts = tables[2]

#Setting column names
mars_facts.columns = ['Measurement','Value']

#Converting table to html
mars_html = mars_facts.to_html()

#Replace \n with an empty string 
mars_html = mars_html.replace('\n','')

#Setting the urls
base_url = 'https://astrogeology.usgs.gov'
photos_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

#Visiting photos_url
browser.visit(photos_url)

#Scraping the description
html = browser.html
photos_soup = bs(html, 'html.parser')

#Finding the titles and jpegs for all hemisphere of mars
all_hemispheres = photos_soup.find('div', class_='collapsible results')
hemisphere_titles = all_hemispheres.find_all('div', class_='item')

#Setting hemisphere_image_urls to a list
hemisphere_image_urls = []

#Setting hem_images_dict to a dictionary
hem_images_dict = {}

#Iterating through hemisphere_titles
for n in hemisphere_titles:
    
    #Finding the title for each hemisphere of mars 
    hem = n.find('div', class_='description')
    title = hem.h3.text
    
    #Fidning the url for the picture links 
    pic_url = hem.a['href']
    
    #Visit the large pics of every hemisphere of mars
    browser.visit(base_url+pic_url)
    
    #Scraping the description 
    pic_html = browser.html
    pic_soup = bs(pic_html, 'html.parser')
    
    #Finding the url for large pics
    mars_pic_link = pic_soup.find('div', class_='downloads')
    image_url = mars_pic_link.find('li').a['href']
    
    #Setting name of the dictionary keys 
    hem_images_dict['title']=title
    hem_images_dict['image_url']=image_url
    
    #Appending each dictionary entry to a list 
    hemisphere_image_urls.append(hem_images_dict)

#Setting all entries into a dictionary 
mars_dict = {'news_title':news_title,
            'news_p':news_p,
            'featured_image_url':featured_image_url,
            'hemisphere_image_urls':hemisphere_image_urls,
            'mars_facts':mars_html
            }