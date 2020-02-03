import googlemaps
import requests
import spacy
import json
import re
from old_models.addressModelExtension import AddressModel2

# gmaps = googlemaps.Client(key='AIzaSyBLpT1VXgEu8-4fTERh4a4XBLFm3blOE1U')

# geocode_result = gmaps.geocode('1600 Amphitheatre Parkway')
# loc = geocode_result[0]['geometry']['location']

# res = requests.get(url="https://www.googleapis.com/civicinfo/v2/representatives", params={'key': 'AIzaSyBLpT1VXgEu8-4fTERh4a4XBLFm3blOE1U', 'address': '1600 Amphitheatre Parkway'}).text

# m = re.search('(\d\d)th congressional district', res)
# print(float(m.group(1)))

am = AddressModel2()

def load(file):
    with open(file) as json_file:
        data = json.load(json_file)
    return data


def pred_district(event, pred_addr):
    res = requests.get(url="https://www.googleapis.com/civicinfo/v2/representatives", params={'key': 'AIzaSyBLpT1VXgEu8-4fTERh4a4XBLFm3blOE1U', 'address': pred_addr}).text

    m = re.search('(\d\d|\d)th congressional district', res)
    
    if m == None:
        # print(res)
        return 0
    else:
        return float(m.group(1))

def pred_address(event, nlp):
    pred = am.predict_event(event)
    return pred

def train(X_train, y_train):
    am.fit(X_train, y_train)
    # dm.fit(X_train, y_train)
    # km.fit(X_train, y_train)
    # im.fit(X_train, y_train)
    # print("training done")


def predict(data):
    nlp = spacy.load("en_core_web_sm")

    predictions = []
    for event in data:
        event_pred = {}

        #event_pred["incident_id"] = event["incident_id"]
        # event_pred["n_killed"] = pred_n_killed(event)
        # event_pred["n_injured"] = pred_n_injured(event)
        # event_pred["shooting_date"] = pred_shooting_date(event)
        pred_addr = pred_address(event, nlp)
        event_pred["address"] = pred_addr
        event_pred["congressional_district"] = pred_district(event, pred_addr)


        predictions.append(event_pred)

    return predictions

def run():
    X_test = load('./data/X_test.json')
    X_train = load('./data/X_val.json')
    y_train = load('./data/y_val.json')

    train(X_train, y_train)
    pred = predict(X_test)
    #with open('out.json', 'w') as f:
    #    f.write(json.dumps(pred))
    return json.dumps(pred)

print(run())

