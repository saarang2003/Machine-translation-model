import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# Download necessary data for NLTK (only need to run once)
nltk.download('stopwords')
nltk.download('wordnet')

# Example input
result = "that child is a Troubled CHILD"

# Lowercase and split words
words = [word.lower() for word in result.split()]

# Remove English stopwords
stop_words = set(stopwords.words("english"))
filtered_words = [word for word in words if word not in stop_words]

# Get unique filtered words
unique_words = list(set(filtered_words))

# Lemmatize words to get root form
def get_root_word(word_list):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word) for word in word_list]

root_words = get_root_word(unique_words)

# Load Kashmiri dictionary CSV
df = pd.read_csv('Kashmiri_dictionary - S_Hassan_dictionary (1).csv')

# Split meanings (if multiple meanings separated by commas)
new_df = pd.DataFrame(df.meaning.str.split(',').tolist(), index=df.word).stack().reset_index([0, 'word'])
new_df.columns = ['word', 'meaning']

new_df.to_csv("new_dictionary.csv", index=False)

# Load stopwords CSV (Kashmiri or English stopwords you want to add)
df_stopwords = pd.read_csv("Stopwords - Sheet1.csv")

# Reload new_dictionary.csv (to remove unwanted columns)
new_df = pd.read_csv('new_dictionary.csv', skipinitialspace=True)
if 'Unnamed: 0' in new_df.columns:
    new_df.drop(columns='Unnamed: 0', inplace=True)

# Combine dictionary and stopwords
df_combined = pd.concat([new_df, df_stopwords], ignore_index=True)

# Drop 'newmeaning' column if exists
if 'newmeaning' in df_combined.columns:
    df_combined.drop(columns='newmeaning', inplace=True)

df_combined.reset_index(drop=True, inplace=True)

# Translate words by matching English word (meaning) to Kashmiri (word)
translated_words = []
for w in words:
    matches = df_combined[df_combined['meaning'] == w]
    if not matches.empty:
        # Take the first Kashmiri translation found
        translated_words.append(matches.iloc[0]['word'])
    else:
        # If no translation found, keep original word or use placeholder
        translated_words.append(w)

# Join translated words to form sentence
translated_sentence = ' '.join(translated_words)

print("Original:", result)
print("Translated:", translated_sentence)
