def extract_features(text: str, stopwords=None):
    """
    Returns set of terms from a string.

    :type text: str
    :type stopwords: set
    :param stopwords: set of stop words
    :param text: original string
    :return: set of tokens after removing punctuation and stop words.
    """
    if stopwords is None:
        stopwords = set()
    string: str = text\
        .replace('\'', ' ')\
        .replace('\"', ' ')\
        .replace('.', ' ')\
        .replace(',', '')\
        .replace('،', ' ')\
        .replace('!', ' ')\
        .replace('؟', ' ')\
        .replace('’', ' ')\
        .replace('۔', ' ')\
        .replace('‘', ' ')

    terms = set(string.split())
    if stopwords:
        terms.difference_update(stopwords)

    return terms
