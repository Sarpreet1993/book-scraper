#Importing Libraries
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request , urllib.parse, urllib.error
from urllib.request import urlopen, Request
import json
import sqlite3

#Forming necessary empty lists. 
title_list=[]
price_list=[]
avail_status=[]
rating_list=[]

#Loping through all the html pages of given url
for i in range(1,51):
    x=str(i)
    url= "http://books.toscrape.com/catalogue/page-"+x+".html"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    
    soup= BeautifulSoup(html, 'html.parser')

    #Collecting titles
    books = soup.find_all("article", class_="product_pod")
    for book in books:
        title = book.h3.a["title"]  
        title_list.append(title)

    #Collecting prices
    prices= soup.find_all("p", class_="price_color")
    for price in prices:
        value= price.text
        price_list.append(value)
    
    #Collecting availability
    avail= soup.find_all("p",class_="instock availability")
    for stock in avail:
        status= stock.text.strip()
        avail_status.append(status)
    
    #Collecting rating
    ratings = soup.find_all("p", class_="star-rating")
    for rating in ratings:
        star = rating.get("class")
        rating_list.append(star[1])

    

# Save to a JSON file
# Combine into list of dictionaries (rows)
data = []
for i in range(len(title_list)):
    row = {
        "title": title_list[i],
        "price": price_list[i],
        "availability": avail_status[i],
        "rating": rating_list[i]
       
    }
    data.append(row)

# Save to JSON
with open("book_scraping.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Saved structured data to book_scraping.json")


#Load the json data
with open("book_scraping.json", "r", encoding="utf-8") as f:
    books_data= json.load(f)

#Creating a new SQLite Database
conn= sqlite3.connect("books_data.db")
cur= conn.cursor() 

#Drop first(Precaution) and then Create Table
cur.execute("DROP TABLE IF EXISTS books")
cur.execute(''' CREATE TABLE IF NOT EXISTS books ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price TEXT,
            rating TEXT,
            availability TEXT
            )
             ''')
# Insert JSON data into the Table
for book in books_data:
    cur.execute('''
INSERT INTO books (title, price, rating, availability)
                VALUES (?,?,?,?)
                ''', (book["title"], book["price"], 
                      book["rating"], book["availability"]))

#Commit and Close the Database
conn.commit()
conn.close() 