# Automated-Collation-of-Information

1. Scripts which retrieves data on daily basis:<br />
ACM_Today - technews.acm.org<br />
IEEE_Today - spectrum.ieee.org<br />
MIT_Todat - news.mit.edu<br />
Science_Daily_Today - sciencedaily.com<br />
Stanford_Today - news.stanford.edu<br />

2. model.ipynb<br />
  a. Text Cleaning/Preprocessing using NLTK,string,re Python Modules<br />
  b. Reduction in Categories<br />
  c. Training Machine Learning Model using Naive Bayes and SGD Classifier<br />
  d. Saved This Model in .pkl file.<br />

3. Combined_Today.ipynb<br />
  a. Prioritised the freshly scraped Data with the help of predicted probablities from our model('NaiveBayes_model_5.pkl')<br />
  b. Saved top 10 articles, which are emailed with the help of SMTP Library in Simple_Mail_Script.ipynb<br />
