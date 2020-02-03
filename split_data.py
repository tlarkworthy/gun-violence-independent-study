import json
from sklearn.model_selection import train_test_split

road_map = {"Road": "Rd", "Street": "St", "Avenue": "Ave", "Boulevard": "Blvd", 
            "Lane": "Ln", "Drive": "Dr", "Terrace": "Ter", "Place": "Pl", "Court": "Ct",
            "Roads": "Rd", "Streets": "St", "Avenues": "Ave", "Boulevards": "Blvd", 
            "Lanes": "Ln", "Drives": "Dr", "Terraces": "Ter", "Places": "Pl", "Courts": "Ct",
            "road": "Rd", "street": "St", "avenue": "Ave", "boulevard": "Blvd", 
            "lane": "Ln", "drive": "Dr", "terrace": "Ter", "place": "Pl", "court": "Ct"}

road_map_inv = {"Rd": "Road", "St": "Street", "Ave": "Avenue", "Blvd": "Boulevard", "Ln": "Lane", "Dr": "Drive", "Ter": "Terrace", "Pl": "Place", "Ct": "Court", "Cir": "Circle", "Rd.": "Road", "St.": "Street", "Ave.": "Avenue", "Blvd.": "Boulevard", "Ln.": "Lane", "Dr.": "Drive", "Ter.": "Terrace", "Pl.": "Place", "Ct.": "Court", "Cir.": "Circle",  "road": "Road", "street": "Sreett", "avenue": "Avenue", "boulevard": "Boulevard", "lane": "Lane", "drive": "Drive", "terrace": "Terrace", "place": "Place", "court": "Court"}


def write_json_to_file(filename, json_obj):
    with open(filename, 'w') as f:
        f.write(json.dumps(json_obj))


def clean_addresses(text, remove_punc = False):
    if remove_punc:
        text = text.replace(".", "")
        text = text.replace(",", "")
        text = text.replace(";", "")
    address_cleaned = [road_map_inv[tok] if tok in road_map_inv else tok 
                       for tok in text.split()]
    return " ".join(address_cleaned)

def main():
    # read and load data
    data = []

    with open('data/gun_data_new.json') as f:
        data = json.loads(f.read())

    # split data into X and y
    X = []
    y = []
    for event in data:

        event["text"] = clean_addresses(event["text"])
        event["address"] = clean_addresses(event["address"], remove_punc = True)

        # skip all faulty articles
        if event["publish_date"] == "" or event["address"] not in event["text"]:
            continue

        if event["shooting_date"] > event["publish_date"]:
            continue

        xdict = {
            "text": event["text"],
            "publish_date": event["publish_date"]
        }

        ydict = {
            "n_killed": event["n_killed"],
            "n_injured": event["n_injured"],
            "shooting_date": event["shooting_date"],
            "address": event["address"],
            "state": event["state"],
            "city_or_county": event["city_or_county"],
            "congressional_district": event["congressional_district"]
        }

        X.append(xdict)
        y.append(ydict)

    print(len(X))

    # split X and y into training 70%, validation 9%, test 21%
    X_train, X_inter, y_train, y_inter = train_test_split(X, y, test_size=0.10, random_state=16)
    X_val, X_test, y_val, y_test = train_test_split(X_inter, y_inter, test_size=0.5, random_state=42)
    #print(len(X_train))
    #print(len(X_val))
    #print(len(X_test))

    # output split to json file
    write_json_to_file('data/X_train.json', X_train)
    write_json_to_file('data/X_val.json',   X_val)
    write_json_to_file('data/X_test.json',  X_test)
    write_json_to_file('data/y_train.json', y_train)
    write_json_to_file('data/y_val.json',   y_val)
    write_json_to_file('data/y_test.json',  y_test)

if __name__ == '__main__':
    main()