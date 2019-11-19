import logging

import numpy as np


def load_pretrained_embeddings(embeddings_file, embeddings_dim, word_to_ix,
                               skip_header=False):
    """ Load pretrained embeddings weights.
    For the words that don't have a pre-trained embedding, we assign them
    a randomly initialized one.
    Args:
        embeddings_file (str): Weights file
        embeddings_dim (int): Embeddings dim
        word_to_ix (dict): Word to index mapper
    Returns:
        np.matrix: pre-trained embeddings matrix
    """
    # init random embeddings
    weights_matrix = np.random.randn(len(word_to_ix), embeddings_dim) * 0.01
    n_words_found = 0

    with open(embeddings_file, "r") as f:
        for i, line in enumerate(f):
            if skip_header and i == 0:
                continue
            # parse row
            line_split = line.split(" ")
            word = line_split[0]
            embeddings = line_split[1:]
            embeddings = np.array(embeddings).astype(float)

            # sanity check
            try:
                assert len(embeddings) == embeddings_dim
            except AssertionError:
                logging.warning("word {0} has incorect embeddings format".format(word))
                continue

            # add embeddings if we find them
            if word in word_to_ix:
                weights_matrix[word_to_ix[word]] = embeddings
                n_words_found += 1

    logging.info("{0} words with pre-trained embeddings".format(n_words_found))

    return weights_matrix
