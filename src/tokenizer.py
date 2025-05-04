class LemmaTokenizer:
    def __init__(self):
        from nltk.stem import WordNetLemmatizer
        from nltk.corpus import stopwords
        self.wnl = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def __call__(self, doc):
        from nltk.tokenize import word_tokenize
        if not isinstance(doc, str) or not doc.strip():
            return []
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc) if t not in self.stop_words]