
# coding: utf-8

# In[1]:


import bs4 
import requests
import pandas as pd
import numpy as np
import os
import requests
import re

import warnings
warnings.filterwarnings("ignore")

# In[2]:


import datetime

now = datetime.datetime.now()


Today_time = now.strftime("%H:%M")

Today_date = now.strftime("%Y-%m-%d")


# In[3]:


def get_date(date):
    dt = re.findall('[A-Z][^A-Z]*', date)[-1]
    return dt

def fix_n(x):
    x = x.replace('\n', ' ')
    
    if('Full Article' in x):
        x=x.replace('Full Article', ' ')
    return x


# In[4]:


url = 'https://technews.acm.org/'
res = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
soup = bs4.BeautifulSoup(res.text,'html.parser')


# In[5]:


text = soup.findAll('div',{'class':'desktopFontSize'})
text = text[2:]


# In[6]:


records = []
for i in range(len(text)):
    Heading = fix_n(text[i].find('b').text)
    Date = get_date(fix_n(text[i].find('i').text))
    Time = '-'
    URL = text[i].findAll('a')[-1]['href']
    Text = fix_n(text[i].text)
    Source = 'ACM'
    Category = 'ACM'
    records.append((Source,Heading,Category,Date,Time,URL,Text))


# In[7]:


df=pd.DataFrame(records,columns=['Source','Heading','Category','Date','Time','URL','Text'])
df['Date'] = pd.to_datetime(df['Date'])


# In[8]:


df


# In[9]:


ACM = pd.read_csv('ACM_Text')
outname ='ACM_Text'

root = 'Backup/'
if not os.path.exists(root):
    os.mkdir(root)
date_today= Today_date +'/'
outdir=root+ date_today[:-1]
if not os.path.exists(outdir):
    os.mkdir(outdir)
fullname = os.path.join(outdir, outname)

ACM.to_csv(fullname,index=False, encoding='utf-8')

# In[10]:


s1 = pd.merge(ACM, df, how='inner', on=['Heading'],sort=True)


# In[11]:


Headings = s1['Heading']

def fix_heading(x):
    for i in Headings:
        if(i==x):
            return 'nil'
    return x
df['Heading'] = df['Heading'].apply(fix_heading)
df = df[df['Heading']!='nil']
df.head()


# In[12]:


temp = ACM.append(df,sort=True)
temp['Date'] = pd.to_datetime(temp['Date'])
temp = temp.sort_values(by=['Date'],ascending=False).reset_index().drop(['index'],axis=1)
temp=temp[['Source','Heading','Category','Date','Time','URL','Text']]

# In[13]:


temp.to_csv('ACM_Text')


# In[14]:


outname ='ACM-'+str(Today_date)+'.csv'
root = 'Uncategorized Data/'
if not os.path.exists(root):
    os.mkdir(root)
date_today= Today_date +'/'
outdir=root+ date_today[:-1]
if not os.path.exists(outdir):
    os.mkdir(outdir)
fullname = os.path.join(outdir, outname)


# In[15]:


df.to_csv(fullname,index=False,encoding='utf-8')


# In[16]:


fullname
