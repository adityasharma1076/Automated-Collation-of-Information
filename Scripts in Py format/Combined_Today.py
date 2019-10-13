
# coding: utf-8

# In[1]:


import os
import glob
import pandas as pd
from sklearn.externals import joblib
import numpy as np
import sys

import warnings
warnings.filterwarnings("ignore")

# In[2]:


import datetime

now = datetime.datetime.now()


Today_time = now.strftime("%H:%M")

Today_date = now.strftime("%Y-%m-%d")


# In[3]:


extension = 'csv'
string = 'Uncategorized Data/'+Today_date+'/*.{}'
all_filenames = [i for i in glob.glob(string.format(extension))]


# In[4]:


df = pd.concat([pd.read_csv(f) for f in all_filenames ])


# In[5]:


df = df.sort_values(by='Date',ascending=False)
df = df[df['Text']!='-']
df = df.drop_duplicates(subset='Heading',keep='last').reset_index(drop=True)


# In[6]:


df['Category'].value_counts()


# In[7]:


def fix_cat(x):
    if x[0]==' ':
        return x[1:]
    else:
        return x
df['Category'] = df['Category'].apply(fix_cat)


# In[8]:


def fix_g(x):
    if 'Q&A' in x:
        return 'nil'
    elif '3 Questions:' in x:
        return 'nil'
    else:
        return x
df['Heading'] = df['Heading'].apply(fix_g)
df = df[df['Heading']!='nil']
df = df[df['Text']!='']


# In[9]:


def fix_cat(x):
    if (x=='Cybersecurity'):
        return 'Computer Science'
    elif (x=='Living Well' or x=='Mind & Brain' or x=='Health & Medicine'):
        return 'Health'
    elif(x=='Plants & Animals' or x=='Earth & Climate'):
        return 'Environment'
    elif(x=='Business & Industry' or x=='Education & Learning' or x=='Gadgets'):
        return 'Society'
    elif(x=='NASA' or x=='Aerospace' or x=='Nasa'):
        return 'Space & Time'
    elif(x=='Research'):
        return 'Research'
    elif(x=='Telecommunications' or x=='Semiconductors' or x=='electronics' or x=='Nanoscience and nanotechnology' or x=='Green Tech' or x=='Nanotech'):
        return 'Electronics and Technology'
    elif(x=='International' or x=='Entrepreneurship' or x=='Undergraduate' or x=='Humanities'):
        return 'Others'
    elif(x=='Social Sciences' or x=='Science & Technology' or x=='Science & Society'):
        return 'Science'
    elif(x=='Fossils & Ruins' or x=='Energy'):
        return 'Matter & Energy'
    else:
        return x
    

df['Category'] = df['Category'].apply(fix_cat)


# In[10]:


df['Category'].value_counts()


# In[11]:


df=df.sort_values(by='Category')
df = df.reset_index(drop=True)


# In[12]:


temp = pd.DataFrame.copy(df)


# In[13]:


from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import re
import string
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from num2words import num2words
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')


# In[14]:


stop = ['a', 'about', 'above', 'across', 'after', 'afterwards', 'again', 'against', 'all', 'almost', 'alone',
             'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'amoungst', 'amount',
             'an', 'and', 'another', 'any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere', 'are', 'around',
             'as', 'at', 'back', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before',
             'beforehand', 'behind', 'being', 'below', 'beside', 'besides', 'between', 'beyond', 'bill', 'both',
             'bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant', 'co', 'con', 'could', 'couldnt', 'cry', 'de',
             'describe', 'detail', 'did', 'do', 'does', 'doing', 'don', 'done', 'down', 'due', 'during', 'each', 'eg',
             'eight', 'either', 'eleven', 'else', 'elsewhere', 'empty', 'enough', 'etc', 'even', 'ever', 'every', 'everyone',
             'everything', 'everywhere', 'except', 'few', 'fifteen', 'fify', 'fill', 'find', 'fire', 'first', 'five', 'for',
             'former', 'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 'further', 'get', 'give', 'go', 'had',
             'has', 'hasnt', 'have', 'having', 'he', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'hereupon',
             'hers', 'herself', 'him', 'himself', 'his', 'how', 'however', 'hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed',
             'interest', 'into', 'is', 'it', 'its', 'itself', 'just', 'keep', 'last', 'latter', 'latterly', 'least', 'less',
             'ltd', 'made', 'many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine', 'more', 'moreover', 'most', 'mostly',
             'move', 'much', 'must', 'my', 'myself', 'name', 'namely', 'neither', 'never', 'nevertheless', 'next', 'nine',
             'no', 'nobody', 'none', 'noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once',
             'one', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out', 'over', 'own',
             'part', 'per', 'perhaps', 'please', 'put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed', 'seeming',
             'seems', 'serious', 'several', 'she', 'should', 'show', 'side', 'since', 'sincere', 'six', 'sixty', 'so', 
             'some', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere', 'still', 'such', 'system',
             't', 'take', 'ten', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'thence', 'there',
             'thereafter', 'thereby', 'therefore', 'therein', 'thereupon', 'these', 'they', 'thickv', 'thin', 'third', 'this',
             'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 'to', 'together', 'too', 'top', 'toward',
             'towards', 'twelve', 'twenty', 'two', 'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we',
             'well', 'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby',
             'wherein', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', 'whoever', 'whole', 'whom',
             'whose', 'why', 'will', 'with', 'within', 'without', 'would', 'yet', 'you', 'your', 'yours', 'yourself',
             'yourselves',
       'csail','faculty','honored','society','abroad','inner','cambridge','academic','school','interdisciplinary','athlete','senior','thirty','mit','team','mit researcher','laboratory','member','student','drug','approach','professor','graduate','phd',
    ]


