import os
import sys
import requests
from bs4 import BeautifulSoup
from re import sub
import string

#get_raw_html
def get_raw_html(URL):
   "Given a raw URL link this function queries and returns the raw html file as String."
   html_string = requests.get(URL, stream=True).text.encode('utf-8')
   return html_string

#get_listing_urls
def get_listing_urls(html_string):
    "Given a raw html string please extract the URL links of listings"
    payload = BeautifulSoup(html_string)
    boatlist = []
    #find names
    for linklist in payload.find_all(class_="ad-title"):
        for boats in linklist.a.stripped_strings:
            boatlist.append([boats,"http://www.boattrader.com"+linklist.a.get('href')])
    return boatlist
    #for i in range(len(boatlist)):
    #    print boatlist[i]

#generate_search_url
def generate_search_url():
    "This function generates a series of search result pages' url."
    #Sort Criteria
    sort_criteria = ""
    while sort_criteria not in ("UPDATED" , "LENGTH","PRICE","YEAR"):
        sort_criteria = raw_input("Please enter your sort criteria.\n\
1) UPDATED for last date updated\n\
2) LENGTH for length of boat\n\
3) PRICE for price of boat\n\
4) YEAR for year of boats manufacturing\n\
5) DISTANCE for distance of boats to the selected location\n\
   Please enter selection now:").upper()
    #Sort order
    sort_order = ""
    while sort_order not in ("DESC" , "ASC"):
        sort_order = raw_input("Please enter your sort order.  Either DESC or ASC please: ").upper()

    html_for_input = "www.boattrader.com/search-results/NewOrUsed-any/Type-any/Category-all/State-TX|Texas/Length-0,10000/Sort-" + sort_criteria + ":" + sort_order
    html_for_input = "http://" + html_for_input
    return html_for_input

#get_UID
def get_UID(URL):
   "Given a URL, this function returns the unique identifier (UID) of the listing."
   site = requests.get(URL, stream=True)
   payload = BeautifulSoup(site.text.encode('utf-8'))
   listing_id_tag = payload.find(id="ad_id")
   UID = listing_id_tag.get('value')
   return UID


#get_title
def get_title(payload):
   "Given a beautifulsoup object, this function returns the title of an individual listing page."
   ad_title = payload.title.string
   return ad_title


#get_price
def get_price(payload):
   "Given a beautifulsoup object, this function returns the price of an individual listing page."
   price = payload.find(id="ad-detail-template",class_="container content").h2.string
   #price = float(sub(r'[^\d.]', '', price))
   return price

#get_description
def get_description(payload):
   "Given a beautifulsoup object, this function returns the description of an individual listing page."
   listing_description = payload.meta.find(attrs={"name":"description"}).attrs['content']
   return listing_description

#get_img_URL
def get_img_URL(payload):
   "This function given a beautifulsoup object will return a list of image URLs of an individual listing page."
   imageURL = []
   for img in payload.find_all('img'):#.src:
       imageURL.append(img.get('src'))
   return imageURL

#get_phone_num
def get_phone_num(payload):
   "This function given a beautifulsoup object will return the phone number of an individual listing page."
   phone_number = payload.find(class_="phone").string
   return phone_number

#get_details
def get_details(payload):
   "This function given a beautifulsoup object will return the 'details section' of an individual listing page."
   details = []
   payload = payload.find(id="ad_detail")
   for detail in payload.find_all('li'):
      details.append([detail.label.string,detail.contents[1]])
   return details    

#This section runs search results.  At this time it has rudimentary filters.
url = generate_search_url()
#This section collects the listings
raw_html =  get_raw_html(url)
listings = get_listing_urls(raw_html)
listing = listings[0][1]
UID = get_UID(listing)
print "UID : " + UID
#create soup object for other scraper functions
listing_raw = requests.get(listing, stream=True).text.encode('utf-8')
listing_soup = BeautifulSoup(listing_raw)

title = get_title(listing_soup)
print "Listing Title : " + title 

price = get_price(listing_soup)
print "Listing Price : " + price

description = get_description(listing_soup)
print "Description : " + description

imageURL = get_img_URL(listing_soup)
for i in range(len(imageURL)):
        print "Image URL : "+imageURL[i]

phone_no = get_phone_num(listing_soup)
print "Phone number : " + phone_no

details = get_details(listing_soup)
print "Additional Details"
for i in range(len(details)):
        print details[i][0]+" : " + details[i][1]