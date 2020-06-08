# author: Carlina Kim, Karanpal Singh, Sukriti Trehan, Victor Cuspinera
# date: 2020-06-08

'''This script will read in Q1 training and validation data from the specified directory,
preprocess the text using preprocessing.py and build the TFID vectorizer to be used later
in the model. Run this at the root project directory 

Usage: tfid_vectorizer.py --input_dir=<input_dir_path> --output_dir=<destination_dir_path>

Example:
    python src/features/tfid_vectorizer.py \
    --input_dir=data/interim/question1_models/ \
    --output_dir=data/interim/

Options:
--input_dir=<input_dir_path> Directory name with the excel files
--output_dir=<destination_dir_path> Directory for saving the vectorizer npy file
'''
#load dependencies
import sys
sys.path.insert(1, '.')
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from src.data.preprocess import Preprocessing 

from docopt import docopt

opt = docopt(__doc__)

def main(input_dir, output_dir):
        
    # Reading in datasets 

    X_train_Q1 = pd.read_excel(input_dir + "/X_train.xlsx") 
    X_valid_Q1 = pd.read_excel(input_dir + "/X_valid.xlsx")                           
 
    # Preprocess train and valid sets
    
    X_train_Q1['preprocessed_comments'] = Preprocessing().general(X_train_Q1['Comment'])
    X_valid_Q1['preprocessed_comments'] = Preprocessing().general(X_valid_Q1['Comment'])
    
    #Tfid Vectorizer Representation

    def tfid_vectorizer(train, valid):
        """
        Fits the TfidVectorizer() on your preprocessed 
        X_train set and transforms on X validation set.
        Returns the matrixes.
        """
        tfid = TfidfVectorizer() 
        X_train = tfid.fit_transform(train)
        X_valid = tfid.transform(valid)
        return X_train, X_valid
    
    #Vectorize X_train and convert Y_train to an array

    X_train, X_valid = tfid_vectorizer(X_train_Q1['preprocessed_comments'].values.astype('U'), 
                        X_valid_Q1['preprocessed_comments'].values.astype('U'))
    
    #Saving matrixes 

    np.save(output_dir + '/tfid_X_train', X_train)
    np.save(output_dir + '/tfid_X_valid', X_valid)
    
if __name__ == "__main__":
    main(opt["--input_dir"], opt["--output_dir"])