#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 17:16:35 2019

@author: Preeti
"""

# importing libraries 
from sklearn.model_selection import cross_val_score
import numpy as np
import nltk 
import re
from urllib import request
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))
from nltk.stem import WordNetLemmatizer 
lemmatizer = WordNetLemmatizer() 


#Data preparation and preprocess
def custom_preprocessor(text):
        text = re.sub(r'\W+|\d+|_', ' ', text)    #removing numbers and punctuations
        text =  re.sub(r'\s+',' ',text) #remove multiple spaces into a single space
        text = re.sub(r"\s+[a-zA-Z]\s+",' ',text) #remove a single character
        text = text.lower() 
        text = nltk.word_tokenize(text)       #tokenizing
        text = [word for word in text if not word in stop_words] #English Stopwords
        text = [lemmatizer.lemmatize(word) for word in text]              #Lemmatising
        return text
    
    
    
filepath_dict = {'Book1':   'https://www.gutenberg.org/files/58764/58764-0.txt',
               'Book2': 'https://www.gutenberg.org/files/58751/58751-0.txt',
               'Book3':   'http://www.gutenberg.org/cache/epub/345/pg345.txt'}

for key, value in filepath_dict.items():
   if (key == "Book1"):
        bookLoc = filepath_dict[key]
        response = request.urlopen(bookLoc)
        raw = response.read().decode('utf-8')
        len(raw)
        first_book = custom_preprocessor(raw)           
   elif (key == "Book2"):
        bookLoc = filepath_dict[key]
        response = request.urlopen(bookLoc)
        raw = response.read().decode('utf-8')
        len(raw)
        second_book = custom_preprocessor(raw)
   elif (key == "Book3"):
        bookLoc = filepath_dict[key]
        response = request.urlopen(bookLoc)
        raw = response.read().decode('utf-8')
        len(raw)
        third_book = custom_preprocessor(raw)
   else:
       pass
        
        
#Building First Book
first_book_text = ' '.join(first_book)
fileLoc = '/Users/sfuhaid/Desktop/EBC7100Assign1/firstbook/a.txt'
with open(fileLoc, 'a') as fout:
    fout.write(first_book_text)
    fout.close()

#Building Second Book
second_book_text = ' '.join(second_book)
fileLoc = '/Users/sfuhaid/Desktop/EBC7100Assign1/secondbook/b.txt'
with open(fileLoc, 'a') as fout:
    fout.write(second_book_text)
    fout.close()
    
 
#Building Third Book
third_book_text = ' '.join(third_book)
fileLoc = '/Users/sfuhaid/Desktop/EBC7100Assign1/thirdbook/c.txt'
with open(fileLoc, 'a') as fout:
    fout.write(third_book_text)
    fout.close()
    

# labeling
# Cretaing tuple
# aBooklist = []
def readAtxtfile(bookText, docs, labels):
    x = 0
    i = 0
    n = 150
    while x < 200:
        temp = ""
        words = bookText.split(" ")[i:n]
        for word in words:
            temp = word + " " + temp
        docs.append(temp)
        labels.append(0)
        i += 150
        n += 150
        x += 1
    return docs, labels


# Cretaing tuple
# bBooklist = []
def readBtxtfile(bookText, docs, labels):
    x = 0
    i = 0
    n = 150
    while x < 184:
        temp = ""
        words = bookText.split(" ")[i:n]
        for word in words:
            temp = word + " " + temp
        docs.append(temp)
        labels.append(1)
        i += 150
        n += 150
        x += 1
    return docs, labels

# Cretaing tuple
# cBooklist = []
def readCtxtfile(bookText, docs, labels):
    x = 0
    i = 0
    n = 150
    while x < 200:
        temp = ""
        words = bookText.split(" ")[i:n]
        for word in words:
            temp = word + " " + temp
        docs.append(temp)
        labels.append(2)
        i += 150
        n += 150
        x += 1
    return docs, labels


docs = []
labels = []
docs, labels = readAtxtfile(first_book_text, docs, labels)
# print(aBooklist)
docs, labels = readBtxtfile(second_book_text, docs, labels)
# print(bBooklist)
docs, labels = readCtxtfile(third_book_text, docs, labels)
# print(cBooklist)


#print(len(docs))
#print(docs)
#print(labels)
#print(len(labels))

#Tf-IDF Model Implementation
# Creating the Tf-Idf model 
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(max_features = 2000, min_df = 3, max_df = 0.6)
TF_X = vectorizer.fit_transform(docs)
TF_X.toarray()


# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
x_train, x_val, y_train, y_val = train_test_split(TF_X, labels, test_size=0.20, random_state=42, shuffle=True)

# fitting the model into machine learning algorithm
# Training first classifier
#SVC
from sklearn.svm import SVC
#cross validation to balance test and train
clf = SVC(kernel='rbf', C=1, gamma='auto', random_state=42)
scores = cross_val_score(clf, x_train, y_train, cv=10)
print("Accuracy: {} (+/- {})".format(scores.mean(), scores.std() * 2))

# manual cross validation with shuffle
from sklearn.model_selection import StratifiedShuffleSplit
n_splits = 10
ssf = StratifiedShuffleSplit(n_splits, test_size=0.20, random_state=42)
# training the first classifer 
clf = SVC(kernel='rbf', C=1, gamma='auto', random_state=42)
new_scores = []
X_array = TF_X.toarray()
labels = np.asarray(labels)

from sklearn.metrics import accuracy_score
print("{} fold cross validation".format(n_splits))
for train_index, val_index in ssf.split(X_array, labels):
    x_train, y_train = X_array[train_index], labels[train_index]
    x_val, y_val = X_array[val_index], labels[val_index]
    clf.fit(x_train, y_train)
    prediction_scores = clf.predict(x_val)
    print(accuracy_score(y_val, prediction_scores))
    new_scores.append(accuracy_score(y_val, prediction_scores))

print("Mean: {}".format(np.mean(new_scores)))
    
# Testing model performance (error analysis) 
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_val, prediction_scores)  

#Accuracy recall and precision
def precision(label, confusion_matrix):
    col = confusion_matrix[:, label]
    return confusion_matrix[label, label] / col.sum()
    
def recall(label, confusion_matrix):
    row = confusion_matrix[label, :]
    return confusion_matrix[label, label] / row.sum()
def precision_macro_average(confusion_matrix):
    rows, columns = confusion_matrix.shape
    sum_of_precisions = 0
    for label in range(rows):
        sum_of_precisions += precision(label, confusion_matrix)
    return sum_of_precisions / rows
def recall_macro_average(confusion_matrix):
    rows, columns = confusion_matrix.shape
    sum_of_recalls = 0
    for label in range(columns):
        sum_of_recalls += recall(label, confusion_matrix)
    return sum_of_recalls / columns

print("label precision recall")
for label in range(3):
    print(f"{label:5d} {precision(label, cm):9.3f} {recall(label, cm):6.3f}")

print("precision total:", precision_macro_average(cm))
print("recall total:", recall_macro_average(cm))   

def accuracy(confusion_matrix):
    diagonal_sum = confusion_matrix.trace()
    sum_of_all_elements = confusion_matrix.sum()
    return diagonal_sum / sum_of_all_elements 

accuracy(cm)


# visualization

# top positive and negative features
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
import matplotlib.pyplot as plt
def plot_coefficients(clf, feature_names, top_features=5):
 coef = clf.coef_.ravel()
 top_positive_coefficients = np.argsort(coef)[-top_features:]
 top_negative_coefficients = np.argsort(coef)[:top_features]
 top_coefficients = np.hstack([top_negative_coefficients, top_positive_coefficients])
 # create plot
 plt.figure(figsize=(7, 5))
 colors = [ 'red' if c < 0 else 'blue' for c in coef[top_coefficients]]
 plt.bar(np.arange(2 * top_features), coef[top_coefficients], color=colors)
 feature_names = np.array(feature_names)
 plt.xticks(np.arange(1, 1 + 2 * top_features), feature_names[top_coefficients], rotation=60, ha='right')
 plt.show()
cv = CountVectorizer()
cv.fit(docs)
#print len(cv.vocabulary_)
#print (cv.get_feature_names())
X_train = cv.transform(docs)

svm = LinearSVC()
svm.fit(x_train, y_train)
plot_coefficients(svm, cv.get_feature_names())


# heatmap-visualization
import seaborn as sn
import pandas as pd
df_cm = pd.DataFrame(cm, index = [i for i in "012"],
                 columns = [i for i in "012"])
sn.set(font_scale=1.4)
sn.heatmap(df_cm,annot=True, annot_kws={"size": 16})


# Saving our classifier
import pickle 
with open('classifiertfidf.pickle','wb') as f:
    pickle.dump(clf,f)
    
# Saving the TF-IDF model
with open('tfidfmodel.pickle','wb') as f:
    pickle.dump(vectorizer,f)


