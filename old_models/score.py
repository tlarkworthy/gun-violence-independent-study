import json
import argparse
import warnings 
from sklearn.metrics import f1_score, precision_score, recall_score

parser = argparse.ArgumentParser()

parser.add_argument('--goldfile', type=str, required=True)
parser.add_argument('--predfile', type=str, required=True)
parser.add_argument('--verbose', '-v', action='store_true')


def read_labels(file):
    with open(file) as f:
        incidents = json.load(f)

    return incidents


def compute_acc(gold, pred, field):
    num_correct = 0
    for i in range(len(gold)):
        if gold[i][field] == pred[i][field]:
            num_correct += 1

    return num_correct / len(gold)


# # use only for the address field
# def compute_f1_addr(gold, pred):
#     n_correct = 0
#     n_guessed = 0
#     for i in range(len(gold)):
#         if isinstance(pred[i]['address'], list):
#             correct = 1 if gold[i]['address'] in pred[i]['address'] else 0
#             n_correct += correct
#             n_guessed += len(pred[i]['address'])
#         else:
#             correct = 1 if gold[i]['address'] == pred[i]['address'] else 0
#             n_correct += correct
#             n_guessed += 1
#     precision = n_correct / n_guessed
#     recall = n_correct / len(gold)
#     f1 = (2 * precision * recall) / (precision + recall)
#     return f1


# def compute_f1_multinomial(gold, pred, field):
#     class_indices = {}
#     index = 0
#     for i in range(len(gold)):
#         key = gold[i][field]
#         if key not in class_indices:
#             class_indices[key] = index
#             index = index + 1

#     c_matrix = np.zeros((index + 1, index + 1))
#     for i in range(len(gold)):

def compute_macro_f1(gold, pred, field):
    y_true = [x[field] for x in gold]
    y_pred = [x[field] for x in pred]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return f1_score(y_true, y_pred, average='macro')

def compute_micro_f1(gold, pred, field):
    y_true = [x[field] for x in gold]
    y_pred = [x[field] for x in pred]
    return f1_score(y_true, y_pred, average='micro')

def compute_pr(gold, pred, field):
    y_true = [x[field] for x in gold]
    y_pred = [x[field] for x in pred]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        precision = precision_score(y_true, y_pred, average='macro')
        recall = recall_score(y_true, y_pred, average='macro')
        return precision, recall


def main(args):
    gold = read_labels(args.goldfile)
    pred = read_labels(args.predfile)

    addr_acc = compute_acc(gold, pred, "address")
    date_acc = compute_acc(gold, pred, "shooting_date")
    n_killed_acc = compute_acc(gold, pred, "n_killed")
    n_injured_acc = compute_acc(gold, pred, "n_injured")

    print()
    print("Address accuracy     : " + str(addr_acc))
    print("Date accuracy        : " + str(date_acc))
    print("Num killed accuracy  : " + str(n_killed_acc))
    print("Num injured accuracy : " + str(n_injured_acc))
    print()

    addr_f1 = compute_macro_f1(gold, pred, "address")
    date_f1 = compute_macro_f1(gold, pred, "shooting_date")
    n_killed_f1 = compute_macro_f1(gold, pred, "n_killed")
    n_injured_f1 = compute_macro_f1(gold, pred, "n_injured")

    print("Address macro f1     : " + str(addr_f1))
    print("Date macro f1        : " + str(date_f1))
    print("Num killed macro f1  : " + str(n_killed_f1))
    print("Num injured macro f1 : " + str(n_injured_f1))
    print()

    if not args.verbose:
        return 

    addr_p, addr_r = compute_pr(gold, pred, "address")
    date_p, date_r = compute_pr(gold, pred, "shooting_date")
    n_killed_p, n_killed_r = compute_pr(gold, pred, "n_killed")
    n_injured_p, n_injured_r = compute_pr(gold, pred, "n_injured")

    print("Address precision     : " + str(addr_p))
    print("Date precision        : " + str(date_p))
    print("Num killed precision  : " + str(n_killed_p))
    print("Num injured precision : " + str(n_injured_p))
    print()

    print("Address recall       : " + str(addr_r))
    print("Date recall          : " + str(date_r))
    print("Num killed recall    : " + str(n_killed_r))
    print("Num injured recall   : " + str(n_injured_r))
    print()


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)

