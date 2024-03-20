# -*- coding: utf-8 -*-
"""ytcomments.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IAkt_1sG94cjURWKBvghkoK2KlZiYzX9
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

df=pd.read_csv("/content/comments.csv")

df.head()

df=df.iloc[:,[2,4]]

df.head(2)

df.info()

df.isnull().sum()

df.dropna(axis=0,how='any',inplace=True)

df.columns

df['Sentiment']=df['Sentiment'].astype('int')

#######################################
#basic_preprocessing
#######################################

df['Comment']=df['Comment'].str.lower()

import string
string.punctuation

exclude=string.punctuation
def remove_punc(text):
  for char in exclude:
    text=text.replace(char,'')
  return text

df['Comment']=df['Comment'].apply(remove_punc)

import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords
stopwords.words('english')

def remove_stopwords(text):
  new_text=[]
  for word in text.split():
    if word in stopwords.words('english'):
      new_text.append('')
    else:
      new_text.append(word)
  x=new_text[:]
  new_text.clear()
  return " ".join(x)

df['Comment']=df['Comment'].apply(remove_stopwords)

from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

def stem_words(text):
  return " ".join([ps.stem(word) for word in text.split()])

df['Comment']=df['Comment'].apply(stem_words)

####################################################
#EDA
####################################################

plt.pie(df['Sentiment'].value_counts(), labels=['negative','neutral','positive'],autopct="%0.2f")
plt.show()

import nltk

nltk.download('punkt')

df['total_characters']=df['Comment'].apply(len)

df.head(2)

df['total_words'] = df['Comment'].apply(lambda x:len(nltk.word_tokenize(x)))

df.head(2)

df['total_sentences'] = df['Comment'].apply(lambda x:len(nltk.sent_tokenize(x)))

df.head(2)

df[['total_characters','total_sentences','total_words']].describe()

mask0=df['Sentiment']==0
mask1=df['Sentiment']==1
mask2=df['Sentiment']==2

df[mask0][['total_sentences','total_words','total_characters']].describe()

df[mask1][['total_sentences','total_words','total_characters']].describe()

df[mask2][['total_sentences','total_words','total_characters']].describe()

plt.figure(figsize=(12,6))
sns.histplot(df[df['Sentiment'] == 0]['total_characters'],color='green')
sns.histplot(df[df['Sentiment'] == 1]['total_characters'],color='red')
sns.histplot(df[df['Sentiment'] == 2]['total_characters'],color='pink')

plt.figure(figsize=(10,4))
sns.histplot(df[df['Sentiment'] == 0]['total_words'],color='green')
sns.histplot(df[df['Sentiment'] == 1]['total_words'],color='red')
sns.histplot(df[df['Sentiment'] == 2]['total_words'],color='pink')

sns.pairplot(df,hue='Sentiment')

sns.heatmap(df.corr(),annot=True)

from wordcloud import WordCloud
wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')

negative_wc = wc.generate(df[df['Sentiment'] == 0]['Comment'].str.cat(sep=" "))

neutral_wc = wc.generate(df[df['Sentiment'] == 1]['Comment'].str.cat(sep=" "))

positive_wc = wc.generate(df[df['Sentiment'] == 2]['Comment'].str.cat(sep=" "))

plt.figure(figsize=(6,6))
plt.imshow(negative_wc)

plt.figure(figsize=(6,6))
plt.imshow(neutral_wc)

plt.figure(figsize=(6,6))
plt.imshow(positive_wc)

negative_corpus = []
for msg in df[df['Sentiment'] == 0]['Comment'].tolist():
    for word in msg.split():
        negative_corpus.append(word)

neutral_corpus = []
for msg in df[df['Sentiment'] == 1]['Comment'].tolist():
    for word in msg.split():
        neutral_corpus.append(word)

positive_corpus = []
for msg in df[df['Sentiment'] == 1]['Comment'].tolist():
    for word in msg.split():
        positive_corpus.append(word)

print(len(negative_corpus))
print(len(neutral_corpus))
print(len(positive_corpus))

from collections import Counter

pd.DataFrame(Counter(negative_corpus).most_common(30))





##############################################
#bag of words#
##############################################

cv=CountVectorizer(lowercase=True,stop_words='english',max_features=3000)
tfidf=TfidfVectorizer(max_features=3000)

features_cv=cv.fit_transform(df['Comment']).toarray()
features_tfidf=tfidf.fit_transform(df['Comment']).toarray()

type(features_cv)

features_cv

dict1 = pd.DataFrame(features_cv)
dict2 = pd.DataFrame(features_tfidf)

dict1.shape

df.columns

x_cv=dict1.iloc[:,:]
y_cv=df[['Sentiment']]

y_cv.columns

np.unique(y_cv)

x_tfidf=dict1.iloc[:,:]
y_tfidf=df.iloc[:,-1]

print(x_cv.shape)
print(x_tfidf.shape)

print(y_cv.shape)
print(y_tfidf.shape)

x_cv_train,x_cv_test,y_cv_train,y_cv_test=train_test_split(x_cv,y_cv,test_size=0.2)

y_cv_test.shape

x_tfidf_train,x_tfidf_test,y_tfidf_train,y_tfidf_test=train_test_split(x_tfidf,y_tfidf,test_size=0.2)

print(x_cv_train.shape)
print(y_cv_test.shape)
print(x_tfidf_train.shape)
print(y_tfidf_test.shape)

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.naive_bayes import GaussianNB,MultinomialNB,BernoulliNB
from sklearn.metrics import accuracy_score,precision_score

svc = SVC(kernel='sigmoid', gamma=1.0)
knc = KNeighborsClassifier()
mnb = MultinomialNB()
dtc = DecisionTreeClassifier(max_depth=5)
lrc = LogisticRegression(solver='liblinear', penalty='l1')
rfc = RandomForestClassifier(n_estimators=50, random_state=2)
abc = AdaBoostClassifier(n_estimators=50, random_state=2)
bc = BaggingClassifier(n_estimators=50, random_state=2)
etc = ExtraTreesClassifier(n_estimators=50, random_state=2)
gbdt = GradientBoostingClassifier(n_estimators=50,random_state=2)
xgb = XGBClassifier(n_estimators=50,random_state=2)

clfs = {
    'SVC' : svc,
    'KN' : knc, 
    'NB': mnb, 
    'DT': dtc, 
    'LR': lrc, 
    'RF': rfc, 
    'AdaBoost': abc, 
    'BgC': bc, 
    'ETC': etc,
    'GBDT':gbdt,
    'xgb':xgb
}

def train_classifier(clf,X_train,y_train,X_test,y_test):
    clf.fit(x_cv_train,y_cv_train)
    y_cv_pred = clf.predict(x_cv_test)
    accuracy = accuracy_score(y_cv_test,y_cv_pred)
    precision = precision_score(y_cv_test,y_cv_pred,average='micro')
    
    return accuracy,precision

#######################################################
#********************Counvectorizer*******************#
#######################################################

np.unique(y_cv_test)

accuracy_scores = []
precision_scores = []

for name,clf in clfs.items():
    
    current_accuracy,current_precision = train_classifier(clf, x_cv_train,y_cv_train,x_cv_test,y_cv_test)
    
    print("For ",name)
    print("Accuracy - ",current_accuracy)
    print("Precision - ",current_precision)
    
    accuracy_scores.append(current_accuracy)
    precision_scores.append(current_precision)

performance_df = pd.DataFrame({'Algorithm':clfs.keys(),'Accuracy':accuracy_scores,'Precision':precision_scores}).sort_values('Precision',ascending=False)

performance_df

from sklearn.ensemble import VotingClassifier

svc = SVC(kernel='sigmoid', gamma=1.0,probability=True)
mnb = MultinomialNB()
etc = ExtraTreesClassifier(n_estimators=50, random_state=2)

voting = VotingClassifier(estimators=[('svm', svc), ('nb', mnb), ('et', etc)],voting='soft')

voting.fit(x_cv_train,y_cv_train)

y_pred = voting.predict(x_cv_test)

print("Accuracy",accuracy_score(y_cv_test,y_pred))
print("Precision",precision_score(y_cv_test,y_pred,average='micro'))



import pickle

pickle.dump(cv,open('vectorizer.pkl','wb'))

pickle.dump(lrc,open('model.pkl','wb'))







gnb = GaussianNB()
mnb = MultinomialNB()
bnb = BernoulliNB()

gnb.fit(x_cv_train,y_cv_train)

pred_gnb=gnb.predict(x_cv_test)

print(accuracy_score(y_cv_test,pred_gnb))
print(precision_score(y_cv_test,pred_gnb,average='micro'))

mnb.fit(x_cv_train,y_cv_train)

pred_mnb=mnb.predict(x_cv_test)

print(accuracy_score(y_cv_test,pred_mnb))
print(precision_score(y_cv_test,pred_mnb,average='micro'))

bnb.fit(x_cv_train,y_cv_train)

pred_bnb=bnb.predict(x_cv_test)

print(accuracy_score(y_cv_test,pred_bnb))
print(precision_score(y_cv_test,pred_bnb,average='micro'))