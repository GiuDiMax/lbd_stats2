import pandas as pd
import pickle

with open('watch', 'rb') as file:
    watch = pickle.load(file)
with open('diary', 'rb') as file:
    diary = pickle.load(file)
with open('links', 'rb') as file:
    links = pickle.load(file)

