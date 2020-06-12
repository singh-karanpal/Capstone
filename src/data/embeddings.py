# author: Carlina Kim, Karanpal Singh, Sukriti Trehan, Victor Cuspinera
# date: 2020-06-10

'''This script load datasets, perform preprocessing on the comments, 
get the embedding matrix and padded dataset for train, validation and
test data.

Usage: src/data/embeddings.py --model=<model> --level=<level> --label_name=<label_name> --include_test=<include_test>
'''

import pandas as pd
import numpy as np
import os
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import codecs
from docopt import docopt


opt = docopt(__doc__)

def main(model, level, label_name, include_test):
    include_test = True if str(include_test).lower() == "true" else False
    emb = Embeddings()
    emb.make_embeddings(model=model, level=level, label_name=label_name, include_test=include_test)
    print('Thanks for your patience, the embedding process has finished!\n')
    return

class Embeddings:
    #Class for doing the embeddings and padded datasets

    def load_data(self, level="theme", label_name="", include_test=False):
        """
        Auxiliar function used to load the datasets of themes or a 
        specific Sub-theme, preprocess the X datasets and calculate
        the basic parameters that will use in other functions of
        this class.

        Parameters
        -------------
        level : (str)
            options are 'theme' and 'subtheme'
        label_name : (str)
            code of the sub-theme
        include_test : (boolean)
            True/False option to include or not the test dataset
        
        Returns
        -------------
        Nothing
        
        Example
        -------------
        from embeddings import Embeddings
        model = Embeddings()
        model.load_data(level="subtheme", label_name="FWE")
        """
        subthemes = ['CPD', 'CB', 'EWC', 'Exec', 'FWE',
            'SP', 'RE', 'Sup', 'SW', 'TEPE', 'VMG', 'OTH']
            
        if level == "theme":
            root = 'data/interim/question1_models/'
            exten = '.xlsx'
        else:
            root = 'data/interim/subthemes/' + label_name + '/'
            exten = '_subset.xlsx'

        X_train = pd.read_excel(root + 'X_train' + exten)['Comment'].tolist()
        X_valid = pd.read_excel(root + 'X_valid' + exten)['Comment'].tolist()
        self.y_train = pd.read_excel(root + 'y_train' + exten)
        self.y_valid = pd.read_excel(root + 'y_valid' + exten)
        if include_test:
            X_test = pd.read_excel(root + 'X_test' + exten)['Comment'].tolist()
            self.y_test = pd.read_excel(root + 'y_test' + exten)
        print('\nLoading: files were sucessfuly loaded.')

        # Preprocess the data
        from preprocess import Preprocessing
        import sys
        sys.path.append('src/data/')
        from preprocess import Preprocessing

        print('Preprocess: this step would take time, please be patient.')
        self.X_train = Preprocessing().general(X_train)
        self.X_valid = Preprocessing().general(X_valid)
        if include_test:
            self.X_test = Preprocessing().general(X_test)

        # Get parameters
        self.max_len = max(len(comment.split()) for comment in X_train)
        self.vect=Tokenizer()
        self.vect.fit_on_texts(X_train)
        self.vocab_size = len(self.vect.word_index) + 1

        # Passing the root to save info in the same folder
        self.root = root
        return


    def make_embeddings(self, model="fasttext", level="theme", label_name="", include_test=False):
        """
        Function that gets the embeddings and padding datasets
        for themes or a specific sub-theme using GloVe vector 
        or Fasttext embeddings, and save these files in the
        correspondent folder.

        Parameters
        -------------
        model : (str)
            options are 'fasttext' and 'glove'
        level : (str)
            options are 'theme' and 'subtheme'
        label_name : (str)
            code of the sub-theme
        include_test : (boolean)
            True/False option to include or not the test dataset
        
        Returns
        -------------
        Nothing
        
        Example
        -------------
        from embeddings import Embeddings
        model = Embeddings()
        model.make_embeddings(level="subtheme", label_name="FWE")
        """
        # Loading datasets
        self.load_data(level, label_name, include_test)

        # Loading the whole embedding into memory
        print('Load Embeddings: loading the whole embedding into memory.')
        embeddings_index = dict()
        if model == "fasttext":
            f = codecs.open('data/fasttext/crawl-300d-2M.vec')
        elif model == "glove":
            f = open('data/glove/glove.6B.300d.txt')

        for line in f:
            values = line.split()#.rsplit(' ')
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = coefs
        f.close()

        # Create a weight matrix for words in training docs
        print('Embeddings: creating a weight matrix for words using', model, "model.")
        embedding_matrix = np.zeros((self.vocab_size, 300))
        for word, i in self.vect.word_index.items():
            embedding_vector = embeddings_index.get(word)
            if embedding_vector is not None:
                embedding_matrix[i] = embedding_vector

        # Padding data
        print('Padding: now is time for padding the embedding matrices.')
        encoded_docs_train = self.vect.texts_to_sequences(self.X_train)
        padded_docs_train = pad_sequences(encoded_docs_train, maxlen=self.vocab_size, padding='post')
        encoded_docs_valid = self.vect.texts_to_sequences(self.X_valid)
        padded_docs_valid = pad_sequences(encoded_docs_valid, maxlen=self.vocab_size, padding='post')
        if include_test:
            encoded_docs_test = self.vect.texts_to_sequences(self.X_test)
            padded_docs_test = pad_sequences(encoded_docs_test, maxlen=self.vocab_size, padding='post')

        # Saving the embedding matrix
        print('Save: saving files in ', self.root, 'directory.')
        np.save(self.root + 'embedding_matrix_' + model, embedding_matrix)

        # Saving the padding X's datafiles
        np.save(self.root + 'X_train_' + model, padded_docs_train)
        np.save(self.root + 'X_valid_' + model, padded_docs_valid)
        if include_test:
            np.save(self.root + 'X_test_' + model, padded_docs_test)

        # Saving the padding y's datafiles
        np.save(self.root + 'y_train', self.y_train)
        np.save(self.root + 'y_valid', self.y_valid)
        if include_test:
            np.save(self.root + 'y_test', self.y_test)

        return


if __name__ == "__main__":
    main(opt["--model"], opt["--level"], opt["--label_name"], opt["--include_test"])
