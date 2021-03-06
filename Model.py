from ast import parse
import os
import time
import torch
import torch.nn as nn
import numpy as np
from torch.nn.modules import loss
from tqdm import tqdm

from NetWork import ResNet
from ImageUtils import parse_record

""" This script defines the training, validation and testing process.
"""

class Cifar(nn.Module):
    def __init__(self, config):
        super(Cifar, self).__init__()
        self.config = config
        self.network = ResNet(
            self.config.resnet_version,
            self.config.resnet_size,
            self.config.num_classes,
            self.config.first_num_filters,
        )
        ### YOUR CODE HERE
        # define cross entropy loss and optimizer
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = torch.optim.SGD(self.network.parameters(),lr = 0.1, momentum = 0.9, weight_decay = 5e-4)
        self.scheduler = torch.optim.lr_scheduler.StepLR(self.optimizer,step_size =10,gamma = 0.1)
        ### YOUR CODE HERE
    
    def train(self, x_train, y_train, max_epoch):
        self.network.train()
        # Determine how many batches in an epoch
        num_samples = x_train.shape[0]
        num_batches = num_samples // self.config.batch_size

        print('### Training... ###')
        for epoch in range(1, max_epoch+1):
            start_time = time.time()
            # Shuffle
            shuffle_index = np.random.permutation(num_samples)
            curr_x_train = x_train[shuffle_index]
            curr_y_train = y_train[shuffle_index]

            ### YOUR CODE HERE
            # Set the learning rate for this epoch
            # Usage example: divide the initial learning rate by 10 after several epochs
            lr = 0.1
            bs = self.config.batch_size
            ### YOUR CODE HERE
            
            for i in range(num_batches):
                ### YOUR CODE HERE
                # Construct the current batch.
                # Don't forget to use "parse_record" to perform data preprocessing.
                # Don't forget L2 weight decay
                start = i*bs
                end = (i+1) * bs
                batch_curr_x_train = curr_x_train[start:end,:]
                batch_curr_y_train = curr_y_train[start:end]
                current_batch_pp = []
                for j in range(self.config.batch_size):
                    current_batch_pp.append(parse_record(batch_curr_x_train[j],True))
                current_batch_pp = np.array(current_batch_pp)
                x_train_tensor = torch.FloatTensor(current_batch_pp)
                y_train_tensor = torch.LongTensor(batch_curr_y_train)

                outputs = self.network(x_train_tensor)
                loss = self.criterion(outputs,y_train_tensor)

                ### YOUR CODE HERE
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                print('Batch {:d}/{:d} Loss {:.6f}'.format(i, num_batches, loss), end='\r', flush=True)
            self.scheduler.step()
            duration = time.time() - start_time
            print('Epoch {:d} Loss {:.6f} Duration {:.3f} seconds.'.format(epoch, loss, duration))

            if epoch % self.config.save_interval == 0:
                self.save(epoch)


    def test_or_validate(self, x, y, checkpoint_num_list):
        self.network.eval()
        print('### Test or Validation ###')
        for checkpoint_num in checkpoint_num_list:
            checkpointfile = os.path.join(self.config.modeldir, 'model-%d.ckpt'%(checkpoint_num))
            self.load(checkpointfile)

            preds = []
            for i in tqdm(range(x.shape[0])):
            ### YOUR CODE HERE
                img_pp = parse_record(x[i],False)
                img_input = np.array([img_pp])
                x_test_tensor = torch.FloatTensor(img_input)
                pred = self.network(x_test_tensor)
                _,pred = torch.max(pred,1)
                preds.append(pred)
            
            ### END CODE HERE

            y = torch.tensor(y)
            preds = torch.tensor(preds)
            print('Test accuracy: {:.4f}'.format(torch.sum(preds==y)/y.shape[0]))
    
    def save(self, epoch):
        checkpoint_path = os.path.join(self.config.modeldir, 'model-%d.ckpt'%(epoch))
        os.makedirs(self.config.modeldir, exist_ok=True)
        torch.save(self.network.state_dict(), checkpoint_path)
        print("Checkpoint has been created.")
    
    def load(self, checkpoint_name):
        ckpt = torch.load(checkpoint_name, map_location="cpu")
        self.network.load_state_dict(ckpt, strict=True)
        print("Restored model parameters from {}".format(checkpoint_name))