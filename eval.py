## Adapted from old_models/score.py

import json
import argparse
import warnings 
from sklearn.metrics import f1_score, precision_score, recall_score


parser = argparse.ArgumentParser()

parser.add_argument('--goldfile', type=str, required=True)
parser.add_argument('--predfile', type=str, required=True)
parser.add_argument('--verbose', '-v', action='store_true')
parser.add_argument('--field', '-f', type=str)


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



def compute_macro_f1(gold, pred, field):
    y_true = [0 if x[field] == '' else x[field] for x in gold]
    y_pred = [0 if x[field] is None else x[field] for x in pred]
    print(y_true)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return f1_score(y_true, y_pred, average='macro')

def compute_micro_f1(gold, pred, field):
    y_true = [0 if x[field] == '' else x[field] for x in gold]
    y_pred = [0 if x[field] is None else x[field] for x in pred]
    return f1_score(y_true, y_pred, average='micro')

def compute_pr(gold, pred, field):
    y_true = [0 if x[field] == '' else x[field] for x in gold]
    y_pred = [0 if x[field] is None else x[field] for x in pred]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        precision = precision_score(y_true, y_pred, average='macro')
        recall = recall_score(y_true, y_pred, average='macro')
        return precision, recall


def main(args):
    gold = read_labels(args.goldfile)
    pred = read_labels(args.predfile)


    # state_acc = compute_acc(gold, pred, "state")
    # state_f1 = compute_macro_f1(gold, pred, "state")
    # state_p, state_r = compute_pr(gold, pred, "state")

    # print()
    # print("State accuracy   : " + str(state_acc))
    # print("State macro f1   : " + str(state_f1))
    # print("State precision  : " + str(state_p))
    # print("State recall : " + str(state_r))
    # print()

    acc = compute_acc(gold, pred, args.field)
    f1 = compute_macro_f1(gold, pred, args.field)
    p, r = compute_pr(gold, pred, args.field)

    print()
    print("accuracy   : " + str(acc))
    print("macro f1   : " + str(f1))
    print("precision  : " + str(p))
    print("recall : " + str(r))
    print()

    # addr_acc = compute_acc(gold, pred, "address")
    # date_acc = compute_acc(gold, pred, "shooting_date")
    # n_killed_acc = compute_acc(gold, pred, "n_killed")
    # n_injured_acc = compute_acc(gold, pred, "n_injured")

    # print()
    # print("Address accuracy     : " + str(addr_acc))
    # print("Date accuracy        : " + str(date_acc))
    # print("Num killed accuracy  : " + str(n_killed_acc))
    # print("Num injured accuracy : " + str(n_injured_acc))
    # print()

    # addr_f1 = compute_macro_f1(gold, pred, "address")
    # date_f1 = compute_macro_f1(gold, pred, "shooting_date")
    # n_killed_f1 = compute_macro_f1(gold, pred, "n_killed")
    # n_injured_f1 = compute_macro_f1(gold, pred, "n_injured")

    # print("Address macro f1     : " + str(addr_f1))
    # print("Date macro f1        : " + str(date_f1))
    # print("Num killed macro f1  : " + str(n_killed_f1))
    # print("Num injured macro f1 : " + str(n_injured_f1))
    # print()

    # if not args.verbose:
    #     return 

    # addr_p, addr_r = compute_pr(gold, pred, "address")
    # date_p, date_r = compute_pr(gold, pred, "shooting_date")
    # n_killed_p, n_killed_r = compute_pr(gold, pred, "n_killed")
    # n_injured_p, n_injured_r = compute_pr(gold, pred, "n_injured")

    # print("Address precision     : " + str(addr_p))
    # print("Date precision        : " + str(date_p))
    # print("Num killed precision  : " + str(n_killed_p))
    # print("Num injured precision : " + str(n_injured_p))
    # print()

    # print("Address recall       : " + str(addr_r))
    # print("Date recall          : " + str(date_r))
    # print("Num killed recall    : " + str(n_killed_r))
    # print("Num injured recall   : " + str(n_injured_r))
    # print()


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)