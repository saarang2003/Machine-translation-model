import pandas as pd
# from pygame import mixer  # Load the popular external library
import numpy as np
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import requests
import time

import os
#English to Kashmiri

result = "that child is a Troubled CHILD"

lis = []
for words in result.split(" "):
  lis.append(words.lower())

print(lis)