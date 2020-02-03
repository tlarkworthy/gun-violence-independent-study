import json
import random
import spacy

def load(file):
    with open(file) as json_file:
        data = json.load(json_file)
    return data


def pred_state(words):
    for i in range(len(words)):
        if words[i] in special and i < len(words) and (words[i] + " " + words[i + 1]) in two_word_states:
            return words[i] + " " + words[i + 1]
        elif words[i] in raw_states:
            return words[i]
        elif words[i] in abbvs:
            return abbvs_to_states[words[i]]
        elif words[i] in ap_abbvs_to_states.keys():
            return ap_abbvs_to_states[words[i]]
        elif i == len(words) - 1:
            return random.choice(raw_states) # randomly guess if no information in the article

def predict(data):
    predictions = []

    for event in data:
        event_pred = {}
        words = event["text"].split()
        event_pred["state"] = pred_state(words)
        predictions.append(event_pred)
        

    return predictions

def pred_state_adv(data, nlp):
    predictions = []

    # "GPE" for cities, counties, states

    for event in data:
        event_pred = {}
        # words = event["text"].split()
        
        doc = nlp(event["text"])
    
        for span in doc.sents:
            for token in span:
                if token.ent_type_ == "GPE":
                    event_pred["state"] = token
                    break

        # event_pred["state"] = pred_state(words)
        predictions.append(event_pred)
    
    return predictions


raw_states = "Alabama, Alaska, Arizona, Arkansas, California, Colorado, Connecticut, Delaware, Florida, Georgia, Hawaii, Idaho, Illinois, Indiana, Iowa, Kansas, Kentucky, Louisiana, Maine, Maryland, Massachusetts, Michigan, Minnesota, Mississippi, Missouri, Montana, Nebraska, Nevada, New Hampshire, New Jersey, New Mexico, New York, North Carolina, North Dakota, Ohio, Oklahoma, Oregon, Pennsylvania, Rhode Island, South Carolina, South Dakota, Tennessee, Texas, Utah, Vermont, Virginia, Washington, West Virginia, Wisconsin, Wyoming".split(sep=", ")
special = ["New", "South", "Rhode", "West"]
two_word_states = ["New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Rhode Island", "South Dakota", "South Carolina", "West Virginia"]
abbvs = "AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY".split()

ap_abbvs_to_states = {
    "Ala.": "Alabama",
    "Ariz.": "Arizona",
    "Ark.": "Arkansas",
    "Calif.": "California",
    "Colo.": "Colorado",
    "Conn.": "Connecticut",
    "Del.": "Delaware",
    "Fla.": "Florida",
    "Ga.": "Georgia",
    "Ill.": "Illinois",
    "Ind.": "Indiana",
    "Kan.": "Kansas",
    "Ky.": "Kentucky",
    "La.": "Louisiana",
    "Md.": "Maryland",
    "Mass.": "Massachusetts",
    "Mich.": "Michigan",
    "Minn.": "Minnesota",
    "Miss.": "Mississippi",
    "Mo.": "Missouri",
    "Mont.": "Montana",
    "Neb.": "Nebraska",
    "Nev.": "Nevada",
    "N.H.": "New Hampshire",
    "N.J.": "New Jersey",
    "N.M.": "New Mexico",
    "N.Y.": "New York",
    "N.C.": "North Carolina",
    "N.D.": "North Dakota",
    "Okla.": "Oklahoma",
    "Ore.": "Oregon",
    "Pa.": "Pennsylvania",
    "R.I.": "Rhode Island",
    "S.C.": "South Carolina",
    "S.D.": "South Dakota",
    "Tenn.": "Tennessee",
    "Vt.": "Vermont",
    "Va.": "Virginia",
    "Wash.": "Washington",
    "W. Va.": "West Virginia",
    "Wis.": "Wisconsin",
    "Wyo.": "Wyoming"
}

abbvs_to_states = dict(zip(abbvs, raw_states))
# print(abbvs_to_states)

def run():
    nlp = spacy.load("en_core_web_sm")
    X_test = load("./data/X_test.json")

    pred = predict(X_test)
    
    return json.dumps(pred)

print(run())