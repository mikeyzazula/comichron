from bs4 import BeautifulSoup
import urllib.request


##Used for the "Old" (pre 2014) format

file = open('./Data/missingOldFormat.txt', 'r')
LinkSoup = BeautifulSoup(file, 'lxml')
file.close()

#Grab each link from our initial dataset then go to each link and retrieve the data from the table
for link in LinkSoup.find_all('a'):
    tempLink = link.get('href', '%s')
    if tempLink[0] == 'm':
        url = "http://www.comichron.com/" + tempLink #building path to each month
        tablePage = urllib.request.urlopen(url).read()
        tableSoup = BeautifulSoup(tablePage, 'lxml')
        divTag = tableSoup.find_all("div", {"id": "content"})
        divSoup = BeautifulSoup(str(divTag), 'lxml')

        table = divSoup.findAll('tbody')[1]
        tableRows = table.find_all('tr')

        filename = tempLink[24:31]
        fo = open("Data/" + filename + ".txt", "w")
        for tr in tableRows:
            td = tr.find_all('td')
            row = [i.text for i in td]
            fo.write(str(row) + "\n")
        fo.close()
