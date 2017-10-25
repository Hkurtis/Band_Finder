import requests
import re
import urllib2
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from Tkinter import *
import tkMessageBox
import tkSimpleDialog
import webbrowser

chrome_path = "/Users/Hunter/Downloads/chromedriver"
driver = webdriver.Chrome(chrome_path)
#time.sleep(10)
#driver.find_element_by_xpath('//a[@title="Similar artists"]').click()

#url = 'https://www.metal-archives.com/bands/Anciients/3540359168' #url of page we want to crawl
#driver.maximize_window()
def has_bandcamp(band_name):
    global band_link_list
    global saved_link
    print "Checking official links of:"+band_name
    new_url = 'https://www.metal-archives.com/bands/'+band_name
    #instead of adding band name to metal archives, just grab the link to the new band instead
    #new_url = band_name
    ##USE ABOVE URL##
    driver.get(new_url)
    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")
    #print "before if"
    if soup.find('div',{'class': 'content_wrapper'}):
        #print "in if"
        soup.find_element_by_partial_link_text(band_name).click()
        html = driver.page_source
        soup = BeautifulSoup(html,"html.parser")
    #print "after if"
    time.sleep(1)

    #new code
    #Go through and check if on the metal encyclopedia if there is already
    #a bandcamp link somewhere
    driver.find_element_by_id("ui-id-5").click()#opens up additional links
    time.sleep(3)
    #reload html
    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")
    pattern = "Bandcamp"
    #if found in official links
    if soup.find('a', text = pattern):
        print "Bandcamp found in official links of:"+band_name
        #found the link now do the hyperlink
        for link in soup.find_all('a',href=True,text=pattern):
            saved_link = link.get("href")
            band_link_list.append(saved_link)
            print saved_link
            return True
    #check official links for bandcamp link, if not found check other link tabs
    if(soup.find('a', text = pattern)==None):
        print "Checking official merch of:"+band_name
        driver.find_element_by_id("ui-id-15").click()#click on official merch
        html = driver.page_source
        soup = BeautifulSoup(html,"html.parser")
        #if found in official merch
        if soup.find('a', text = pattern):
            print "Bandcamp found in official merch of:"+band_name
            #found the link now do the hyperlink
            for link in soup.find_all('a',href=True,text=pattern):
                saved_link = link.get("href")
                print saved_link
                return True
        #if not found in official merch
        if(soup.find('a', text = pattern)==None):
            print "Checking unofficial links of:"+band_name
            driver.find_element_by_id("ui-id-16").click()#click on unofficial links
            html = driver.page_source
            soup = BeautifulSoup(html,"html.parser")
            #if found in unofficial links
            if soup.find('a', text = pattern):
                print "Bandcamp found in unofficial links of:"+band_name
                #found the link now do the hyperlink
                for link in soup.find_all('a',href=True,text=pattern):
                    saved_link = link.get("href")
                    print saved_link
                    return True
            #if theres no link in either: official, merch, or unofficial links
            #return nothing
            if(soup.find('a', text = pattern)==None):
                print "No bandcamp found for: "+band_name
                return False

def hype_link(event):
    band_name_l = saved_link
    print band_name_l
    webbrowser.open_new(band_name_l)


def input_spider(max_pages, band_name):
    global original_url
    global saved_link#used later in function and in hype_link function
    global band_name_link #used later in function
    url = 'https://www.metal-archives.com/bands/'+band_name
    original_url = url
    driver.get(url)
    bandz = [] #variable for the band array
    page = 1
    #print "ah"
    while(page <= max_pages):
        #attempt 1
        source = requests.get(url) #get source code
        text = source.text #page in text form
        soup = BeautifulSoup(text, "html.parser") #make soup object to iterate through data
        #print soup
        #this is the case that there are many bands with the same name
        #current fix is to just grab the first band by the name
        if soup.find('div',{'class': 'content_wrapper'}):
            many_bands = soup.find('ul')
            for le in many_bands:
                #grab first
                url = soup.find('a')
                driver.get(url)
                source = requests.get(url) #get source code
                text = source.text #page in text form
                soup = BeautifulSoup(text, "html.parser") #make soup object to iterate through data
                #break out of loop when one band is grabbed
                break;
        else: #grab band name section
            bandName = soup.find_all('h1',{'class': 'band_name'})
        #print bandName
        for link in bandName:
            #gets the band name, need to use this to print to top of Tkinter
            name = link.find('a').contents[0]
            #print name
        driver.find_element_by_id("ui-id-4").click()#opens up similar artist tab
        time.sleep(3)
        #reload the soup page to find new things
        html = driver.page_source
        soup = BeautifulSoup(html,"html.parser")
        artist_list = soup.find_all('table', {'id': 'artist_list'})
        artist_string = str(artist_list)
        artists = artist_string.split("<a")

        #print artists
        for art in artists:
            if("href" in art):
                n = art.split(">")
                for x in n:
                    #grab the band link itself
                    #need to inject this block into other code
                    if("href" in x):
                        #Both xStr and xElement are variables for a band name
                        #I did not want to keep naming things similarly
                        #For the sake of keeping things cleaner
                        xStr = str(x)
                        print xStr
                        #grabs band's name
                        split_link_1 = xStr.split('/')
                        split_band = split_link_1[4]
                        print split_band
                        #grabs band's url to be searched later on
                        split_link_2 = xStr.split("\"")
                        split_url = split_link_2[1]
                        print split_url
                        #need to put split url into code so that the crawler
                        #searched based upon this url rather than just the band name
                    if("</a" in x):
                        #Both xStr and xElement are variables for a band name
                        #I did not want to keep naming things similarly
                        #For the sake of keeping things not confusing
                        xStr = str(x)
                        #print xStr

                        xElement = xStr.split("</a")
                        #print xElement
                        #print xElement[0]
                        if("see more" in xElement[0]):
                            break
                        elif("see more" not in xElement[0]):
                            bandz.append(xElement[0])

        #print bandz
        for ba in bandz:
            b = str(ba)
            b = b.replace(' ','_')
            b = b.replace('&','%26')
            #b = b.replace('%%2520',' ')
            band_name_link = b
            print "BAND_NAME_LINK IS %s" % band_name_link

            #original attempt uncomment to show off
            if has_bandcamp(b) == True:
                bandLabel = Label(app,text=b,fg="blue",cursor="hand2")
                bandLabel.pack()
                #need to fix, currently just grabs the nth band name
                #perhaps create a dictionary to lookup the band names
                bandLabel.bind("<Button-1>",hype_link)
                labels.append(bandLabel)
            else:
                bandLabel = Label(app,text=b)
                bandLabel.pack()
                #print bandLabel
                #bandLabel.pack(side=LEFT)
                labels.append(bandLabel)
        print labels
        page+=1
    return bandz

def find_bands():
    #clear out all previous labels
    #use for multiple searches
    global labels
    for label in labels:
        label.destroy()
    for i in xrange(len(labels)-1,-1,-1):
        del labels[i]

    global ban
    band = ban.get()
    input_spider(1,band)

#global stuff down here
labels = []
band_link_list = []
app = Tk()
app.title = "Band Finder"
app.geometry('500x500+200+200')
# bnd = StringVar()
ban = Entry(app)
ban.pack()
ban.focus_set()

#bandS = str(band)
b = Button(app, text = "Enter",command=find_bands)
b.pack()
app.mainloop()
#b = raw_input("Enter a band name: ")
#input_spider(1, b)
#spider(1)
