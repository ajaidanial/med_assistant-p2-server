from urllib.request import urlopen
from bs4 import BeautifulSoup
from firebase_admin import db
import firebase_admin
from firebase_admin import credentials


# init the firebase admin sdk
cred = credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://med-assistant-a6d8a.firebaseio.com/'
})


data = []
result = []
# TODO : remove on first time
major_data = db.reference('diseases_data').get()
major_data_d = []
major_data_s = []
prediction_data = {}
# making the individual data
for x in major_data:
        major_data_d.append(x)
        major_data_s.append(major_data[x])
        prediction_data[x] = 0
# TODO : remove on first time end


def make_soup(url):
    thepage=urlopen(url)
    soupdata= BeautifulSoup(thepage,"html.parser")
    return soupdata


def writefreshdatabase_prepare():
    soup=make_soup("http://people.dbmi.columbia.edu/~friedma/Projects/DiseaseSymptomKB/index.html")
    rows = soup.find_all('tr')[1:]
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    t = []
    for x in data:
        if len(x) == 3:
            d = str(x[0]).split("_")[-1].replace("\n", "")
            x = str(x).split('_')[-1].replace("']", "").replace("\n", "")
            result.append(t)
            t = []
            t.append(d)
            t.append(x)
        else:
            x = str(x).split('_')[-1].replace("']", "").replace("\n", "")
            t.append(x)
    result.append(t)
    del result[0]


def writeres(list_data):
    d = list_data[0].replace("\\n","").lower().replace("\\","")
    s = ",".join(list_data[1:]).replace("\\n","").lower().replace("\\","")
    db.reference('diseases_data').child(d).set(s)


def firstTimeDataAdd():
    print("Writing Data")
    writefreshdatabase_prepare()
    for dis in result:
        writeres(dis)
    print("Writing Data Done")


def prediction(data):
    data = data.split(",")
    return predict(data)


def predict(data):
    for sy_list in range(0, len(major_data_d)):
        for d in data:
            if d in major_data_s[sy_list]:
                prediction_data[major_data_d[sy_list]] += 1

    # Ranking 
    max = 0
    output_result = []    
    for x, y in prediction_data.items():
        if y == max:
            output_result.append(x)
            continue
        if y > max and y != max:
            max = y
            output_result = []
            output_result.append(x)
    print(output_result)
    return output_result