# In[15]:


stop_words = stopwords.words('english')
stop_words.extend(stop)
stop = set(stop_words)
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()


# In[16]:


def remove_apostrophe(data):
    return np.char.replace(data, "'", "")
def remove_punctuation(data):
    for i in (exclude):
        data = np.char.replace(data, i, ' ')
        data = np.char.replace(data, "  ", " ")
    data = np.char.replace(data, ',', '')
    return data

def convert_numbers(data):
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        try:
            w = num2words(int(w))
        except:
            a = 0
        new_text = new_text + " " + w
    new_text = np.char.replace(new_text, "-", " ")
    return new_text

def clean(data):
    stop_free = " ".join([i for i in data.lower().split() if i not in stop])
    normalized = " ".join(lemma.lemmatize(word) for word in stop_free.split())
    processed = re.sub(r"\d+","",normalized)
    #y = processed.split()
    return processed


# In[17]:


temp['Text'] = temp['Text'].apply(remove_apostrophe)
temp['Text'] = temp['Text'].apply(remove_punctuation)
temp['Text'] = temp['Text'].apply(convert_numbers)
temp['Text'] = temp['Text'].apply(clean)


# In[18]:


my_tags = temp['Category'].unique()
my_tags


# In[19]:


from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import accuracy_score
from nltk.tokenize import word_tokenize

nb_load = joblib.load('NaiveBayes_model_5.pkl')


# In[20]:

if temp.empty:
    print()
    print()
    sys.exit('NO News to Update')
y_pred = nb_load.predict(temp['Text'])


# In[21]:


all_categories= ['Computer Science',
        'Electronics and Technology',
        'Environment',
        'Health',
        'Matter & Energy',
        'Others',
        'Robotics',
        'Society',
        'Space & Time',
         'Telecom']
        


# In[22]:


weights= {
        'Computer Science':0.21,
        'Electronics and Technology':0.17,
        'Environment':0.08,
        'Health':0.04,
        'Matter & Energy':0.08,
        'Others':0.07,
        'Robotics':0.11,
        'Society':0.05,
        'Space & Time':0.10,
        'Telecom':0.09
        }


# In[23]:


#present_tags = {k: weights[k] for k in my_tags if k in weights}
#present_tags


# In[24]:


def sum(x):
    arr = np.asarray(x) * np.asarray(weights_values)
    return np.sum(arr)


# In[25]:


test_prob = nb_load.predict_proba(temp['Text'])
weights_df = pd.DataFrame(test_prob,columns=all_categories)


# In[26]:


weights_df.head()


# In[27]:


weights_values = [ v for v in weights.values() ]
weights_df['Weight'] = weights_df.apply(sum,axis=1)


temp['Category_predicted'] = y_pred
weighs = weights_df['Weight']
weighs = np.asarray(weighs)


# In[28]:


temp['weights'] = weighs


# In[29]:


df['Category_predicted']=temp['Category_predicted']
df['weights'] = temp['weights']


# In[30]:


df.sort_values(by='weights',ascending=False)


# In[31]:


df = df.sort_values(by='weights',ascending=False).reset_index(drop=True)


# In[32]:


outname =str(Today_date)+'.csv'
root = 'Prioritized Data/'
if not os.path.exists(root):
    os.mkdir(root)
date_today= Today_date +'/'
outdir=root+ date_today[:-1]
if not os.path.exists(outdir):
    os.mkdir(outdir)
fullname = os.path.join(outdir, outname)


# In[33]:


df.to_csv(fullname)


# In[34]:


col = ['Heading', 'URL']
to_print = df[col].head(12)


# In[35]:


outname =str(Today_date)+'.xlsx'
root = 'To Upload/'
if not os.path.exists(root):
    os.mkdir(root)
date_today= Today_date +'/'
outdir=root+ date_today[:-1]
if not os.path.exists(outdir):
    os.mkdir(outdir)
print_name = os.path.join(outdir, outname)


# In[36]:


to_print.to_excel(print_name)

