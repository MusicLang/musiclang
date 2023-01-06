import math
from typing import Tuple

import torch
from torch import nn, Tensor
import torch.nn.functional as F
from torch.nn import TransformerEncoder, TransformerEncoderLayer
from torch.utils.data import dataset

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

from ..base.model import ModelWrapper

class TransformerModelWrapper(ModelWrapper):
    """ """

    def __init__(self, n_tokens, d_model, n_head,  d_hid, n_layers, bptt, batch_size, lr, sc, dropout=0.5, model=None, **kwargs):
        self.n_tokens = n_tokens
        self.d_model = d_model
        self.n_head = n_head
        self.d_hid = d_hid
        self.n_layers = n_layers
        self.bptt = bptt
        self.dropout = dropout
        self.batch_size = batch_size
        self.lr = lr
        self.sc = sc

        if model is None:
            self.model = TransformerModel(n_tokens, d_model, n_head, d_hid, n_layers, dropout=dropout).to(device)
        else:
            self.model = model.to(device)


    def get_params(self):
        """ """
        return {'n_tokens': self.n_tokens,
                'd_model': self.d_model,
                'n_head': self.n_head,
                'd_hid': self.d_hid,
                'n_layers': self.n_layers,
                'bptt': self.bptt,
                'dropout': self.dropout,
                'batch_size': self.batch_size,
                'lr': self.lr,
                'sc': self.sc
                }

    def set_params(self, params):
        """

        Parameters
        ----------
        params :
            

        Returns
        -------

        """
        self.n_tokens = params['n_tokens']
        self.d_model = params['d_model']
        self.n_head = params['n_head']
        self.d_hid = params['d_hid']
        self.n_layers = params['n_layers']
        self.bptt = params['bptt']
        self.dropout = params['dropout']
        self.batch_size = params['batch_size']
        self.lr = params['lr']
        self.sc = params['sc']


    def batchify(self, data: Tensor, bsz: int) -> Tensor:
        """Divides the data into bsz separate sequences, removing extra elements
        that wouldn't cleanly fit.

        Parameters
        ----------
        data :
            Tensor, shape [N]
        bsz :
            int, batch size
        data: Tensor :
            
        bsz: int :
            

        Returns
        -------
        
            Tensor of shape [N // bsz, bsz]

        """
        seq_len = data.size(0) // bsz
        data = data[:seq_len * bsz]
        data = data.view(bsz, seq_len).t().contiguous()
        return data.to(device)

    def save_model(self, filepath):
        """

        Parameters
        ----------
        filepath :
            

        Returns
        -------

        """
        torch.save({'weights': self.model.state_dict(),
                    'params': self.get_params()
                    }, filepath)
        pass

    @classmethod
    def load_model(cls, filepath):
        """

        Parameters
        ----------
        filepath :
            

        Returns
        -------

        """
        data = torch.load(filepath)
        model_wrapper = cls(**data['params'])
        model = model_wrapper.model
        model.load_state_dict(data['weights'])
        model.eval()
        return model_wrapper



    def train(self, train_data, val_data, epochs=10, criterion=None):
        """

        Parameters
        ----------
        train_data :
            
        val_data :
            
        epochs :
             (Default value = 10)
        criterion :
             (Default value = None)

        Returns
        -------

        """
        train_data = torch.tensor(train_data, dtype=torch.long).to(device)
        val_data = torch.tensor(val_data, dtype=torch.long).to(device)
        train_data, val_data = batchify(train_data, self.batch_size), batchify(val_data, self.batch_size)

        best_model = train(self.model, train_data, val_data, epochs, self.bptt, self.n_tokens, self.lr, self.sc, criterion=criterion)
        self.model = best_model
        return TransformerModelWrapper(self.n_tokens, self.d_model, self.n_head,
                                       self.d_hid, self.n_layers, self.bptt, self.batch_size, self.lr, self.sc,
                                       dropout=self.dropout, model=best_model)

    def predict(self, tokens):
        """

        Parameters
        ----------
        tokens :
            

        Returns
        -------

        """
        with torch.no_grad():
            self.model.eval()
            data = torch.tensor(tokens, dtype=torch.long).to(device)
            data = data.reshape((data.shape[0], 1))
            output = self.model(data)
            return output


