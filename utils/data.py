import torch
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence



def read_text(f_name, max_words=100):
    with open(f'data/daily/ids/{f_name}', 'r', encoding='utf-8') as f:
        orig_data = f.readlines()

    #cut long sentences with max_words limitation
    data = []
    for line in orig_data:
        _line = list(map(int, line.split()))
        if len(_line) > max_words:
            _line = _line[:99]
            _line.append(3) #append eos token
        data.append(_line)
    
    return data



class CustomDataset(Dataset):
    def __init__(self, src_data, trg_data):
        self.src = src_data
        self.trg = trg_data
    
    def __len__(self):
        return len(self.trg)
    
    def __getitem__(self, idx):
        return self.src[idx], self.trg[idx]



def _collate_fn(data_batch):    
    src_batch, trg_batch = [], []

    for batch in data_batch:
        src = torch.tensor(batch[0], dtype=torch.long)
        trg = torch.tensor(batch[1], dtype=torch.long)
        src_batch.append(src)
        trg_batch.append(trg)

    #padding value == 0
    src_batch = pad_sequence(src_batch, batch_first=True, padding_value=1)
    trg_batch = pad_sequence(trg_batch, batch_first=True, padding_value=1)

    return src_batch, trg_batch



def get_dataloader(split, batch_size):        
    src = read_text(f"{split}.src")
    trg = read_text(f"{split}.trg")

    dataset = CustomDataset(src, trg)
    iterator = DataLoader(dataset, batch_size=batch_size, shuffle=True, collate_fn=_collate_fn, num_workers=2)
    
    return iterator