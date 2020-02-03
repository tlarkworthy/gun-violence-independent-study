import numpy as np
from matplotlib import pyplot as plt
import json

states = dict()

with open("data/y_test.json") as f:
    for event in json.load(f):
        if event["city_or_county"] not in states.keys():
            states[event["city_or_county"]] = 1
        else:
            states[event["city_or_county"]] += 1

with open("data/y_train.json") as f:
    for event in json.load(f):
        if event["city_or_county"] not in states.keys():
            states[event["city_or_county"]] = 1
        else:
            states[event["city_or_county"]] += 1

with open("data/y_val.json") as f:
    for event in json.load(f):
        if event["city_or_county"] not in states.keys():
            states[event["city_or_county"]] = 1
        else:
            states[event["city_or_county"]] += 1


top_five_states = sorted(list(states.keys()), key=lambda x: states[x], reverse=True)[:5]
top_five_vals = [states[x] for x in top_five_states]

plt.title("Top Five Cities by Incident Frequency")
plt.xlabel("City")
plt.ylabel("Frequency")
plt.bar(range(len(top_five_vals)), list(top_five_vals), align='center')
plt.xticks(range(len(top_five_states)), top_five_states)
plt.show()