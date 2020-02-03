import sklearn_crfsuite
import spacy
import re

class AddressModel2(object):
    def __init__(self):
        self.crf = sklearn_crfsuite.CRF( algorithm='lbfgs', c1=0.1, c2=0.1,max_iterations=100, all_possible_transitions=True)
        self.nlp = spacy.load("en_core_web_sm")
        self.desired_ents = ["FAC", "LOC"]
        
        self.death_terms = ["killed", "death", "died", "fatal"]
        self.injured_terms = ["hurt", "shot", "injured", "hospitalized", "wounded"]
        self.crime_terms = ["robbed", "stole"]

        #roads = ["Rd", "St", "Ave", "Blvd", "Ln", "Dr", "Ter", "Pl", "Ct"]
        roads = ["Road", "Street", "Avenue", "Boulevard", "Lane", "Drive", "Terrace", "Place", "Court", "Circle"]

        addr_regex1 = r"[0-9]* block of( [^ ]*){1,2} (" + "|".join(roads) + ")"
        addr_regex2 = r"[0-9]+( [^ ]*){1,2} (" + "|".join(roads) + ")"
        addr_regex3 = r"([A-Z][\S]* ){1,2}(" + "|".join(roads) + r") and ([A-Z][\S]* ){1,2}(" + "|".join(roads) + ")"
        self.addr_regex = "(" + addr_regex1 + "|" + addr_regex2 + "|" + addr_regex3 + ")"

    def __sent_tokenize(self, text):
        doc = self.nlp(text)
        sentences = [sent.string.strip() for sent in doc]
        return sentences


    # loc is 1 if sentence contains at least 1 location
    # 0 otherwise
    def __sent2features(self, sent, loc):
        doc = self.nlp(sent)

        features = {
            "death_terms": sum([1 if w.text in self.death_terms else 0 for w in doc]),
            "injured_terms": sum([1 if w.text in self.injured_terms else 0 for w in doc]),
            "location": loc,
            "contains_addr": 1 if re.search(self.addr_regex, doc.text) else 0,
            "crime_terms": sum([1 if w.text in self.crime_terms else 0 for w in doc])
        }
        return features

    def __filter_ents(self, span):
        candidates = list(filter(lambda x: x.label_ in self.desired_ents, span.ents))
        for idx, x in enumerate(candidates):
            x = x.text
            if x[0:3] == "the":
                candidates[idx] = x[4:]
            elif x[0:2] == "at":
                candidates[idx] = x[3:]
            else:
                candidates[idx] = x
        return candidates

    def assign_label(self, num):
        arr = self.arr_labels
        idx = len(arr) - 1 if num > len(arr) - 1 else num
        return self.arr_labels[idx]

    def fit(self, X_event, y_event):
        y_train = []
        X_train = []
        for event, label in zip(X_event, y_event):
            doc = self.nlp(event["text"])
            sub_label = []
            sub_train = []
            for span in doc.sents:
                sub_label.append("CRL" if label["address"] in span.string and label["address"] != "" else "N-CRL")
                
                for token in span:
                    if token.ent_type_ in self.desired_ents:
                        sub_train.append(self.__sent2features(span.string.strip(), 1))
                        break
                else:
                    sub_train.append(self.__sent2features(span.string.strip(), 0))

            y_train.append(sub_label)
            X_train.append(sub_train)

        self.crf.fit(X_train, y_train)

    def predict_event(self, event):
        doc = self.nlp(event["text"])
        sub_train = []
        for span in doc.sents:
            for token in span:
                if token.ent_type_ in self.desired_ents:
                    sub_train.append(self.__sent2features(span.string.strip(), 1))
                    break
            else:
                sub_train.append(self.__sent2features(span.string.strip(), 0))

        X_test = [sub_train]

        y_pred = self.crf.predict(X_test)[0]
        y = self.crf.predict_marginals(X_test)[0]

        combined = []
        for i in range(len(y_pred)):
            tup = list(doc.sents)[i], y[i][y_pred[i]], y_pred[i]
            combined.append(tup)

        combined = sorted(combined, key = lambda x: x[1], reverse=True)

        # print(self.crf.predict_marginals(X_test))
        for span, _, pred in combined:
            if pred == "N-CRL": # no address here
                continue
            candidates = self.__filter_ents(span)

            addr = re.search(self.addr_regex, span.string.strip())

            if addr:
                return addr.group(0)
            elif len(candidates) != 0:
                return candidates[0]

        # do baseline when all fails
        candidates = self.__filter_ents(doc)
        if len(candidates) > 0:
            return candidates[0]
        return ""