class TransformerModel(nn.Module):
    """ """

    def __init__(self, ntoken: int, d_model: int, nhead: int, d_hid: int,
                 nlayers: int, dropout: float = 0.5, **kwargs):
        super().__init__()
        self.model_type = 'Transformer'
        self.pos_encoder = PositionalEncoding(d_model, dropout)
        encoder_layers = TransformerEncoderLayer(d_model, nhead, d_hid, dropout)
        self.transformer_encoder = TransformerEncoder(encoder_layers, nlayers)
        self.encoder = nn.Embedding(ntoken, d_model)
        self.d_model = d_model
        self.decoder = nn.Linear(d_model, ntoken)

        self.init_weights()

    def init_weights(self) -> None:
        """ """
        initrange = 0.1
        self.encoder.weight.data.uniform_(-initrange, initrange)
        self.decoder.bias.data.zero_()
        self.decoder.weight.data.uniform_(-initrange, initrange)

    def forward(self, src: Tensor, src_mask: Tensor = None) -> Tensor:
        """

        Parameters
        ----------
        src :
            Tensor, shape [seq_len, batch_size]
        src_mask :
            Tensor, shape [seq_len, seq_len]
        src: Tensor :
            
        src_mask: Tensor :
             (Default value = None)

        Returns
        -------
        
            output Tensor of shape [seq_len, batch_size, ntoken]

        """
        src = self.encoder(src) * math.sqrt(self.d_model)
        src = self.pos_encoder(src)
        output = self.transformer_encoder(src, src_mask)
        output = self.decoder(output)
        return output



class PositionalEncoding(nn.Module):
    """ """

    def __init__(self, d_model: int, dropout: float = 0.1, max_len: int = 5000):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe = torch.zeros(max_len, 1, d_model)
        pe[:, 0, 0::2] = torch.sin(position * div_term)
        pe[:, 0, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x: Tensor) -> Tensor:
        """

        Parameters
        ----------
        x :
            Tensor, shape [seq_len, batch_size, embedding_dim]
        x: Tensor :
            

        Returns
        -------

        """
        x = x + self.pe[:x.size(0)]
        return self.dropout(x)


def generate_square_subsequent_mask(sz: int) -> Tensor:
    """Generates an upper-triangular matrix of -inf, with zeros on diag.

    Parameters
    ----------
    sz: int :
        

    Returns
    -------

    """
    return torch.triu(torch.ones(sz, sz) * float('-inf'), diagonal=1)


def batchify(data: Tensor, bsz: int) -> Tensor:
    """Divides the data into bsz separate sequences, removing extra elements
    that wouldn't cleanly fit.

    Parameters
    ----------
    data :
        Tensor, shape [N]
    bsz :
        int, batch size
    data: Tensor :
        
    bsz: int :
        

    Returns
    -------
    
        Tensor of shape [N // bsz, bsz]

    """
    seq_len = data.size(0) // bsz
    data = data[:seq_len * bsz]
    data = data.view(bsz, seq_len).t().contiguous()
    return data.to(device)


def get_batch(source: Tensor, i: int, bptt) -> Tuple[Tensor, Tensor]:
    """

    Parameters
    ----------
    source :
        Tensor, shape [full_seq_len, batch_size]
    i :
        int
    source: Tensor :
        
    i: int :
        
    bptt :
        

    Returns
    -------
    
        tuple (data, target), where data has shape [seq_len, batch_size] and
        target has shape [seq_len * batch_size]

    """
    seq_len = min(bptt, len(source) - 1 - i)
    data = source[i:i+seq_len]
    target = source[i+1:i+1+seq_len].reshape(-1)
    return data, target


