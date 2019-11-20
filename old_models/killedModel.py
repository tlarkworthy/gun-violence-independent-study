
import sklearn_crfsuite
import spacy

class KilledModel(object):
    def __init__(self, killed=True):
        self.crf = sklearn_crfsuite.CRF( algorithm='lbfgs', c1=0.1, c2=0.1,max_iterations=100, all_possible_transitions=True)
        self.nlp = spacy.load("en_core_web_sm")
        injured_labels = ["O-INJ", "1-INJ", "2-INJ", "3-INJ", "4-INJ"]
        killed_labels = ["0-KILL", "1-KILL", "2-KILL", "3-KILL", "4-KILL"]
        self.field = "n_killed" if killed else "n_injured"
        self.arr_labels = killed_labels if killed else injured_labels
        self.killed =  killed

        #0.6585365853658537
        #0.17073170731707318 simple-baseline injured acc
        #0.3170731707317073  injured 
        #0.3170731707317073


    def __sent_tokenize(self, text):
        doc = self.nlp(text)
        sentences = [sent.string.strip() for sent in doc]
        return sentences


    def __sent2features(self, sent, num):
        doc = self.nlp(sent)
        death_terms = ["killed", "death", "died", "shot", "fatal"]
        injured_terms = ["hurt", "shot", "injured", "hospitalized", "wounded"]

        features = {
            "death_terms": sum([1 if w in death_terms else 0 for w in doc.text]),
            "injured_terms": sum([1 if w in injured_terms else 0 for w in doc.text]),
            "int_number": int(num) if num.isdigit() else 0,
            "str_number": num if not num.isdigit() else "" 
        }
        return features

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
                for token in span:
                    if token.pos_ == "NUM":
                        al = self.assign_label(label[self.field])
                        sub_label.append(al)
                        sub_train.append(self.__sent2features(span.string.strip(), token.text))
                        break
                else:
                    sub_label.append(self.arr_labels[0])
                    sub_train.append(self.__sent2features(span.string.strip(), "0"))

            y_train.append(sub_label)
            X_train.append(sub_train)

        self.crf.fit(X_train, y_train)

    def predict_event(self, event):
        doc = self.nlp(event["text"])
        sub_train = []
        for span in doc.sents:
            for token in span:
                if token.pos_ == "NUM":
                    sub_train.append(self.__sent2features(span.string.strip(), token.text))
                    break
            else:
                sub_train.append(self.__sent2features(span.string.strip(), "0"))

        X_test = [sub_train]

        y_pred = self.crf.predict(X_test)
        n_killed = [self.arr_labels.index(label) for label in y_pred[0]]
        return max(n_killed)

    # def predict(self, X_events):
    #     return [self.__predict_event(event) for event in X_events]



    





