import jieba
import pickle
from torchtext.data import TabularDataset,Field,BucketIterator
def tokenize(text):
    return list(jieba.cut(text))

TEXT = Field(sequential=True,tokenize=tokenize,lower = True,pad_token='<pad>')
fields = [('trg',TEXT),('src',TEXT)]

train_data,valid_data = TabularDataset.splits(
    path = 'C:\\Users\\Alfred\\Desktop\\rss\\train_kit\\data\\',
    train = 'train.tsv',
    validation = 'valiation.tsv',
    format = 'tsv',
    fields = fields,
)
TEXT.build_vocab(train_data)
print(train_data)
train_iter,valid_iter = BucketIterator.splits(
    (train_data,valid_data),
    batch_size = 32,
    shuffle = True,
    sort_key=lambda x: len(x.src),
    device = -1
)

train_texts = [vars(example)['src'] for example in train_data]
train_labels = [vars(example)['trg'] for example in train_data]
valid_texts = [vars(example)['src'] for example in valid_data]
valid_labels = [vars(example)['trg'] for example in valid_data]

with open('train_valid_data.pkl', 'wb') as f:
    pickle.dump((train_texts, train_labels, valid_texts, valid_labels), f)