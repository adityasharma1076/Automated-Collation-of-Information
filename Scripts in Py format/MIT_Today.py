
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


def fix_url(url_t):
    prefix = 'http://news.mit.edu'
    
    return (prefix+url_t)


# In[4]:


MIT = pd.read_csv('MIT_Text')
#MIT.drop(['Unnamed: 0'],axis=1,inplace=True)
MIT = MIT[['Source','Heading','Category','Date','Time','URL','Text']]

outname ='MIT_Text'

root = 'Backup/'
if not os.path.exists(root):
    os.mkdir(root)
date_today= Today_date +'/'
outdir=root+ date_today[:-1]
if not os.path.exists(outdir):
    os.mkdir(outdir)
fullname = os.path.join(outdir, outname)

MIT.to_csv(fullname,index=False, encoding='utf-8')

# In[5]:


link = 'http://news.mit.edu/'
res = requests.get(link)
soup=bs4.BeautifulSoup(res.text,'lxml')


# In[6]:


List1 = ['http://news.mit.edu/topic/algorithms',
        'http://news.mit.edu/topic/computer-vision',
        'http://news.mit.edu/topic/machine-learning',
        'http://news.mit.edu/topic/big-data',
        'http://news.mit.edu/topic/software',
        'http://news.mit.edu/topic/cyber-security',
        'http://news.mit.edu/topic/networks',
        'http://news.mit.edu/topic/natural-language-processing',
        'http://news.mit.edu/topic/web-development',
        'http://news.mit.edu/topic/computers',
         'http://news.mit.edu/engineering']
       
List2 =['http://news.mit.edu/topic/robotics',
       'http://news.mit.edu/topic/electronics',
       'http://news.mit.edu/topic/research',
       'http://news.mit.edu/topic/nanotech',
       'http://news.mit.edu/topic/nasa']


# In[7]:


def get_records(content_d,category):
    temp_records = []
    for temp_record in content_d:
        URL = fix_url(temp_record.find('a')['href'])
        Heading = temp_record.find('h3').text
        #Summary = temp_record.find('p').text
        Date = temp_record.find('em').text
        Category = category
        Source = 'MIT News'
        Time = '-'
        Text = ''
        temp_records.append((Source,Heading,Category,Date,Time,URL,Text))
    return temp_records   


# In[8]:


records = []
for list_element in List1:
    category = 'Computer Science'
    
    list_element_url = list_element
    res_element = requests.get(list_element_url)
    soup_element=bs4.BeautifulSoup(res_element.text,'lxml')
    content = soup_element.find('ul',{'class':'view-news-items'}).findAll('li')
    rec = get_records(content,category)
    records.append(rec)
    

for list_element in List2:
    category = str.split(list_element,'/')[-1]
    
    list_element_url = list_element
    res_element = requests.get(list_element_url)
    soup_element=bs4.BeautifulSoup(res_element.text,'lxml')
    content = soup_element.find('ul',{'class':'view-news-items'}).findAll('li')
    rec = get_records(content,category.capitalize())
    records.append(rec)


# In[9]:


flat_list = []
for sublist in records:
    for item in sublist:
        flat_list.append(item)


# In[10]:


df=pd.DataFrame(flat_list,columns=['Source','Heading','Category','Date','Time','URL','Text'])
df['Date'] = pd.to_datetime(df['Date'])


# In[11]:


df


# In[12]:


df = df.drop_duplicates(subset='Heading',keep='last').reset_index(drop=True)


# In[13]:


s1 = pd.merge(MIT, df, how='inner', on=['Heading'])
Headings = s1['Heading']

def fix_heading(x):
    for i in Headings:
        if(i==x):
            return 'nil'
    return x
df['Heading'] = df['Heading'].apply(fix_heading)


# In[14]:


df = df[df['Heading']!='nil']
df


# In[15]:


def fix_text(x):
    try:
        res = requests.get(x,headers={'User-Agent': 'Mozilla/5.0'})
        soup = bs4.BeautifulSoup(res.text,'lxml')
    
        txt = soup.find('div',{'class':'field-item'}).text
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
    


# In[16]:


MIT


# In[17]:


temp = MIT.append(df,sort=True)
temp['Date'] = pd.to_datetime(temp['Date'])
temp = temp.sort_values(by=['Date'],ascending=False).reset_index().drop(['index'],axis=1)
temp.to_csv('MIT_Text')


# In[18]:


temp


# In[19]:


outname ='MIT-'+str(Today_date)+'.csv'
root = 'Uncategorized Data/'
if not os.path.exists(root):
    os.mkdir(root)
date_today= Today_date +'/'
outdir=root+ date_today[:-1]
if not os.path.exists(outdir):
    os.mkdir(outdir)
fullname = os.path.join(outdir, outname)


# In[20]:


df.to_csv(fullname,index=False,encoding='utf-8')


# In[21]:


Today_date

