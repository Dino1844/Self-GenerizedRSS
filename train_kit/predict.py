#需要添加到test.ipynb后
#详见README


text = ''
tokens = [tok for tok in jieba.cut(text)]
tokens_idx = [SOS_IDX] + [vocab2id.get(word) for word in tokens] + [EOS_IDX]
tokens_idx = torch.tensor(tokens_idx)
print(tokens_idx)
res = []
encoder_outputs, hidden = model.encoder(tokens_idx.unsqueeze(0).to(device))
inputs = torch.tensor([SOS_IDX]).to(device)
for t in range(1, 25):
    output, hidden = model.decoder(inputs, hidden, encoder_outputs)
    inputs = output.argmax(1)
    word = id2vocab[inputs.item()]
    res.append(word)
    if word == '<eos>':
        break
print(''.join(res))