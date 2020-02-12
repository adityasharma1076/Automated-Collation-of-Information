# Automated-Collation-of-Information

1. Scripts which retrieves data on daily basis:
ACM_Today - technews.acm.org
IEEE_Today - spectrum.ieee.org
MIT_Todat - news.mit.edu
Science_Daily_Today - sciencedaily.com
Stanford_Today - news.stanford.edu

2. model.ipynb
  a. Text Cleaning/Preprocessing using NLTK,string,re Python Modules
  b. Reduction in Categories
  c. Training Machine Learning Model using Naive Bayes and SGD Classifier
  d. Saved This Model in .pkl file.

3. Combined_Today.ipynb
  a. Prioritised the freshly scraped Data with the help of predicted probablities from our model('NaiveBayes_model_5.pkl')
  b. Saved top 10 articles, which are emailed with the help of SMTP Library in Simple_Mail_Script.ipynb
