
# coding: utf-8

# In[1]:


import bs4 
import requests
import pandas as pd
import numpy as np
import os


# In[2]:


import datetime

now = datetime.datetime.now()


Today_time = now.strftime("%H:%M")

Today_date = now.strftime("%Y-%m-%d")


# In[3]:


year = now.strftime("%Y")

def get_date(date):
    if(date[-1]=='—'):
        date=date[:-2]
    if '.' in date:
        spl = str.split(date,'.')
        date = spl[0]+spl[1]
    else:
        spl = str.split(date)
        date = spl[0]+' '+spl[1]+' '+spl[2]
    spl = str.split(date,' ')
    date = spl[0]+' '+spl[1]+' '+spl[2]
    return date

def get_url(Url):
    prefix = 'https://www.sciencedaily.com'
    return prefix+Url

def get_cat(soup):
    z = str.split(soup.find('div',{'id':'title'}).text)[:-1]
    cat= ''
    for i in z:
        cat=cat+' '+i
    return cat


# In[4]:


List_SD = [#'https://www.sciencedaily.com/news/health_medicine/',
       'https://www.sciencedaily.com/news/mind_brain/',
       #'https://www.sciencedaily.com/news/living_well/',
       'https://www.sciencedaily.com/news/matter_energy/',
       'https://www.sciencedaily.com/news/space_time/',
       'https://www.sciencedaily.com/news/computers_math/',
       #'https://www.sciencedaily.com/news/plants_animals/',
       'https://www.sciencedaily.com/news/earth_climate/',
       #'https://www.sciencedaily.com/news/fossils_ruins/',
       'https://www.sciencedaily.com/news/science_society/',
       'https://www.sciencedaily.com/news/business_industry/',
       'https://www.sciencedaily.com/news/education_learning/']


# In[5]:


records = []
for link in List_SD:
    res = requests.get(link,headers={'User-Agent': 'Mozilla/5.0'})
    soup = bs4.BeautifulSoup(res.text,'lxml')
    tab_pane = soup.findAll('div',{'class':'tab-pane'})
    category = get_cat(soup)
    for record in tab_pane[:10]:
        Category=category[1:]
        Heading = record.find('h3').text
        URL = get_url(record.find('a')['href'])
        Date = get_date(record.find('span').text)
        Source = 'Science Daily'
        Time = '-'
        records.append((Source,Heading,Category,Date,Time,URL))


# In[6]:


df=pd.DataFrame(records,columns=['Source','Heading','Category','Date','Time','URL'])
df['Date'] = pd.to_datetime(df['Date'])


# In[7]:


df.head()


# In[8]:


science_daily = pd.read_csv('SD_Text')
science_daily = science_daily[['Source','Heading','Category','Date','Time','URL','Text']]

outname ='SD_Text'
root = 'Backup/'
if not os.path.exists(root):
    os.mkdir(root)
date_today= Today_date +'/'
outdir=root+ date_today[:-1]
if not os.path.exists(outdir):
    os.mkdir(outdir)
fullname = os.path.join(outdir, outname)

science_daily.to_csv(fullname,index=False, encoding='utf-8')

# In[9]:


s1 = pd.merge(science_daily, df, how='inner', on=['Heading'])
Headings = s1['Heading']

def fix_heading(x):
    for i in Headings:
        if(i==x):
            return 'nil'
    return x
df['Heading'] = df['Heading'].apply(fix_heading)
df = df[df['Heading']!='nil']

# In[10]:


def fix_text(x):
    res = requests.get(x,headers={'User-Agent': 'Mozilla/5.0'})
    soup = bs4.BeautifulSoup(res.text,'lxml')
    try:
        txt = soup.find('div',{'id':'text'}).text
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


# In[11]:


temp = science_daily.append(df,sort=True)
temp['Date'] = pd.to_datetime(temp['Date'])
temp = temp.sort_values(by=['Date'],ascending=False).reset_index().drop(['index'],axis=1)
temp = temp[['Source','Heading','Category','Date','Time','URL','Text']]

# In[12]:


temp.to_csv('SD_Text')


# In[13]:


outname ='Science_Daily-'+str(Today_date)+'.csv'
root = 'Uncategorized Data/'
if not os.path.exists(root):
    os.mkdir(root)
date_today= Today_date +'/'
outdir=root+ date_today[:-1]
if not os.path.exists(outdir):
    os.mkdir(outdir)
fullname = os.path.join(outdir, outname)




# In[14]:


df.to_csv(fullname,index=False,encoding='utf-8')



