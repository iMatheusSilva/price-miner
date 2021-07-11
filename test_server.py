#!/usr/bin/python3
# coding: utf-8


import pandas as pd

data = {'Name': ['Tom', 'Joseph', 'Krish', 'John'], 'Age': [20, 21, 19, 18]}

df = pd.DataFrame(data)

df.to_html('funcionou.html')
