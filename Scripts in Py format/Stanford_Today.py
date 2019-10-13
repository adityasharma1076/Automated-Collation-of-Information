
# coding: utf-8

# In[1]:


import bs4 
import requests
import pandas as pd
import numpy as np
import os

import warnings
warnings.filterwarnings("ignore")

# In[2]:


import datetime

now = datetime.datetime.now()


Today_time = now.strftime("%H:%M")

Today_date = now.strftime("%Y-%m-%d")


# In[3]:



year = now.strftime("%Y")

def get_date(date):
    x = str.split(date,'\xa0')
    if(len(x)==3):
        Date = x[1]+' '+x[0]+', '+x[2]
    else:
        Date = x[1]+' '+x[0]+', '+year
    return Date


# In[4]:


url = 'https://news.stanford.edu/'
res = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
soup = bs4.BeautifulSoup(res.text,'lxml')


# In[5]:


cat = ['Science & Technology', 'Health', 'Social Sciences', 'Humanities',
       'Environment', 'International', 'Cybersecurity', 'Entrepreneurship','Undergraduate']


# In[6]:


content = soup.findAll('article')
records = []
for record in content:
    URL = record.find('a')['href']
    Heading = record.find('h3').text
    Text = record.find('p').text
    Date = Today_date
    Time='-'
    Category = record.find('div',{'class':'meta'}).text
    
    Source = 'Stanford'
    if Category in cat:
        
        records.append((Source,Heading,Category,Date,Time,URL,Text))


# In[7]:


df=pd.DataFrame(records,columns=['Source','Heading','Category','Date','Time','URL','Text'])
df['Date'] = pd.to_datetime(df['Date'])


# In[8]:


df


# In[9]:


stanford = pd.read_csv('STN_Text')
stanford = stanford[['Source','Heading','Category','Date','Time','URL','Text']]
#stanford = stanford.drop(['Unnamed: 0'],axis=1)

outname ='STN_Text'
root = 'Backup/'
if not os.path.exists(root):
    os.mkdir(root)
date_today= Today_date +'/'
outdir=root+ date_today[:-1]
if not os.path.exists(outdir):
    os.mkdir(outdir)
fullname = os.path.join(outdir, outname)

stanford.to_csv(fullname,index=False, encoding='utf-8')
# In[10]:


s1 = pd.merge(stanford, df, how='inner', on=['Heading'])
Headings = s1['Heading']

def fix_heading(x):
    for i in Headings:
        if(i==x):
            return 'nil'
    return x
df['Heading'] = df['Heading'].apply(fix_heading)


# In[11]:


df = df[df['Heading']!='nil']
df.head()


# In[12]:


def fix_text(x):
    try:
        res = requests.get(x,headers={'User-Agent': 'Mozilla/5.0'})
        soup = bs4.BeautifulSoup(res.text,'lxml')
    
        txt = soup.find('div',{'id':'story-content'}).text
    except:
        try:
            res = requests.get(x,headers={'User-Agent': 'Mozilla/5.0'})
            soup = bs4.BeautifulSoup(res.text,'lxml')

            txt = soup.find('div',{'class':'group-p-ws-style'}).text
        except:
            return '-'
    n = str.split(txt,'\n')
    a = ''
    for i in n:
        a=a+' '+i
        
    o = str.split(a,'\xa0')
    b = ''
    for i in o:
        b=b+' '+i
    return b    

df['Text'] = df['URL'].apply(fix_text)


# In[13]:


df


# In[14]:


temp = stanford.append(df,sort=True)
temp['Date'] = pd.to_datetime(temp['Date'])
temp = temp.sort_values(by=['Date'],ascending=False).reset_index().drop(['index'],axis=1)
temp = temp[['Source','Heading','Category','Date','Time','URL','Text']]
temp.to_csv('STN_Text')


# In[15]:


outname ='Stanford-'+str(Today_date)+'.csv'
root = 'Uncategorized Data/'
if not os.path.exists(root):
    os.mkdir(root)
date_today= Today_date +'/'
outdir=root+ date_today[:-1]
if not os.path.exists(outdir):
    os.mkdir(outdir)
fullname = os.path.join(outdir, outname)


# In[16]:


df.to_csv(fullname,index=False,encoding='utf-8')

