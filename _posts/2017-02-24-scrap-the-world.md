---
layout: post
title: Downloading Music .
---
 
This is what happens when a lazy  person wants to listen to music and does not like to manually download songs from the internet .One reason is that it is boring another because of adds . It was the same time when i was trying to learn python and was reading Automating Boring Stuffs with python . Hmm why dont i write a script to automate this boring task of downloading songs one by one .


# Mango 
[mango](http://www.maango.info/ "Mango") is a new site with modern look and contains songs from 2015 only . I used to download new songs fom here so it was my first choice scrap .

```line_numbers=false

#!/usr/bin/python3

import bs4,requests,os

url = "http://www.maango.info/malayalam/"
#url = "http://www.maango.info/tamil/"
#url = "http://www.maango.info/hindi/"

while True :
#Downloading Man Page
    maango = requests.get(url)
    maango_soup = bs4.BeautifulSoup(maango.text, "html.parser")
    link = []

#Looks for Links With Text Download and create a List(Create a list of Movies)
    for i in maango_soup.find_all('a', text="Download"):
        link.append(i["href"])

    for j in range(0,int(len(link))):
	#Downloads the Movie Page 
        song = requests.get(link[j])
        song_soup = bs4.BeautifulSoup(song.text, "html.parser")
        mp3_link = []

	#Make a List of all available MP3 links 
        for i in song_soup.find_all('a', text="Download (Server 2)"):
            mp3_link.append(i["href"])
	
	#Get the Movie Title
        title = song_soup.select('div[class="songbox"] > h2')
        if  os.path.exists(song_soup.select('div[class="p-info-serial"] > span')[0].text) :
            print("FileExist")
        else:
	    #Make Folder with movie's Name            
	    os.makedirs(song_soup.select('div[class="p-info-serial"] > span')[0].text)
            os.chdir(song_soup.select('div[class="p-info-serial"] > span')[0].text)

	    #Download's The MP3 
            for i in range(0,int(len(mp3_link))):
                print("Downloading " + title[i].text + " ...")
                mp3 = requests.get(mp3_link[i])
                mp3_file = open(title[i].text+".mp3", "wb")
                for chunk in mp3.iter_content(100000):
                    mp3_file.write(chunk)
                mp3_file.close()
            os.chdir("..")
#Go to Next Page
    try :
        url = maango_soup.find_all('a', text="Next")[0]["href"]
    except IndexError:
        print("Done ...")
        exit()
```


After downloading all the songs from HINDI TAMIL and MALAYALAM section i wrote a shell script that invoke this script and update my local files .
Next task was to find good site to get old songs.

# Tmail Beats

[Tamil Beats](http://www.tamilabeat.com/index.html "Tamil Beats") is a old site that contain a big database of tamil Songs it was the next cantidate . unlike mango that download the songs i wrote a script that scrape their mp3 [database](http://www.tamilabeat.com/tamilsongs/movies%20a%20to%20z/ "TamilBeats MP3") section and find the movie and its corresponding songs , it outputed it as a wget command  . This was done because the download speed was limited it did not utilize my full bandwidth . Later I used the output and parallel program to run 10 downloads at ones .

```line_numbers=false
#!/usr/bin/python3

import bs4,requests,re,os,sys,time
url = sys.argv[1]
beats = requests.get(url)
beats_soup = bs4.BeautifulSoup(beats.text,"html.parser")
links_unsorted = []
for i in beats_soup.select('a'):
    links_unsorted.append(i["href"])
links = []
sort = re.compile(r'http:.*')
for i in links_unsorted:
    if(sort.search(i)):
        links.append(i)
sort = re.compile(r'(.\.\/)(.*)')
for i in links_unsorted:
    if sort.search(i):
        links.append(sort.sub(r'http://www.tamilabeat.com/tamilsongs/\2',i))
links_unique = links
print(len(links_unique))
songs = []
for i in links_unique[:]:
    print(i)
    try:
        music = requests.get(i)
    except TimeoutError:
        print("TimeOut at "+ i )
    if music.ok:
        music_soup = bs4.BeautifulSoup(music.text,"html.parser")
        try:
            movie_name = re.compile(r'(.*?)-').search(music_soup.title.string).group(1)
        except AttributeError:
            movie_name = re.compile(r'([A-Z])\w+([ ])*([A-Z])*\w*( )*([A-Z])*\w*').search(music_soup.select('tr > td > b > font')[1].text).group(0)
        if movie_name == "TamilBeat.Com "  :
            try :
                movie_name = re.compile(r'([A-Z])\w+([ ])*([A-Z])*\w*( )*([A-Z])*\w*').search(music_soup.select('tr > td > b > font')[1].text).group(0)
            except AttributeError:
                movie_name = ""
            except  IndexError:
                movie_name= ""
        print(movie_name)
        for j in music_soup.select('tr > td > font > a["href"]'):
            songs.append(j["href"])
        songs = list(set(songs))
        for j in songs:
            if re.compile(".*mp3").search(j):
                title =  re.compile('%20').sub("",re.compile("(TamilBeat\.Com[%20\-%20]*)|([%20\-%20]*TamilBeat(\.Com)*)").sub(" ",re.compile(r'([A-Z,a-z,0-9,%-.]*)\.mp3').search(j).group(1)))
                sys.stdout.write("wget -c  "+j+ " -O  "+"./"+ "\""+movie_name+"\"/"+"\""+title[:-1]+"\".mp3\n")
    songs = []
print("Done ...")
```
made a file with all the links. 

```line_numbers=false

./tamilbeats.py http://www.tamilabeat.com/tamilsongs/movies%20a%20to%20z/ >> links
#extracted dir name and makes them 
cat links  | grep wget | cut -d "/" -f 7 |sort | uniq |  xargs -n 1 mkdir
#parallel
cat links | grep wget | sort | uniq | parallel -P 10
```
Got all the Tamil Songs Around 28GB
Next HINDI Songs


# Songs PK
[Songs PK](http://www.songspk.io/bollywood-songs-mp3.html "SongsPK") has even bigger set of collection songs [HINDI] . First i wrote a script to scrap the movie link from their site 

```line_numbers=false
#!/usr/bin/python3
import sys,requests,bs4
url = sys.argv[1]
songspk = requests.get(url)
songspk_soup = bs4.BeautifulSoup(songspk.text,"html.parser")

for i in songspk_soup.select('li > ul > li > a["href"]'):
    if  not (len(i["href"]) > 22 and i["href"][0:22]=="http://www.songspk.io/"):
        sys.stdout.write("http://www.songspk.io/" + i["href"] + "\n")
    else:
        sys.stdout.write(i["href"] + "\n")
```
and another to scrap the songs from the movie link . songs pk had three site design and different methord had to be made to scrap them . this script take two arguments one link and another movie name 

```line_numbers=false
#!/usr/bin/python3
import sys,requests,bs4,re

sig_latest = 'div > div > div > div > table > tr > td > strong > font > a'
sig_old = 'tr > td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > table > tr > td > a[href]'
sig_mid = 'li > div > p > b > a[href]'

url = sys.argv[1]
movie_name = sys.argv[2]

print("Movie :: " + movie_name)
songspk = requests.get(url)
songspk_soup = bs4.BeautifulSoup(songspk.text,"html.parser")

if len(songspk_soup.select(sig_mid)) > 0 :
    for i in songspk_soup.select(sig_mid):
        sys.stdout.write("wget -c " + "\""+ i["href"]+"\"  -O ./"+"\""+movie_name+"\"/\""+i.text+"\".mp3" + "\n")

elif len(songspk_soup.select(sig_old)) > 0:
    for i in songspk_soup.select(sig_old):
        sys.stdout.write("wget -c " +"\""+ i["href"]+"\"  -O ./"+"\""+movie_name+"\"/\""+re.sub(r'[\t,\n]','',i.text)+"\".mp3" + "\n")

elif len(songspk_soup.select(sig_latest)) ==2 :
    sys.stdout.write("wget -c " +"\""+ songspk_soup.select(sig_latest)[1]["href"] +"\"   -O ./"+"\""+movie_name+"\"/\"" + songspk_soup.select(sig_latest)[1].text+"\".zip" + "\n")

```
Runing the scripts 


```line_numbers=false
#Made a file with all the movies links
echo http://www.songspk.io/{a..z}_list.html | xargs -n 1 ./link.py >> movie_link
#Extracting move name
cat movie_link | rev | cut -d "/" -f 1 | rev | cut -d "." -f 1 | tr [_] [' '] | sed -e "s/\b\(.\)/\u\1/g"  | sed -r 's/(.*)/"&"/' >> movie_name
#Mixing both files
paste -d " " movie_lins movie_name >> arg
#then the links
cat arg | xargs -n 1 ./songs.py >> songs
cat songs | sort | uniq >> final_links
echo 1 >> count
```

Then Wrote a bash script to run the downloading and added a cron job to autorun the script at reboot

```line_numbers=false
#!/bin/bash
sleep 180s
COUNTER=$(cat ./count)
while [ $COUNTER -lt 23000 ];do
sed -n $COUNTER,$(($COUNTER+100))p ./final_links | parallel -P 10 >> log 2>&1 
COUNTER=$(($COUNTER+100))
echo $COUNTER > ./count
done
```

<br>

