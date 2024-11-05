import torch
import torch.nn as nn

class DLSTMEncoder(nn.Module):
    def __init__(self,vocab_size,embedding_dim,hidden_dim,num_layers):
        super(DLSTMEncoder,self).__init__()
        self.embedding = nn.Embedding(vocab_size,embedding_dim)
        self.lstm =nn.LSTM(embedding_dim,hidden_dim,num_layers,bidirectional=True,batch_first=True)
        
    def forward(self,x):
        embeded = self.embedding(x)
        output,(hidden,cell) = self.lstm(embeded)
        return output,hidden,cell
    
class self_atttention(nn.Module):
    def __init__(self,hidden_dim):
        super(self_atttention,self).__init__()
        self.hidden_dim = hidden_dim
        self.quert = nn.Linear(hidden_dim,hidden_dim)
        self.key = nn.Linear(hidden_dim,hidden_dim)
        self.value = nn.Linear(hidden_dim,hidden_dim)
        self.softmax = nn.Softmax(dim=1)
        
    def forward(self,x):
        query = self.query(x)
        key = self.key(x).transpose(1,2)
        value = self.value
        attentionscore = torch.bmm(query,key)/(self.hidden_dim**0.5)
        context_vector = torch.bmm(attentionscore,value)
        return context_vector

        
class LSTMDecoder(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim):
        super(LSTMDecoder, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.attention = self_atttention(hidden_dim)
        self.fc = nn.Linear(hidden_dim * 2, vocab_size) # 考虑attention输出

    def forward(self, x, hidden, cell, encoder_outputs):
        embedded = self.embedding(x)
        output, (hidden, cell) = self.lstm(embedded, (hidden, cell))
        context_vector = self.attention(encoder_outputs)
        combined = torch.cat((output, context_vector), dim=2)
        predictions = self.fc(combined)
        return predictions, hidden, cell
    
class Seq2Seq(nn.Module):
    def __init__(self, encoder, decoder):
        super(Seq2Seq, self).__init__()
        self.encoder = encoder
        self.decoder = decoder

    def forward(self, article, summary):
        encoder_outputs, hidden, cell = self.encoder(article)
        decoder_outputs = []
        for i in range(summary.size(1)):
            decoder_input = summary[:, i].unsqueeze(1)
            predictions, hidden, cell = self.decoder(decoder_input, hidden, cell, encoder_outputs)
            decoder_outputs.append(predictions)
        return torch.stack(decoder_outputs, dim=1)
    
vocab_size = 100
embedding_dim = 128
hidden_dim = 256
num_layers = 2

encoder = DLSTMEncoder(vocab_size, embedding_dim, hidden_dim, num_layers)
decoder = LSTMDecoder(vocab_size, embedding_dim, hidden_dim)
model = Seq2Seq(encoder, decoder)