---
title:  Downloading Interactively
updated: 2017-08-12 20:32:23
tags: python
---

- [Making My Music Download interactive](#org8dd8feb)


<a id="org8dd8feb"></a>

# Making My Music Download interactive

The Python script i last made to download the music from mio.to was designed in such a way that it download songs when the album link was given . Because then it was to Download all the music from the site and an interactive interface was not required . The list.py created a list of all the movies in a particular category and shell scripting was used to automatically download all the music from this list . Now I think that it should be made interactive , so I changed the script to and added the ability to search from their site and crab the link of the search result . python have an -i option which executes all the code in the file and gives a interactive shell.

there are three function new() , search_album() , download()

new() &#x2013; load the new music from Hindi Malayalam and Tamil Category search_album() &#x2013; takes a string as argument and searches the string in mio.to and loads the top five result download() &#x2013; shows all the loaded link and prompt for the index number of the movie to be downloaded

a global variable is declared to to store the the result of new() and search_album() then calling download to download any of the loaded link

modified code

```python

# Made by :  Nemesis
# Discription :This downloads The songs from site named mio.to
# syantax : python3 -i mio.py
# Requirements : python modules bs4
# System Package : eyed3 [User for insterting artwork]

import bs4
import requests
import sys
import re
import subprocess
import os

movie_list = []

def download_album(s):

    #Downloads the webpage and create a Beautifull Soup Object
    
    # url=sys.argv[1]
    # url = "http://mio.to/album/Aashiqui+2+%282013%29"

    url = str(s)
    mio = requests.get(url)
    mio_soup = bs4.BeautifulSoup(mio.text,'html.parser')

    #Extracts some informations :

    movie_name = re.search(r".*?\([0-9]+\)",mio_soup.select('div.heading')[0].text).group(0)
    art_work = mio_soup.select('div.group.info > img["src"]')[0]["src"]
    year = re.search(r'\(([0-9][0-9]+)\)',movie_name).group(1)
    link = re.search(r'http://media-images.mio.to/(.*?)/(.*)/Art-350.jpg',art_work).group(1)
    artwork_path = movie_name+"/artwork.jpg"

    print("\nMovie Name : "+movie_name )

    subprocess.call(["mkdir" ,"-p",movie_name])

    #Downloading the artwork
    print("Downloading Artwork")
    if not os.path.exists(artwork_path):
        subprocess.call(["wget","-q","--show-progress" ,"-c",art_work,"-O",artwork_path])

    #Finds all the songs links and downloads the and inserts the tags

    for i in mio_soup.find_all("tr" ,{"class" : "song-link"}):
        artist = ",".join(re.findall('"(.*?)"',i['track_artist']))
        album_name = movie_name
        track_number = i["track_number"]
        disk_number = i["disc_number"]
        track_name = i["track_name"]
        path = album_name+"/"+track_name+".mp3"
        #Create the download links of the mp3
        mp3_link = "http://media-audio.mio.to/"+link+"/"+i["album_id"][0]+"/"+i["album_id"]+"/"+disk_number+"_"+track_number+" - "+track_name+"-vbr-V5.mp3"
        print("Downloading ",track_name,"  ...","\n")
        subprocess.call(["wget","-q","--show-progress","-c",mp3_link,"-O",path])
        # Inserting the tag details
        command = ["eyeD3","--add-image",artwork_path+":FRONT_COVER",path,"-a",artist,"-A",album_name,"-t",track_name,"-n",track_number,"-Y",year]
        with open("log",'a') as log_file:
            subprocess.call(command,stdout=log_file,stderr=log_file)

def new():
    url = ["http://mio.to/Malayalam/Movie+Songs", "http://mio.to/Hindi/Movie+Songs","http://mio.to/Tamil/Movie+Songs"]
    global movie_list
    movie_list = []
    for i in url:
        mio = requests.get(i)
        mio_soup = bs4.BeautifulSoup(mio.text,"html.parser")
        for i in mio_soup.find_all('div', {'id' : '#trending-now'}):
            movie_list = movie_list + [ [j.find("h2").text , "http://mio.to"+j["href"]] for j in i.select("a")]
    for i in movie_list:
        print(" {0:20}: {1} ".format(i[0],i[1]))
    # return movie_list
    
            
def search_album(s):
    global movie_list
    movie_list = []
    s = s.replace(' ','+')
    url = "http://mio.to/search/" + s
    mio = requests.get(url)
    mio_soup = bs4.BeautifulSoup(mio.text,"html.parser")
    for i in mio_soup.find_all('div', {'id' : 'albums'}):
        movie_list = [ [ re.search(r'\<span\>(.*)\</span\>',str(j.select('span')[0])).group(1) , "http://mio.to"+j['href'] ] for j in i.select('a')[1:] ]
    for i in movie_list:
        print(" {0:20}: {1} ".format(i[0],i[1]))
    # return movie_list[0:5]

def download():
    global movie_list
    index = 1
    for i in movie_list:
        print(str(index)+ " {0:20}: {1} ".format(i[0],i[1]))
        index = index + 1
    print("Enter the number to Download : ")
    index = int(input())
    download_album(movie_list[index-1][1])
```
