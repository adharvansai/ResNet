# import torch as t
# import numpy as np
# def unpickle(file):
#     print(file)
#     import pickle
#     fo = open(file, 'rb')
#     dict = pickle.load(fo,encoding='bytes')
#     fo.close()
#     return dict

# xs = []
# ys = []

# d = unpickle('/Users/aj/Documents/HW2/ResNet/cifar-10-batches-py/data_batch_'+repr(0+1))
# x = d[b'data']
# y = d[b'labels']
# xs = x
# ys = y

# for j in range(1,5):
#     d = unpickle('/Users/aj/Documents/HW2/ResNet/cifar-10-batches-py/data_batch_'+repr(j+1))
#     x = d[b'data']
#     y = d[b'labels']
#     x = np.array(x)
#     xs = np.concatenate((x,xs),axis = 0)
#     ys = np.concatenate((y,ys),axis = 0)

# print(np.shape(xs))
# print(np.shape(ys))
# #print(unpickle('/Users/aj/Documents/HW2/ResNet/cifar-10-batches-py/data_batch_1'))

print("Hello World")