# author: Carlina Kim, Karanpal Singh, Sukriti Trehan, Victor Cuspinera
# date: 2020-06-21

'''This script has our best models for subthemes. These models will be
used to train subtheme labels.
'''
import pandas as pd
import numpy as np

import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"

from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten, Activation, Concatenate
from keras.layers import Conv1D, Conv2D, MaxPooling2D, GlobalMaxPooling1D, MaxPool1D, MaxPooling1D, SpatialDropout1D, GRU, Bidirectional, AveragePooling1D, GlobalAveragePooling1D
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, LSTM, Input
from keras.layers.merge import concatenate
from keras.utils import to_categorical
from keras import layers
import tensorflow as tf

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, hamming_loss


def bigru(max_features, max_len, n_class, weight_matrix, hidden_sequences, embed_size = 300):

    inputs1 = Input(shape=(max_len,))
    embedding1 = Embedding(max_features, embed_size, weights=[weight_matrix], trainable=False)(inputs1)

    bi_gru = Bidirectional(GRU(hidden_sequences, return_sequences=True))(embedding1)
    
    global_pool = GlobalMaxPooling1D()(bi_gru)
    avg_pool = GlobalAveragePooling1D()(bi_gru)

    concat_layer = Concatenate()([global_pool, avg_pool])

    output = Dense(n_class, activation='sigmoid')(concat_layer)

    model=Model(inputs1, output)
    
    print(model.summary())

    return model

def bigru_2(max_features, max_len, n_class, weight_matrix, hidden_sequences, hidden_sequences_2, embed_size = 300):

    inputs1 = tf.keras.Input(shape=(max_len,))
    embedding1 = Embedding(max_features, embed_size, weights=[weight_matrix], trainable=False)(inputs1)

    bi_gru = Bidirectional(GRU(hidden_sequences, return_sequences=True))(embedding1)
    bi_gru2 = Bidirectional(GRU(hidden_sequences_2, return_sequences=True))(bi_gru)
    
    global_pool = GlobalMaxPooling1D()(bi_gru2)
    avg_pool = GlobalAveragePooling1D()(bi_gru2)

    concat_layer = Concatenate()([global_pool, avg_pool])

    output = Dense(n_class, activation='sigmoid')(concat_layer)

    model=Model(inputs1, output)

    
    print(model.summary())
    return model

def cnn(max_features, embed_size, weight_matrix, trainable, maxlen, filters,kernel_size, hidden_dims,n_class):

    model = Sequential()

    model.add(Embedding(max_features, embed_size, weights=[weight_matrix], trainable=trainable, input_length=maxlen))

    model.add(Dropout(0.2))
    model.add(Conv1D(filters, kernel_size, padding='valid', activation='relu',
                    strides=1))
    model.add(MaxPooling1D())
    model.add(Conv1D(filters, kernel_size, padding='valid',activation='relu'))
    model.add(MaxPooling1D())
    model.add(Flatten())

    # L2 regularization
    model.add(Dense(hidden_dims, activation = 'relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)))
    model.add(Dense(hidden_dims, activation = 'relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)))
    
    model.add(Dense(n_class, activation = 'sigmoid'))

    print(model.summary())
    return model