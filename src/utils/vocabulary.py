import string
from collections import defaultdict


def make_char_to_ix():
    """ Make a character to index dictionary.

    Returns:
        dict: character to index
    """
    all_chars = string.printable + "°éèàëïüâêîôûç"
    char_to_ix = {c: i for i, c in enumerate(all_chars)}

    return char_to_ix


def make_word_to_ix(train_sentences, char_to_split_at=" ", unk_tag="<UNK>"):
    """ Make a word to index dictionary

    Args:
        train_sentences (list): list of sentences
        char_to_split_at (str, optional): str. Character to use to split \
            the sentence (for tokenization). Defaults to " ".
        unk_tag (str, optional): Unknown tag. Defaults to "<UNK>".

    Returns:
        [type]: [description]
    """
    word_to_ix = defaultdict(str)

    word_to_ix[unk_tag] = 0

    for sent in train_sentences:
        for word in sent.split(char_to_split_at):
            if word not in word_to_ix:
                word_to_ix[word] = len(word_to_ix)

    return word_to_ix

