# Doccano Transformer Imports
#from doccano_transformer.datasets import NERDataset
#from doccano_transformer.utils import read_jsonl
from sklearn.model_selection import train_test_split
import IPython
import json
news_sources = ["bitcoin", "bitnews", "coindesk",
                "cryptonews", "cryptoslate", "insideBitcoins"]

data_path = "./data/"
source_path = data_path + "sources/"


def news_split(test_size=0.3):
    files = [source_path + i+"_data.jsonl" for i in news_sources]
    all_data = []
    for f in files:
        ls = list(open(f, encoding="utf-8"))
        ls = [json.loads(i) for i in ls]
        all_data.extend(ls)
    # Changing all labels to Entity
    for entry in all_data:
        labels = entry["labels"]
        if len(labels) == 0:
            continue
        for label in labels:
            label[2] = "Entity"

    train, test = train_test_split(
        all_data, test_size=test_size, random_state=42)

    train = [convert(i) for i in train]
    # train = [i for j in train for i in j] #flatten list
    test = [convert(i) for i in test]
    # test = [i for j in test for i in j] #flatten list

    train_str = ""
    for article in train:
        for label in article:
            if not label[0]:
                continue
            train_str += label[0] + " " + label[1]
            train_str += "\n"
        train_str += "\n"  # Add newline after each article extract

    test_str = ""
    for article in test:
        for label in article:
            if not label[0]:
                continue
            test_str += label[0] + " " + label[1]
            test_str += "\n"
        test_str += "\n"  # Add newline after each article extract

    text_file = open(data_path + "news_train_sep.conll", "w", encoding="utf-8")
    text_file.write(train_str)
    text_file.close()

    text_file = open(data_path + "news_test_sep.conll", "w", encoding="utf-8")
    text_file.write(test_str)
    text_file.close()


def reddit_split():
    pass


def twitter_split():
    pass


def convert(data):
    output_text = []
    beg_index = 0
    end_index = 0

    text = data["text"]
    all_labels = sorted(data["labels"])

    for ind in range(len(all_labels)):
        next_label = all_labels[ind]
        output_text += [(label_word, "O")
                        for label_word in text[end_index:next_label[0]].strip().split()]

        label = next_label
        beg_index = label[0]
        end_index = label[1]
        label_text = text[beg_index:end_index]
        output_text += [(label_word, "B-" + label[2]) if not i else (label_word,
                                                                     "I-" + label[2]) for i, label_word in enumerate(label_text.split(" "))]

    output_text += [(label_word, "O")
                    for label_word in text[end_index:].strip().split()]
    return output_text


news_split()
# train = train.to_conll2003(str.split)
IPython.embed()
