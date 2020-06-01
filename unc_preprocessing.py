def extract_features(text: str, stopwords: set):
    """
    Returns set of terms from a string.

    :param stopwords: set of stop words
    :param text: original string
    :return: set of tokens after removing punctuation and stop words.
    """
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
    terms.difference_update(stopwords)

    return terms
