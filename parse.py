from bs4 import BeautifulSoup
import requests
import json

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
    print(json.dumps(data))
    return json.dumps(data)


def partParser(soup):

    dataPack = []
    for chunk in soup.find("ul", {"posts"}).findAll("li"):
        data = {}
        author = chunk.find("p", {"class": "postmeta"}).find("a").text
        description = chunk.find("div", {"class": "postcontent"}).text

        data["user_id"] = author
        data["message"] = description
        dataPack.append(data)
    return dataPack




url = 'https://tipidpc.com/viewtopic.php?tid=322046'
stackParser(url)
