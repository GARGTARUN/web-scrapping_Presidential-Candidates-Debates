import requests
import csv
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd

data = {'TITLE': [],
        'TYPE': [],
        'YEAR': [],
        'DATE': [],
        'PARTICIPANTS': [],
        'MODERATORS': [],
        'LINK': [],
        'TRANSCRIPT': [],
        'DICTIONARY': []
        }
csvFile = open('data.csv', 'w', newline='')
csvWriter = csv.writer(csvFile)
csvWriter.writerow(["TITLE", "TYPE", "YEAR", "DATE", "PARTICIPANTS", "MODERATORS", "LINK"])
csvFile.close

# For getting data from website
URL = "https://www.presidency.ucsb.edu/documents/presidential-documents-archive-guidebook/presidential-candidates-debates-1960-2016"
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'lxml')

all_links = soup.find_all("a")
lin_web = []
for link in all_links:
    lin_web.append(link.get("href"))

# for storing all the links available on the page

links = []
test = 'https://www.presidency.ucsb.edu/ws/index.php?pid=105443'

for i in range(len(lin_web)):
    if isinstance(lin_web[i], str):
        if lin_web[i][0:33] == test[0:33]:
            links.append(lin_web[i])

# to get specific fields from each webpage

for z in range(len(links)):

    wiki = links[z]
    page = urllib.request.urlopen(wiki)

    soup = BeautifulSoup(page)
    response = requests.get(wiki)
    soup = BeautifulSoup(response.text, "html.parser")

    typ = soup.find('div', class_="field-ds-doc-title")

    name = list(typ.text)  # Title of the debate

    while "\n" in name:
        name.remove("\n")
    name = "".join(name)
    print('TITLE:', name)  # print debate title

    # to classify the type of debate

    if "Republican" in name:
        typ = "Primary-R (Republican)"
    elif "Democratic" in name:
        typ = "Primary-D (Democratic)"
    elif "Vice Presidential" in name:
        typ = "General"
    elif "Presidential" in name:
        typ = "General"
    else:
        typ = "Not Given"

    print("TYPE:", typ)  # print debate type

    date = soup.find(class_="date-display-single")
    print("DATE:", date.text)  # print date of debate
    date = date.text  # exact date of debate
    tmp = list(date)
    year = ''.join(tmp[-4:])  # year of debate
    print("YEAR:", year)  # print year of debate
    trans = soup.find(class_="field-docs-content")
    trans = trans.text.split()  # full transcript of debate

    participants = []  # to store all the participants names

    # to seperate participants names from transcript

    f = 0

    for i in range(50):
        if "MODERATOR" in trans[i] or "Moderator" in trans[i] or "Moderated" in trans[i]:
            f = 1
            break

    if f == 0:
        participants = "NA"
    if f == 1:
        participants = trans[1:i].copy()

    for v in range(len(participants) - 1, 0, -1):
        if participants[v] == 'and':
            participants[v] = ';'

    participants = " ".join(participants)
    participants = participants.split(";")
    print('PARTICIPANTS:', participants)  # print participants name

    mod = []  # to store names of moderators

    # to seperate names of moderators from transcript

    fl = 0
    for x in range(i + 1, i + 50):
        mod.append(trans[x])
        if ":" in trans[x]:
            fl = 1
            break
    if fl == 0:
        mod = "NA"
    mod = mod[0:-1]

    for v in range(len(mod) - 1, 0, -1):
        if mod[v] == 'and':
            mod[v] = ';'
    mod = " ".join(mod)
    if ";" in mod:
        mod = mod.split(";")
    print('MODERATORS:', mod)  # print moderators name

    listoflist = []  # store lists having name and statement of person
    tmp = []
    keys = []
    for i in range(x, len(trans)-1):
        if ":" in trans[i]:
            tmp1 = list(trans[i])
            tmp1.remove(":")
            tmp1 = "".join(tmp1)
            if tmp1.isupper():
                tmp.append(i)
                if tmp1 not in keys:
                    keys.append(tmp1)
    for i in range(len(tmp) - 1):
        tmp1 = list(trans[tmp[i]])
        if ":" in tmp1:
            tmp1.remove(":")
        tmp1 = "".join(tmp1)
        tmp2 = [tmp1, ' '.join(trans[tmp[i] + 1:tmp[i + 1] - 1])]
        listoflist.append(tmp2)
    print(listoflist)  # print listoflist
    trans = trans[x:]
    trans = " ".join(trans)  # full transcript of debate
    print(trans)  # print full transcript
    # create or open file in append mode to store data in csv
    csvFile = open('data.csv', 'a', newline='')
    flag=0
    # Use csv Writer
    if(len(listoflist)>3):
        flag=1
        tmp1 = list(trans[tmp[i + 1]])
        if ":" in tmp1:
            tmp1.remove(":")
            tmp1 = "".join(tmp1)
        tmp2 = [tmp1, ' '.join(trans[tmp[i + 1] + 1:len(trans)])]
        listoflist.append(tmp2)
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow([name, typ, year, date, participants, mod, links[z]])  # store data in csv
    print("\n\n\n")
    dict={}   # Dictionary
    if flag == 1:
        for i in range(len(keys)):
            tmplist=[]
            for j in range(len(listoflist)):
                if(keys[i]==listoflist[j][0]):
                    tmplist.append(listoflist[j][1])
            dict[keys[i]]=tmplist
    # print(dict)

    data['TITLE'].append(name)
    data['TYPE'].append(typ)
    data['YEAR'].append(year)
    data['DATE'].append(date)
    data['PARTICIPANTS'].append(participants)
    data['MODERATORS'].append(mod)
    data['LINK'].append(links[z])
    data['TRANSCRIPT'].append(trans)
    data['DICTIONARY'].append(dict)

df = pd.DataFrame(data)
df.head(5)
print(df.head(5))
