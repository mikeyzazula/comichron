from bs4 import BeautifulSoup
import urllib.request


# old is mostly stuff before 2014, new is after. Lots of special one off cases the functions were messed with for.
file = open('./Data/missingOldFormat.txt', 'r')
#file = open('./Data/missing2014format.txt', 'r')
LinkSoup = BeautifulSoup(file, 'lxml')
file.close()


def old_format():
    ##Grab each link from our initial data set then go to each link and retrieve the data from the table
    for link in LinkSoup.find_all('a'):
        tempLink = link.get('href', '%s')
        if tempLink[0] == 'm':
            url = "http://www.comichron.com/" + tempLink  # building path to each month
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


def new_format():
    for link in LinkSoup.find_all('a'):
        tempLink = link.get('href', '%s')
        if tempLink[0] == 'm':
            url = "http://www.comichron.com/" + tempLink  # building path to each month
            tablePage = urllib.request.urlopen(url).read()
            tableSoup = BeautifulSoup(tablePage, 'lxml')
            divTag = tableSoup.find_all("table", {"id": "Top300Comics"})
            divSoup = BeautifulSoup(str(divTag), 'lxml')

            table = divSoup.findA('tbody')
            tableRows = table.find_all('tr')

            filename = tempLink[24:31]
            fo = open("Data/" + filename + ".txt", "w")
            for tr in tableRows:
                td = tr.find_all('td')
                row = [i.text for i in td]
                fo.write(str(row) + "\n")
            fo.close()
