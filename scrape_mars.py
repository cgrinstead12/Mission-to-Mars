from splinter import Browser
from bs4 import BeautifulSoup as bs
import pymongo
import time
import pandas as pd

def Scrape():

  mars_dict = {}

  executable_path = {"executable_path":"C:/Users/cgrinstead12/Desktop/Mission to Mars/chromedriver.exe"}
  browser = Browser("chrome", **executable_path, headless = False)
  url = "https://mars.nasa.gov/news/"
  
  print(f'chrome driver visiting url {url}')

  browser.visit(url)
  html = browser.html
  soup = bs(html,"html.parser")

  news_title = soup.find('div', class_='content_title').text
  news_para = soup.find('div', class_='article_teaser_body').text

  mars_dict["news_title"] = news_title
  mars_dict["news_para"] = news_para

  image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

  browser.visit(image_url)
  print(f'chrome driver visiting url {url}')

  browser.click_link_by_partial_text('FULL IMAGE')
  time.sleep(5)
  browser.click_link_by_partial_text('more info')
  time.sleep(5)
  image_html = browser.html
  soup = bs(image_html, "html.parser")
  image_url = soup.find('img', class_="main_image")['src']

  main_url = 'https://www.jpl.nasa.gov/'

  image_url_combined = main_url + image_url

  mars_dict["main_image_url"] = image_url_combined

  browser.visit(image_url_combined)
  time.sleep(5)
  print(f'chrome driver visiting url {url}')

  url = 'https://twitter.com/marswxreport?lang=en'
  browser.visit(url)
  time.sleep(10)
  twitter_html = browser.html
  soup = bs(twitter_html, "html.parser")
  mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
  url = "https://space-facts.com/mars/"

  mars_dict["weather"] = mars_weather

  browser.visit(url)
  time.sleep(10)

  print(f'chrome driver visiting url {url}')

  facts_html = browser.html
  soup = bs(facts_html, "html.parser")
  results = soup.find('tbody').find_all('tr')

  mars_facts = []

  for result in results:
      column_description = result.find('td', class_="column-1").text
      print(f' this is the column description: {column_description}')
      column_fact = result.find('td', class_="column-2").text
      print(f' this is the column fact: {column_fact}')
      mars_space_facts = {}
      mars_space_facts['column_description'] = column_fact
      mars_facts.append(mars_space_facts)

  mars_dict['mars_facts'] = mars_facts

  df = pd.DataFrame(list(mars_dict.items()), columns=['Facts', 'Data'])

  url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

  hemispheres = ['Cerberus Hemisphere Enhanced', 
               'Schiaparelli Hemisphere Enhanced', 
               'Syrtis Major Hemisphere Enhanced', 
               'Valles Marineris Hemisphere Enhanced']
  links = []

# [  { title: '', url: '' },  ]
  for hemisphere in hemispheres:
    browser.visit(url)
    time.sleep(5)
    print(f'chrome driver visiting url {url}')
    browser.click_link_by_partial_text(hemisphere)
    time.sleep(5)
    highresMars_html = browser.html
    soup = bs(highresMars_html, "html.parser")
    time.sleep(5)
    image_url_hemisphere = soup.find('div', class_='downloads').a['href']
    image_dict = {}
    image_dict['url'] = image_url_hemisphere
    image_dict['title'] = hemisphere
    links.append(image_dict)

  mars_dict['links'] = links

  print(mars_dict)

  return mars_dict

  print("scrape complete")
