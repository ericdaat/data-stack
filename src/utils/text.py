import re


def isolate_punctuation(text):
    """ Isolate punctuation in a sentence.

    >>> split_punctuation('Hi there!')
    'Hi there !'

    Args:
        text (str): Input sentence

    Returns:
        str: Output sentence with isolated punctuation
    """
    text = re.sub('([.,!?()])', r' \1 ', text)
    text = re.sub('\s{2,}', ' ', text)

    return text.strip()


def replace_urls(text, replace_with="<URL>"):
    """Replace urls in a sentence with a chosen string.

    >>> replace_urls("I love https://github.com")
    "I love <URL>"

    Args:
        text (str): Input sentence
        replace_with (str, optional): string to replace the url with. Defaults to "<URL>".

    Returns:
        str: Output sentence with replaced url
    """
    url_regex = re.compile(r"((http|ftp|https):\/\/)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b(.*)")
    text = url_regex.sub(replace_with, text)

    return text
