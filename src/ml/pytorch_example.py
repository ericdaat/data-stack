"""
From: https://pytorch.org/tutorials/beginner/text_sentiment_ngrams_tutorial.html
"""


import time
import os

import torch
from torch import optim
from torch.utils.data import DataLoader
import torch.nn as nn
from torchtext.datasets import text_classification
from torch.utils.data.dataset import random_split

from src.ml_helper.training import (
    register_model_in_db, register_epoch_in_db,
    hash_parameters, delete_model
)


BATCH_SIZE = 16
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class TextSentiment(nn.Module):
    def __init__(self, vocab_size, embed_dim, num_class):
        super().__init__()
        self.embedding = nn.EmbeddingBag(vocab_size, embed_dim, sparse=True)
        self.fc = nn.Linear(embed_dim, num_class)
        self.init_weights()

    def init_weights(self):
        initrange = 0.5
        self.embedding.weight.data.uniform_(-initrange, initrange)
        self.fc.weight.data.uniform_(-initrange, initrange)
        self.fc.bias.data.zero_()

    def forward(self, text, offsets):
        embedded = self.embedding(text, offsets)
        return self.fc(embedded)


def generate_batch(batch):
    label = torch.tensor([entry[0] for entry in batch])
    text = [entry[1] for entry in batch]
    offsets = [0] + [len(entry) for entry in text]
    # torch.Tensor.cumsum returns the cumulative sum
    # of elements in the dimension dim.
    # torch.Tensor([1.0, 2.0, 3.0]).cumsum(dim=0)

    offsets = torch.tensor(offsets[:-1]).cumsum(dim=0)
    text = torch.cat(text)

    return text, offsets, label


def train_func(model, optimizer, criterion, scheduler, sub_train_):

    # Train the model
    train_loss = 0
    train_acc = 0
    data = DataLoader(
        sub_train_,
        batch_size=BATCH_SIZE,
        shuffle=True,
        collate_fn=generate_batch
    )

    for i, (text, offsets, cls) in enumerate(data):
        optimizer.zero_grad()
        text, offsets, cls = text.to(device), offsets.to(device), cls.to(device)
        output = model(text, offsets)
        loss = criterion(output, cls)
        train_loss += loss.item()
        loss.backward()
        optimizer.step()
        train_acc += (output.argmax(1) == cls).sum().item()

    # Adjust the learning rate
    scheduler.step()

    return train_loss / len(sub_train_), train_acc / len(sub_train_)


def test(model, criterion, data_):
    loss = 0
    acc = 0
    data = DataLoader(data_, batch_size=BATCH_SIZE, collate_fn=generate_batch)
    for text, offsets, cls in data:
        text, offsets, cls = text.to(device), offsets.to(device), cls.to(device)
        with torch.no_grad():
            output = model(text, offsets)
            loss = criterion(output, cls)
            loss += loss.item()
            acc += (output.argmax(1) == cls).sum().item()

    return loss / len(data_), acc / len(data_)


def main():
    if not os.path.isdir('./.data'):
        os.mkdir('./.data')

    train_dataset, test_dataset = text_classification.DATASETS['AG_NEWS'](
        root='./.data',
        ngrams=2,
        vocab=None
    )

    VOCAB_SIZE = len(train_dataset.get_vocab())
    NUN_CLASS = len(train_dataset.get_labels())

    params = dict(
        embed_dim=32,
        n_epochs=5,
        lr=0.04,
        model_name="TextSentiment",
        optimizer_name="SGD"
    )

    model_id = hash_parameters(params)
    delete_model(model_id)
    register_model_in_db(model_id, params)
    print("stored model id:", model_id)

    model = TextSentiment(
        VOCAB_SIZE,
        params["embed_dim"],
        NUN_CLASS
    ).to(device)

    criterion = torch.nn.CrossEntropyLoss().to(device)
    optimizer = getattr(optim, params["optimizer_name"])(model.parameters(), lr=params["lr"])
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, 1, gamma=0.9)

    train_len = int(len(train_dataset) * 0.95)
    sub_train_, sub_valid_ = random_split(
        train_dataset,
        [train_len, len(train_dataset) - train_len]
    )

    for epoch in range(params["n_epochs"]):

        start_time = time.time()
        train_loss, train_acc = train_func(
            model, optimizer,
            criterion, scheduler, sub_train_
        )
        valid_loss, valid_acc = test(model, criterion, sub_valid_)

        secs = int(time.time() - start_time)
        mins = secs / 60
        secs = secs % 60

        register_epoch_in_db(
            model_id,
            epoch+1,
            training_loss=train_loss,
            eval_loss=valid_loss.item(),
            training_acc=train_acc,
            eval_acc=valid_acc
        )

        print('Epoch: %d' % (epoch + 1), " | time in %d minutes, %d seconds" % (mins, secs))
        print(f'\tLoss: {train_loss:.4f}(train)\t|\tAcc: {train_acc * 100:.1f} % (train)')
        print(f'\tLoss: {valid_loss:.4f}(valid)\t|\tAcc: {valid_acc * 100:.1f} % (valid)')


if __name__ == '__main__':
    main()
