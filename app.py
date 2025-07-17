from flask import Flask, render_template, request, jsonify
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

app = Flask(__name__)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/eng', methods=['GET', 'POST'])
def eng():
    if request.method == 'POST':
        result = request.form.get('result', '').strip()
        if not result:
            return jsonify({'result': 'No input text provided.'})

        lis = [word.lower() for word in result.split()]
        stop_words = set(stopwords.words("english"))
        filtered_sentence = [word for word in lis if word not in stop_words]

        unique_words = list(set(filtered_sentence))

        # Lemmatize unique words
        lemmatizer = WordNetLemmatizer()
        root_words = [lemmatizer.lemmatize(word) for word in unique_words]

        # Load your CSV dictionary files
        df = pd.read_csv('Kashmiri_dictionary - S_Hassan_dictionary (1).csv')
        df_new1 = pd.read_csv('Stopwords - Sheet1 (2).csv')

        # Prepare expanded dictionary dataframe
        new_df = pd.DataFrame(df.meaning.str.split(',').tolist(), index=df.word).stack().reset_index([0, 'word'])
        new_df.columns = ['word', 'meaning']
        new_df.drop(columns='Unnamed: 0', inplace=True, errors='ignore')

        frames = [new_df, df_new1]
        df1 = pd.concat(frames, ignore_index=True)
        df1.drop(['newmeaning'], axis=1, inplace=True, errors='ignore')

        # Find matches for root words
        meaning_indices = []
        for word in root_words:
            matches = df1[df1["meaning"] == word]
            if not matches.empty:
                meaning_indices.append(matches.index[0])

        translated_words = [df1.at[i, 'word'] for i in meaning_indices]

        final_translation = ' '.join(translated_words) if translated_words else 'No translation found.'

        print(f"Input: {result}")
        print(f"Filtered: {filtered_sentence}")
        print(f"Lemmatized: {root_words}")
        print(f"Translation: {final_translation}")

        return jsonify({'result': final_translation})

    else:
        # For GET requests, show the input page
        return render_template('english_kashmiri.html', english_out='')

if __name__ == '__main__':
    app.run(debug=True)