import copy
import time


def train(model, train_data, val_data, epochs, bptt, ntokens, lr, sc, criterion=None):
    """

    Parameters
    ----------
    model :
        
    train_data :
        
    val_data :
        
    epochs :
        
    bptt :
        
    ntokens :
        
    lr :
        
    sc :
        
    criterion :
         (Default value = None)

    Returns
    -------

    """
    optimizer = torch.optim.SGD(model.parameters(), lr=lr)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, 1.0, gamma=sc)
    criterion = nn.CrossEntropyLoss() if criterion is None else criterion
    best_val_loss = float('inf')

    for epoch in range(1, epochs + 1):
        epoch_start_time = time.time()
        train_one(train_data, model, ntokens, bptt, criterion, optimizer, scheduler, epoch)
        val_loss = evaluate(model, val_data, bptt, ntokens, criterion)
        val_ppl = math.exp(val_loss)
        elapsed = time.time() - epoch_start_time
        print('-' * 89)
        print(f'| end of epoch {epoch:3d} | time: {elapsed:5.2f}s | '
              f'valid loss {val_loss:5.2f} | valid ppl {val_ppl:8.2f}')
        print('-' * 89)

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_model = copy.deepcopy(model)

        scheduler.step()

    return best_model


def train_one(train_data, model, ntokens, bptt, criterion, optimizer, scheduler, epoch) -> None:
    """

    Parameters
    ----------
    train_data :
        
    model :
        
    ntokens :
        
    bptt :
        
    criterion :
        
    optimizer :
        
    scheduler :
        
    epoch :
        

    Returns
    -------

    """

    model.train()  # turn on train mode
    total_loss = 0.
    log_interval = 200
    start_time = time.time()
    src_mask = generate_square_subsequent_mask(bptt).to(device)

    num_batches = len(train_data) // bptt
    for batch, i in enumerate(range(0, train_data.size(0) - 1, bptt)):
        data, targets = get_batch(train_data, i, bptt)
        seq_len = data.size(0)
        if seq_len != bptt:  # only on last batch
            src_mask = src_mask[:seq_len, :seq_len]
        output = model(data, src_mask)
        loss = criterion(output.view(-1, ntokens), targets)

        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 0.5)
        optimizer.step()

        total_loss += loss.item()
        if batch % log_interval == 0 and batch > 0:
            lr = scheduler.get_last_lr()[0]
            ms_per_batch = (time.time() - start_time) * 1000 / log_interval
            cur_loss = total_loss / log_interval
            ppl = math.exp(cur_loss)
            print(f'| epoch {epoch:3d} | {batch:5d}/{num_batches:5d} batches | '
                  f'lr {lr:02.2f} | ms/batch {ms_per_batch:5.2f} | '
                  f'loss {cur_loss:5.2f} | ppl {ppl:8.2f}')
            total_loss = 0
            start_time = time.time()

def evaluate(model: nn.Module, eval_data: Tensor, bptt, ntokens, criterion) -> float:
    """

    Parameters
    ----------
    model: nn.Module :
        
    eval_data: Tensor :
        
    bptt :
        
    ntokens :
        
    criterion :
        

    Returns
    -------

    """
    model.eval()  # turn on evaluation mode
    total_loss = 0.
    src_mask = generate_square_subsequent_mask(bptt).to(device)
    with torch.no_grad():
        for i in range(0, eval_data.size(0) - 1, bptt):
            data, targets = get_batch(eval_data, i, bptt)
            seq_len = data.size(0)
            if seq_len != bptt:
                src_mask = src_mask[:seq_len, :seq_len]
            output = model(data, src_mask)
            output_flat = output.view(-1, ntokens)
            total_loss += seq_len * criterion(output_flat, targets).item()
    return total_loss / (len(eval_data) - 1)