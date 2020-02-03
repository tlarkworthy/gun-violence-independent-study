import sklearn_crfsuite
import spacy
import sys
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier

class KilledModelExtension(object):
    def __init__(self, killed=True):
        self.model = SVC()
        self.nlp = spacy.load("en_core_web_sm")
        injured_labels = ["O-INJ", "1-INJ", "2-INJ", "3-INJ", "4-INJ"]
        killed_labels = ["0-KILL", "1-KILL", "2-KILL", "3-KILL", "4-KILL"]
        self.field = "n_killed" if killed else "n_injured"
        self.arr_labels = killed_labels if killed else injured_labels
        self.killed =  killed

    def assign_label(self, num):
        arr = self.arr_labels
        idx = len(arr) - 1 if num > len(arr) - 1 else num
        return self.arr_labels[idx]

    def __cardinal2number(self, card):
        num = card.lower()
        d = { 'zero': 0,
              'one': 1,
              'two': 2,
              'three': 3,
              'four': 4,
              'five': 5,
              'six': 6,
              'seven': 7,
              'eight': 8,
              'nine': 9,
              'ten': 10 }
        if num in d:
            return d[num]
        else:
            return -1

    def __doc2features(self, doc):
        death_terms = ["kill", "death", "dead", "died", "die", "fatal", "fatally", "killed", "deceased"]
        injured_terms = ["hurt", "shot", "injured", "injuries", "injury", "hospital", "wound", "wounds", "wounded", "hospitalized"]
        prison_terms = ["prison", "sentenced", "charged", "penalty", "ordered"]
        single_terms = ["victim", "name", "individual"]
        plural_terms = ["victims", "names", "others"]
        roads = ["Rd", "St", "Ave", "Blvd", "Ln", "Dr", "Ter", "Pl", "Ct"]

        int_num = 0
        str_num = 0

        unique_people = []

        for ent in doc.ents:
            contains_numbers_and_letters = any(char.isdigit() for char in ent.text) and \
                                           any(char.isalpha() for char in ent.text)

            if ent.label_ == "CARDINAL" and not contains_numbers_and_letters:
                num = ent.text
                if num.isdigit():
                    int_num = int(num)
                else:
                    str_num = self.__cardinal2number(num)
    
            elif ent.label_ == "PERSON":
                p = ent.text
                if len(p.split()) > 1:
                    lastname = p.split()[-1]
                    if lastname in roads:
                        continue
                    unique_people.append(lastname)
                else:
                    unique_people.append(p)

        unique_people = set(unique_people)

        features = [
            len(unique_people),
            sum([1 if w.text in death_terms else 0 for w in doc]),
            sum([1 if w.text in injured_terms else 0 for w in doc]),
            sum([1 if w.text in prison_terms else 0 for w in doc]),
            sum([1 if w.text in single_terms else 0 for w in doc]),
            sum([1 if w.text in plural_terms else 0 for w in doc])
        ]

        return features

    def fit(self, X_event, y_event):
        y_train = []
        X_train = []
        for event, label in zip(X_event, y_event):
            doc = self.nlp(event["text"])
            sub_label = label[self.field]
            sub_train = self.__doc2features(doc)

            y_train.append(sub_label)
            X_train.append(sub_train)

        self.model.fit(X_train, y_train)

    def predict_event(self, event):
        doc = self.nlp(event["text"])
        sub_train = self.__doc2features(doc)

        X_test = [sub_train]

        y_pred = self.model.predict(X_test)
        return int(y_pred[0])
