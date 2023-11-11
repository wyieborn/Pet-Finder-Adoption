#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 


# In[2]:


file_path = r"C:\Users\aleja\jupyter python data perro\pets\train.csv" # Assuming the file is named 'train.csv'


# In[5]:


file_path_test = r"C:\Users\aleja\jupyter python data perro\pets\test.csv" # Assuming the file is named 'train.csv'


# In[14]:


data = pd.read_csv(file_path)


# In[7]:


data.head()


# In[13]:


data_test = pd.read_csv(file_path_test)


# In[15]:


data_test.head()


# In[8]:


import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


# In[9]:


nltk.download('vader_lexicon')


# In[10]:


sia = SentimentIntensityAnalyzer()


# In[11]:


data['Description'] = data['Description'].astype(str).fillna("No description")


# In[20]:


data['Description'] = data['Description'].astype(str).fillna('')


# In[21]:


data['sentiments'] = data['Description'].apply(lambda x: sia.polarity_scores(x))


# In[22]:


data['compound'] = data['sentiments'].apply(lambda x: x['compound'])


# In[23]:


print(data[['Description', 'compound']].head())


# In[24]:


data_test['Description'] = data_test['Description'].astype(str).fillna("No description")


# In[25]:


data_test['Description'] = data_test['Description'].astype(str).fillna('')


# In[26]:


data_test['sentiments'] = data_test['Description'].apply(lambda x: sia.polarity_scores(x))


# In[27]:


data_test['compound'] = data_test['sentiments'].apply(lambda x: x['compound'])


# In[28]:


print(data_test[['Description', 'compound']].head())


# In[29]:


train_file_path = r'C:\Users\aleja\jupyter python data perro\pets\train.csv'
test_file_path = r'C:\Users\aleja\jupyter python data perro\pets\test.csv'  


# In[30]:


train = pd.read_csv(train_file_path)
test = pd.read_csv(test_file_path)


# In[31]:


def get_polarity(text):
    return TextBlob(text).sentiment.polarity

def get_subjectivity(text):
    return TextBlob(text).sentiment.subjectivity


# In[33]:


from textblob import TextBlob


# In[34]:


train['polarity'] = train['Description'].astype(str).apply(get_polarity)
train['subjectivity'] = train['Description'].astype(str).apply(get_subjectivity)

test['polarity'] = test['Description'].astype(str).apply(get_polarity)
test['subjectivity'] = test['Description'].astype(str).apply(get_subjectivity)


# In[35]:


print(train[['Description', 'polarity', 'subjectivity']].head())
print(test[['Description', 'polarity', 'subjectivity']].head())


# In[ ]:




