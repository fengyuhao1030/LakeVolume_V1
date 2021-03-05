import requests
import numpy as np
from bs4 import BeautifulSoup

CookieInfo = 'f5_cspm=1234; f5_cspm=1234; _ga=GA1.2.2047195957.1601634521; CIsForCookie_OPS=X3fPR1lkiF8NC60r7EbzEQAAABw; f5avr0921159276aaaaaaaaaaaaaaaa=DELKHLFEDCDBAKKCJCMIDOMEPAKJIGNOAKMBOOIDECMKKENACEMAEHIDALDACLKMMIMCENEOFIPHPKJINHDAGAGEAFNMILKLEOIGNDBJDADNEACKECILOJEOPPPBKKMG'
User = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
Headers = {'Cookie': CookieInfo,
           'User-Agent': User
           }
downloadPath = 'D:\Lake Volume\Lake Level\ATL13'

# Get folder names
baseURL = 'https://n5eil01u.ecs.nsidc.org/ATLAS/ATL13.003/'
Year = np.linspace(2019, 2019, 1, dtype=int)
Month = np.linspace(10, 10, 1, dtype=int)
Day = np.linspace(1, 31, 31, dtype=int)
validateURL = []
for tempYear in Year:
    for tempMonth in Month:
        for tempDay in Day:
            if tempMonth < 10:
                strMonth = '0' + str(tempMonth)
            else:
                strMonth = str(tempMonth)
            if tempDay < 10:
                strDay = '0' + str(tempDay)
            else:
                strDay = str(tempDay)
            tempURL = baseURL + str(tempYear) + '.' + strMonth + '.' + strDay + '/'
            Response = requests.get(tempURL, headers=Headers).text
            Soup = BeautifulSoup(Response,'lxml')
            validateFlag = Soup.find('title')
            if validateFlag.contents[0] != '404 Not Found':
                validateURL.append(tempURL)
                print(tempURL)
            del Response
            print(strDay)

# Download files in each folder
for tempURL in validateURL:
    Response = requests.get(tempURL, headers=Headers).text
    Soup = BeautifulSoup(Response, 'lxml')
    linkList = Soup.find_all('a')
    newLinkList = []
    for link in linkList:
        link = link.get('href')
        if link[-3:] == '.h5':
            newLinkList.append(tempURL+link)
    newLinkList = list(set(newLinkList))
    outputFileNameList = []
    for i in range(0, len(newLinkList)):
        tempLink = newLinkList[i]
        tempIndex = tempURL.rfind('/')
        outputFileName = downloadPath + '\\' + tempURL[-11:-1] + '_' + tempLink[tempIndex + 1:]
        outputFileNameList.append(outputFileName)
    for i in range(0, len(newLinkList)):
        tempLink = newLinkList[i]
        tempOutputFileName = outputFileNameList[i]
        tempResponse = requests.get(tempLink, headers=Headers, stream=True)
        outputFileHandle = open(tempOutputFileName, 'wb')
        outputFileHandle.write(tempResponse.content)
        outputFileHandle.close()
        tempResponse.close()
        print(tempLink)
