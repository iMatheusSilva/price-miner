#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd

data = {'Name': ['Tom', 'Joseph', 'Krish', 'John'], 'Age': [20, 21, 19, 18]}  
  
# Create DataFrame  
df = pd.DataFrame(data)  

df.to_html('funcionou.html')


# In[ ]:




