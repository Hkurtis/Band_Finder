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
    driver.get(new_url)
    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")
    #print "before if"
    if soup.find('div',{'class': 'content_wrapper'}):
        #print "in if"
        soup.find_element_by_partial_link_text("Enslaved").click()
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
                print "No dice"
                return False

        # elif soup.find('a', text = pattern):
        #     print "Bandcamp found in official merch of:"+band_name
        #     #found the link now do the hyperlink
        #     for link in soup.find_all('a',href=True,text=pattern):
        #         saved_link = link.get("href")
        #         print saved_link
        #         return True
    # elif soup.find('a', text = pattern):
    #     print "Bandcamp found in official links of:"+band_name
    #     #found the link now do the hyperlink
    #     for link in soup.find_all('a',href=True,text=pattern):
    #         saved_link = link.get("href")
    #         print saved_link
    #         return True

    # driver.find_element_by_id("ui-id-4").click()#opens up similar artist tab
    # time.sleep(3)
    # #reload the soup page to find new things
    # html = driver.page_source
    # soup = BeautifulSoup(html,"html.parser")
    # artist_list = soup.find_all('table', {'id': 'artist_list'})
    # artist_string = str(artist_list)
    # artists = artist_string.split("<a")

    #Attempt one, find all the bandcamps by hand
    #didn't exactly work so I am refining
    #comment all above for original attempt to work
    #bc for bandcamp to keep things clean

    #uncomment all below to show working
    # bcurl = 'https://'+band_name+'.bandcamp.com'
    # source = requests.get(bcurl)
    # text = source.text
    # bcsoup = BeautifulSoup(text, "html.parser")
    # if bcsoup.find_all('h2',{'class':'signuptitle'}):
    #     driver.get(bcurl)
    #     print "No it doesn't"
    #     print bcurl
    #     return False
    # else:
    #     #print "Yes it does"
    #     return True

def hype_link(event):
    band_name_l = saved_link
    print band_name_l
    webbrowser.open_new(band_name_l)

    #original attempt
    #uncomment all below to have it work
    # band_name_l = band_name_link
    # #band_name_l = urllib2.quote(band_name_link)
    # print band_name_l
    # webbrowser.open_new(r"https://"+band_name_l+".bandcamp.com")
    # print "https://"+band_name_l+".bandcamp.com"

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
                    #print x
                    if("</a" in x):
                        #Both xStr and xElement are variables for a band name
                        #I did not want to keep naming things similarly
                        #For the sake of keeping things not confusing
                        xStr = str(x)
                        xElement = xStr.split("</a")
                        #print xElement[0]
                        if("see more" in xElement[0]):
                            break;
                        elif("see more" not in xElement[0]):
                            bandz.append(xElement[0])

        #print bandz
        for ba in bandz:
            b = str(ba)
            b = b.replace(' ','_')
            b = b.replace('&','%26')
            #b = b.replace('%%2520',' ')
            band_name_link = b
            #new code: comment until it works
            # if has_bandcamp == False:
            #     bandLabel = Label(app,text=b)
            #     bandLabel.pack()
            #     #print bandLabel
            #     #bandLabel.pack(side=LEFT)
            #     labels.append(bandLabel)

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
        #weird attempt
        # for band in labels:
        #     print band
        #     bandLabel = Label(app,text=band).pack()


                #print n
        # for art in artists:
        #     name = art.find('a').contents[0]
        #     print name
        #broken attempt
        # tabs = soup.findAll('table', {'class': 'display'})
        # similar_bands = soup.find(string=re.compile('id=artist_list'))
        # #rows = similar_bands.find_all('tr')
        # print similar_bands
        page+=1
    return bandz

def spider(max_pages):#, band_url):
    bandz = [] #variable for the band array
    page = 1
    print "ah"
    while(page <= max_pages):
        #attempt 1
        source = requests.get(url) #get source code
        text = source.text #page in text form
        soup = BeautifulSoup(text, "html.parser") #make soup object to iterate through data

        #print soup
        #grab band name section
        bandName = soup.find_all('h1',{'class': 'band_name'})
        #print bandName
        for link in bandName:
            #gets the band name, need to use this to print to top of Tkinter
            name = link.find('a').contents[0]
            print name
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
                    #print x
                    if("</a" in x):
                        #Both xStr and xElement are variables for a band name
                        #I did not want to keep naming things similarly
                        #For the sake of keeping things not confusing
                        xStr = str(x)
                        xElement = xStr.split("</a")
                        #print xElement[0]
                        bandz.append(xElement[0])
        print bandz

        page+=1
    return bandz

def find_bands():
    #clear out all previous labels
    global labels
    for label in labels:
        label.destroy()
    for i in xrange(len(labels)-1,-1,-1):
        del labels[i]

    global ban
    band = ban.get()
    input_spider(1,band)
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
