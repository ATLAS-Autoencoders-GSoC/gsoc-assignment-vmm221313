# -*- coding: utf-8 -*-
"""relu_vs_tanh.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZapXgAm4f2IZuMuanQ6b99yPVMddyL3h
"""

!pip install corner

from google.colab import drive
drive.mount('/content/drive', force_remount=True)

cd drive/My\ Drive/Projects/Autoencoder_1

import os
import utils
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import corner.corner as corner
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data
from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader

import fastai
from fastai import train as tr 
from fastai.callbacks import ActivationStats
from fastai import data_block, basic_train, basic_data

import matplotlib as mpl
import my_matplotlib_style as ms
mpl.rc_file('my_matplotlib_rcparams')

from utils import plot_activations
from my_utils import make_plots, load_data, train_evaluate_model

if torch.cuda.is_available():
  fastai.torch_core.defaults.device = 'cuda'

class AE_3D_200_relu(nn.Module):
    def __init__(self, hidden_dim_1, hidden_dim_2, hidden_dim_3, n_features=4):
        super(AE_3D_200_relu, self).__init__()
        self.en1 = nn.Linear(n_features, hidden_dim_1)
        self.en2 = nn.Linear(hidden_dim_1, hidden_dim_2)
        self.en3 = nn.Linear(hidden_dim_2, hidden_dim_3)
        self.en4 = nn.Linear(hidden_dim_3, 3)
        self.de1 = nn.Linear(3, hidden_dim_3)
        self.de2 = nn.Linear(hidden_dim_3, hidden_dim_2)
        self.de3 = nn.Linear(hidden_dim_2, hidden_dim_1)
        self.de4 = nn.Linear(hidden_dim_1, n_features)
        self.relu = nn.ReLU()

    def encode(self, x):
        return self.en4(self.relu(self.en3(self.relu(self.en2(self.relu(self.en1(x)))))))

    def decode(self, x):
        return self.de4(self.relu(self.de3(self.relu(self.de2(self.relu(self.de1(self.relu(x))))))))

    def forward(self, x):
        z = self.encode(x)
        return self.decode(z)

    def describe(self):
        return 'in-' + str(hidden_dim_1) + '-' + str(hidden_dim_2) + '-' + str(hidden_dim_3) + '-' +'3-' + str(hidden_dim_3) + '-' + str(hidden_dim_2) + '-' + str(hidden_dim_1) + '-out'

class AE_3D_200_tanh(nn.Module):
    def __init__(self, hidden_dim_1, hidden_dim_2, hidden_dim_3, n_features=4):
        super(AE_3D_200_tanh, self).__init__()
        self.en1 = nn.Linear(n_features, hidden_dim_1)
        self.en2 = nn.Linear(hidden_dim_1, hidden_dim_2)
        self.en3 = nn.Linear(hidden_dim_2, hidden_dim_3)
        self.en4 = nn.Linear(hidden_dim_3, 3)
        self.de1 = nn.Linear(3, hidden_dim_3)
        self.de2 = nn.Linear(hidden_dim_3, hidden_dim_2)
        self.de3 = nn.Linear(hidden_dim_2, hidden_dim_1)
        self.de4 = nn.Linear(hidden_dim_1, n_features)
        self.tanh = nn.Tanh()

    def encode(self, x):
        return self.en4(self.tanh(self.en3(self.tanh(self.en2(self.tanh(self.en1(x)))))))

    def decode(self, x):
        return self.de4(self.tanh(self.de3(self.tanh(self.de2(self.tanh(self.de1(self.tanh(x))))))))

    def forward(self, x):
        z = self.encode(x)
        return self.decode(z)

    def describe(self):
        return 'in-' + str(hidden_dim_1) + '-' + str(hidden_dim_2) + '-' + str(hidden_dim_3) + '-' +'3-' + str(hidden_dim_3) + '-' + str(hidden_dim_2) + '-' + str(hidden_dim_1) + '-out'

hidden_dim_1 = 200
hidden_dim_2 = 100
hidden_dim_3 = 50

model = AE_3D_200_tanh(hidden_dim_1, hidden_dim_2, hidden_dim_3)
model_name = 'AE_3D_200_tanh'
num_epochs = 50
learning_rate = 3e-4
loss = train_evaluate_model(model, model_name, num_epochs, learning_rate, hidden_dim_1, hidden_dim_2, hidden_dim_3)

model = AE_3D_200_relu(hidden_dim_1, hidden_dim_2, hidden_dim_3)
model_name = 'AE_3D_200_relu'
num_epochs = 50
learning_rate = 3e-3
loss = train_evaluate_model(model, model_name, num_epochs, learning_rate, hidden_dim_1, hidden_dim_2, hidden_dim_3)
