
# coding: utf-8

# In[5]:


import requests
import time
import bs4
import pandas as pd
import time
import datetime
import os
from selenium import webdriver

import warnings
warnings.filterwarnings("ignore")

# In[2]:




import datetime

now = datetime.datetime.now()


Today_time = now.strftime("%H:%M")

Today_date = now.strftime("%Y-%m-%d")

Year = now.strftime("%Y")


# In[4]:


def get_date(date):
    x = str.split(date,'\xa0')
    if(len(x)==3):
        Date = x[1]+' '+x[0]+', '+x[2]
    else:
        Date = x[1]+' '+x[0]+', '+year
    return Date
def get_url(x):
    prefix = 'https://spectrum.ieee.org'
    url = prefix+x 
    return url

def get_text(x):
    try:
        driver.get(x)
        time.sleep(10)
        html_source = driver.page_source
        soup = bs4.BeautifulSoup(html_source, "lxml")
        Text_P = soup.findAll('p')
        Text = ''
        for i in Text_P:
            Text = Text+' ' +i.text
    except:
        Text ='-'
    return Text

def fix_text(x):
    n = str.split(x,'\n')
    a = ''
    for i in n:
        a=a+' '+i

    o = str.split(a,'\xa0')
    b = ''
    for i in o:
        b=b+' '+i


    p = str.split(b,'\t')
    c = ''
    for i in p:
        c=c+' '+i

    r = str.split(c,'\r')
    d = ''
    for i in r:
        d=d+' '+i

    s = str.split(d,'\'s')

    e=''
    for i in s:
        e=e+' '+i
    return e


# In[6]:


#from selenium.webdriver.chrome.options import Options
#Options.add_argument("--enable-features=NetworkService")
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
options.add_argument('--enable-features=NetworkServiceWindowsSandbox')
driver=webdriver.Chrome('chromedriver.exe')


# In[6]:


cat =['Robotics','Semiconductors','Aerospace','Energy','Telecommunications']


# In[7]:

driver.get('https://spectrum.ieee.org/')
time.sleep(5)
html_source = driver.page_source
soup = bs4.BeautifulSoup(html_source, "lxml")
Articles = soup.findAll('article')


# In[8]:


records = []
for article in Articles:
    try:
        Category=article.find('div')['class'][0].capitalize()
        if Category in cat :
            Source = 'IEEE'
            Date = article.find('time').text +', '+str(Year)
            Heading = article.find('h3').text
            Time='-'
            URL = get_url(article.find('a')['href'])
            Text= '-'

            records.append((Source,Heading,Category,Date,Time,URL,Text))
        else:
            continue
    except:
        continue


# In[9]:


df=pd.DataFrame(records,columns=['Source','Heading','Category','Date','Time','URL','Text'])
df['Date'] = pd.to_datetime(df['Date'])


# In[10]:


# In[11]:


df.head()


# In[12]:


ieee = pd.read_csv('IEEE_Text')


# In[13]:


ieee= ieee[ieee['Date']!='-']


# In[14]:


ieee=ieee[ieee['Text']!='-']


# In[15]:


s1 = pd.merge(ieee, df, how='inner', on=['Heading'])
Headings = s1['Heading']

def fix_heading(x):
    for i in Headings:
        if(i==x):
            return 'nil'
    return x
df['Heading'] = df['Heading'].apply(fix_heading)
df = df[df['Heading']!='nil']
df.head()

print(df)
# In[16]:

if df.empty:
    driver.close()
else:
    #df['Text'] = df['URL'].apply(get_text)
    #df['Text'] = df['Text'].apply(fix_text)
    #driver.close()

# In[17]:


#driver.quit()


# In[18]:


#ieee.sort_values(by='Date')


# In[19]:


temp = ieee.append(df)
temp['Date'] = pd.to_datetime(temp['Date'])
temp = temp.sort_values(by=['Date'],ascending=False).reset_index().drop(['index'],axis=1)
temp.drop(['Unnamed: 0'],axis=1,inplace=True)


# In[20]:


temp.to_csv('IEEE_Text')


# In[21]:


outname ='IEEE-'+str(Today_date)+'.csv'
root = 'Uncategorized Data/'
if not os.path.exists(root):
    os.mkdir(root)
date_today= Today_date +'/'
outdir=root+ date_today[:-1]
if not os.path.exists(outdir):
    os.mkdir(outdir)
fullname = os.path.join(outdir, outname)


# In[22]:


df.to_csv(fullname,index=False,encoding='utf-8')

