def extract_features(text: str):
    """
    Returns set of terms from a string.

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

    return terms
