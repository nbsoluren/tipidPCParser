from bs4 import BeautifulSoup
import requests
import json
import copy
import time, datetime
from datetime import datetime
import re




def stackParser(url):

    #initialization
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data,"html.parser")
    #Putting it all together
    data = {}
    data["user_id"] = partParser(soup)[0]["user_id"]
    data["message"] = soup.find("h1", {"class": "topictitle"}).text
    data["quotes"] = partParser(soup)
    data["date_posted"] = partParser(soup)[0]["message"]
    print(data)
    return json.dumps(data)




def partParser(soup):

    dataPack = []
    for chunk in soup.find("ul", {"posts"}).findAll("li"):
        data = {}
        author = chunk.find("p", {"class": "postmeta"}).find("a").text
        description = chunk.find("div", {"class": "postcontent"}).text
        data["user_id"] = author
        data["message"] = description
        data["date_posted"] = getDate_posted(chunk)
        dataPack.append(data)
    return dataPack

def getDate_posted(soup):
    chunk = copy.copy(soup)
    date_posted = chunk.find("p", {"class": "postmeta"})
    date_posted.a.decompose()
    rawTime = date_posted.text.split()
    year = rawTime[3]
    if (59 <= int(year) <= 99):
        yearString = '19' + year
    else:
        yearString = '20' + year
    dayString = rawTime[2] + ' ' + rawTime[1] + ' ' + yearString + ' ' + rawTime[5] + rawTime[6]
    d = datetime.strptime(dayString,'%b %d %Y %I:%M%p')
    return time.mktime(d.timetuple())





url = 'https://tipidpc.com/viewtopic.php?tid=322046'
stackParser(url)
