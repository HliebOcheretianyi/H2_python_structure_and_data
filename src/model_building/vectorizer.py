
import os
import re
import string
import numpy as np
import pandas as pd
import nltk
from nltk.stem import PorterStemmer
from nltk import word_tokenize
from nltk.corpus import stopwords
from src.preparations import ISW_everyday_update as I
import pickle
from src.model_building.tokenizer import LemmaTokenizer


INPUT_FILE = "../../data/ISW.csv"
OUTPUT_FILE = "../../data/ISW_vector.csv"
MAX_FEATURES = 2000
MIN_DF = 5
MAX_DF = 0.8
PCA_COMPONENTS = 400
TOP_KEYWORDS = 1000


with open('../our_models/3_lemming_v1.pkl', 'rb') as f:
    lemming = pickle.load(f)


with open('../our_models/3_tf_idf_v1.pkl', 'rb') as f:
    tf_idf = pickle.load(f)


with open('../our_models/3_PCA_v1.pkl', 'rb') as f:
    pca = pickle.load(f)


def setup_nltk():
    data_dir = '../prepar_notebooks/models'
    os.makedirs(data_dir, exist_ok=True)
    nltk.data.path.append(data_dir)

    resources = ['punkt_tab', 'wordnet', 'stopwords']
    for resource in resources:
        nltk.download(resource, download_dir=data_dir)


class StemmerTokenizer:

    def __init__(self):
        self.sp = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))

    def __call__(self, doc):
        if not isinstance(doc, str) or not doc.strip():
            return []
        return [self.sp.stem(t) for t in word_tokenize(doc)
                if t not in self.stop_words]


def clean_text(text):

    if not isinstance(text, str):
        return text

    month_names = [
        'january', 'february', 'march', 'april', 'may', 'june',
        'july', 'august', 'september', 'october', 'november', 'december'
    ]

    text = text.lower()
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    punctuation_to_remove = ''.join(c for c in string.punctuation if c != '-')
    text = re.sub(f'[{re.escape(punctuation_to_remove)}]', '', text)
    text = re.sub(r'\b(?:' + '|'.join(month_names) + r')\s+\d{1,2}\b', '', text)
    text = re.sub(r'[©®™•·]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def extract_keywords(X_pca, feature_names, pca_model, top_n=1000):

    keywords_per_doc = []

    for i in range(X_pca.shape[0]):
        doc_vector = X_pca[i]
        feature_importance = np.zeros(len(feature_names))

        for j, weight in enumerate(doc_vector):
            feature_importance += abs(weight) * abs(pca_model.components_[j])

        top_indices = feature_importance.argsort()[-top_n:][::-1]
        top_keywords = [(feature_names[idx], feature_importance[idx])
                        for idx in top_indices]

        max_importance = max([score for _, score in top_keywords])
        keywords_dict = {word: float(round(score / max_importance, 3))
                         for word, score in top_keywords}

        keywords_per_doc.append(keywords_dict)

    return keywords_per_doc


def main():
    I.everyday_parsing_isw()
    setup_nltk()

    print("Loading and cleaning data...")
    df_raw = pd.read_csv(INPUT_FILE)
    df_raw.dropna(inplace=True)
    df_raw['content'] = df_raw['content'].map(clean_text)

    lemma_tokenizer = LemmaTokenizer()
    stem_tokenizer = StemmerTokenizer()

    print("Applying tokenization, lemmatization, and stemming...")
    df_raw['lemma_content'] = df_raw['content'].apply(
        lambda x: ' '.join(lemma_tokenizer(x)) if isinstance(x, str) else '')
    df_raw['stem_content'] = df_raw['content'].apply(
        lambda x: ' '.join(stem_tokenizer(x)) if isinstance(x, str) else '')

    print("Extracting features...")

    X_lemma = lemming.fit_transform(df_raw['content'].fillna(''))

    print("Applying TF-IDF transformation...")
    X_tf_idf = tf_idf.fit_transform(X_lemma)
    X_dense = X_tf_idf.toarray()

    print(f"Performing PCA with {PCA_COMPONENTS} components...")

    X_pca = pca.fit_transform(X_dense)

    feature_names = lemming.get_feature_names_out()

    print("Extracting keywords...")
    keywords_per_doc = extract_keywords(X_pca, feature_names, pca, TOP_KEYWORDS)
    df_raw['keywords'] = keywords_per_doc

    df_raw['keywords'] = df_raw['keywords'].apply(lambda x: dict(sorted(x.items())))
    df_raw['keywords'] = df_raw['keywords'].apply(
        lambda x: " ".join(str(i) for i in x.values()))

    print(f"Saving results to {OUTPUT_FILE}...")
    df_raw.to_csv(OUTPUT_FILE, index=False)
    print("Processing complete!")


if __name__ == "__main__":
    main()