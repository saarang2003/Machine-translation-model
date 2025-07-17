from flask import Flask, render_template,request,Markup,redirect,url_for,jsonify
import jinja2
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
nltk.download('punkt')
nltk.download('wordnet')

from nltk.stem import WordNetLemmatizer
import requests
import time

import os

#import requests
app = Flask(__name__)

if __name__ == '__main__':
    app.run()
global result
global final
"""@app.route('/')
def hello():
    
    return 'Success'"""
@app.route('/index')
def index():
  return render_template('index.html')


@app.route('/eng')
def test():
  print("inside first app route")
  return render_template('english_kashmiri.html',english_out='Hello world')


def eng():
  '''if not request.data:
    print("inside if")
    return render_template('english_kashmiri.html')'''


  result = request.form['result']
  
  print("Reached in python")
  print(result)

  lis = []
  for words in result.split(" "):
    lis.append(words.lower())

  nltk.download('stopwords')

    #to remove the stop words


  stop_words = set(stopwords.words("english"))

    # Removing stop words from the list
  filtered_sentence = [word for word in lis if word.lower() not in stop_words]

    # Printing filtered words
    # print(filtered_sentence)


  stop_words = set(stopwords.words("english"))
    # len(stop_words)

  d = pd.DataFrame(stop_words)
  
  unique_words = list(set(filtered_sentence))
    # print(unique_words)

    #to find the root word 
  global df
  def get_root_word(word_list):
    lemmatizer = WordNetLemmatizer()
    root_words = [lemmatizer.lemmatize(word) for word in word_list]
    return root_words

  root_words = unique_words
    # print(root_words)
  
  df = pd.read_csv(r'Kashmiri_dictionary - S_Hassan_dictionary (1).csv')
  
  
  new_df = pd.DataFrame(df.meaning.str.split(',').tolist(), index=df.word).stack()
  new_df = new_df.reset_index([0, 'word'])
  new_df.columns = ['word', 'meaning']

  new_df.to_csv('new_dictionary.csv')
  global df_new1
  df_new1 = pd.read_csv(r'Stopwords - Sheet1 (2).csv')
   # df_new1 C:\\Users\\Ritika\\Desktop\\flask_app\\flask_app\\Stopwords - Sheet1 (2).csv

  new_df = pd.read_csv('new_dictionary.csv', skipinitialspace=True)

  new_df.drop(columns='Unnamed: 0', inplace=True)

    # new_df

  frames = [new_df,df_new1]
  df1 = pd.concat(frames)

    # df1

  df1.drop(['newmeaning'],axis=1,inplace=True)

    # df1

  df1.to_csv('finalset.csv')

  def Diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif

  df1 = pd.read_csv('finalset.csv')

  meaning = []
  
  for word in lis:
    # Searching the word in the "Words" column of the DataFrame  
    if word in df1["meaning"].values:
     # Getting the index of the matching word
      index = df1[df1["meaning"] == word].index[0]
     # Printing the corresponding meaning from the "Meanings" column
      mean = df1.at[index, 'word']
      meaning.append(index)

  df1.reset_index(drop=True,inplace=True)
  
  
    # meaning
  global new1
  new1 = []
  for i in meaning:
    new1.append(df1['word'][i])

  final = ' '.join(new1)
  print(final)
    # new1
  output = 'My name is Ritika'
  return jsonify({'result': final}) 
  #return render_template('english_kashmiri.html',english_out=final,result=result)