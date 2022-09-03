import string

import pandas as pd
import zeyrek
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import *


def get_stopwords():
    stopwords_set_f = list()
    with open('Analyze/turkish_stopwords.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            stopwords_set_f.append(line.strip())
    stopwords_set = stopwords.words('turkish')
    stopwords_set.extend(stopwords_set_f)
    return set(stopwords_set)


def clean(sentence):
    # Check has some unnecessary words. Find if exists and count
    re_urls = r'http\S+'
    re_html = r'<.*?>'
    re_digits = r'\d+'

    # remove digits
    sentence = re.sub(re_digits, '', sentence)
    # remove html tags
    sentence = re.sub(re_html, '', sentence)
    # remove urls
    sentence = re.sub(re_urls, '', sentence)

    # lowercase
    sentence = sentence.lower()

    # remove stop words
    stopwords_set = get_stopwords()
    sentence = sentence.split()
    sentence = ' '.join([word for word in sentence if word not in stopwords_set])

    # remove punctuations
    punctuation_set = string.punctuation

    for punctuation in punctuation_set:
        sentence = sentence.replace(punctuation, ' ')

    return sentence


# Slow version
# def lemmatizer(sentence):
#     # First, we need to tokenize sentences
#     tokenized_sentence = word_tokenize(sentence)
#
#     analyzer = zeyrek.MorphAnalyzer()
#     lemmatized_sentence = []
#     for word in tokenized_sentence:
#         if word == '':
#             continue
#         else:
#             lemmatized_word = analyzer.lemmatize(word)
#             lemmatized_sentence.append(lemmatized_word[0][1][0])
#
#     # Lowercase the tokens
#     i = 0
#     for word in lemmatized_sentence:
#         lemmatized_sentence[i] = word.lower()
#         i += 1
#
#     return lemmatized_sentence


def lemmatizer(text):
    # First, we need to tokenize sentences
    tokenized_text = [word_tokenize(sentence) for sentence in text]

    analyzer = zeyrek.MorphAnalyzer()
    lemmatized_text = []
    for tokenized_sentence in tokenized_text:
        lemmatized_sentence = []
        for word in tokenized_sentence:
            if word == '':
                continue
            else:
                lemmatized_word = analyzer.lemmatize(word)
                lemmatized_sentence.append(lemmatized_word[0][1][0])
        lemmatized_text.append(lemmatized_sentence)

    # Lowercase the tokens
    for lemmatized_sentence in lemmatized_text:
        i = 0
        for word in lemmatized_sentence:
            lemmatized_sentence[i] = word.lower()
            i += 1

    return lemmatized_text



def remove_rare_words(text, desired_freq):
    # text.dropna(axis=0, how='all', inplace=True)
    # text.reset_index(drop=True, inplace=True)
    prepared_freq = pd.read_csv('Analyze/frequencies.csv', index_col=0)
    prepared_freq = prepared_freq.squeeze()

    # Find frequencies
    freq = pd.Series(' '.join(text).split()).value_counts()
    last_freq = prepared_freq.add(freq, fill_value=0)
    less_freq = list(last_freq[last_freq == desired_freq].index)
    # Eliminate less frequency ones
    # text = text.apply(lambda sentence: " ".join(sentence for sentence in sentence.split() if sentence not in less_freq))
    text = [" ".join(sentence for sentence in sentence.split() if sentence not in less_freq) for sentence in text]

    return text



def preprocess_text(text):
    # Clean first
    cleaned_text = text.apply(lambda sentence: clean(sentence))
    # Lemmatize the cleaned text
    # lemmatized_text = cleaned_text.apply(lambda cleaned_sentence: lemmatizer(cleaned_sentence))
    lemmatized_text = lemmatizer(cleaned_text)
    # Normalize tokens
    lemmatized_text = list(filter(('').__ne__, lemmatized_text))
    lemmatized_text = [' '.join(x) for x in lemmatized_text]

    # Remove rare words
    lemmatized_text = remove_rare_words(lemmatized_text, desired_freq=1)

    return lemmatized_text



if __name__ == '__main__':
    df = pd.read_csv('test.txt', delimiter="\n", header=None)
    text = df.iloc[:, 0]
    lem_text = preprocess_text(text)
