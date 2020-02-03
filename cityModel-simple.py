import json
import spacy


def load(file):
    with open(file) as json_file:
        data = json.load(json_file)
    return data


def predict(data, nlp):
    predictions = []

    for event in data:
        event_pred = {}

        event_pred["city_or_county"] = pred_city(event, nlp)

        predictions.append(event_pred)

    return predictions


def pred_city(event, nlp):

    doc = nlp(event["text"])

    for span in doc.sents:
        for tok in span:
            if tok.ent_type_ == "GPE":
                return str(tok).title()


def run():
    X_test = load("./data/X_test.json")
    nlp = spacy.load("en_core_web_sm")

    pred = predict(X_test, nlp)
    
    return json.dumps(pred)

print(run())