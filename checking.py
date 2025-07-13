import bs4
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request , urllib.parse, urllib.error
from urllib.request import urlopen, Request
import json

title_list=[]
price_list=[]
avail_status=[]

for i in range(1,51):
    x=str(i)
    url= "http://books.toscrape.com/catalogue/page-"+x+".html"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    
    soup= BeautifulSoup(html, 'html.parser')

#Collecting rating
    ratings = soup.find("p", class_="star-rating")
    rating = ratings.get("class")
    print(rating[1])

