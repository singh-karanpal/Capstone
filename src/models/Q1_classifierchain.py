# author: Carlina Kim, Karanpal Singh, Sukriti Trehan, Victor Cuspinera
# date: 2020-06-08

'''This script will read in the tfid vectorizer embeddings of train and validation set and 
conduct a Classifier Chain baseline model.
It will save the model to the specified directory and save a csv data frame with the training 
accuracy, validation accuracy, hamming loss, precision, recall and f1 results.
There are 2 parameters Input and Output Path where you want to write this data.

Usage: Q1_classifierchain.py --input_dir=<input_dir_path> --output_dir=<destination_dir_path>

Example:
    python src/models/Q1_classifierchain.py \
    --input_dir=data/interim/ \
    --output_dir=models/

Options:
--input_dir=<input_dir_path> Directory name for the vectorizer excel files
--output_dir=<destination_dir_path> Directory for saving model and results in a csv file
'''
#load dependencies
import numpy as np
import pandas as pd
from skmultilearn.problem_transform import ClassifierChain
from sklearn.svm import LinearSVC
from sklearn.metrics import hamming_loss, accuracy_score, recall_score, precision_score, f1_score
import pickle
import scipy.sparse
import os

from docopt import docopt

opt = docopt(__doc__)

def main(input_dir, output_dir):
    
    # Reading in y datasets                           
    y_train_Q1 = pd.read_excel(input_dir + "/question1_models/y_train.xlsx") 
    y_valid_Q1 = pd.read_excel(input_dir + "/question1_models/y_valid.xlsx")
    
    #Read in tfid vectorizers
    X_train = scipy.sparse.load_npz(input_dir + '/tfid_X_train.npz')
    X_valid = scipy.sparse.load_npz(input_dir + '/tfid_X_valid.npz')

    #slice y to themes and subthemes
    subthemes_ytrain = y_train_Q1.loc[:, 'CPD_Improve_new_employee_orientation':'Unrelated'] #62
    subthemes_yvalid = y_valid_Q1.loc[:, 'CPD_Improve_new_employee_orientation':'Unrelated']

    themes_ytrain = y_train_Q1.loc[:, 'CPD': 'OTH'] #12
    themes_yvalid = y_valid_Q1.loc[:, 'CPD': 'OTH']

    if np.any(np.sum(subthemes_ytrain, axis=0) == 0):
            subthemes_yvalid = subthemes_yvalid.drop(subthemes_yvalid.columns[np.where(np.sum(subthemes_ytrain, axis=0) == 0)[0]], axis=1)
            subthemes_ytrain = subthemes_ytrain.drop(subthemes_ytrain.columns[np.where(np.sum(subthemes_ytrain, axis=0) == 0)[0]], axis=1)

    print("data getting and slicing success")

    #Classifier Chain function
    results_dict = []

    def Classifier_Chain(ytrain, yvalid, base_model):
        """
        Fits a Classifier Chain Model with LinearSVC as base classifier 
        specifiying either themes or subthemes of Y.
        Returns a table of results showing training score, validation score, 
        validation recall, precision scores, hamming loss, and f1.
        """
        classifier_chain = ClassifierChain(base_model)
        model = classifier_chain.fit(X_train, ytrain)
        
        train = model.score(X_train, np.array(ytrain)) 
        valid = model.score(X_valid, np.array(yvalid)) 
        predictions = model.predict(X_valid)
        hamming = hamming_loss(np.array(yvalid), predictions)
        recall = recall_score(np.array(yvalid), predictions, average= 'micro') 
        precision = precision_score(np.array(yvalid), predictions, average= 'micro') 
        f1 = f1_score(np.array(yvalid), predictions, average='micro')
            
        if ytrain.shape[1] == 62: 
            class_name = 'Subtheme'
        else:
            class_name = 'Theme'
        print(class_name)
        
        case = {'Class': class_name,
            'Train Accuracy': train,
            'Validation Accuracy': valid,
            'Hamming Loss': hamming,
            'Recall Score': recall,
            'Precision Score': precision,
            'F1 Score': f1}
    
        results_dict.append(case)
    
    #Theme
    model1 = Classifier_Chain(themes_ytrain, themes_yvalid, LinearSVC())

    print("model for themes success")
    
    #Subthemes
    model2 = Classifier_Chain(subthemes_ytrain, subthemes_yvalid, LinearSVC())
    
    print("model for sub themes success")

    #Dataframe of results 
    df = pd.DataFrame(results_dict)

    #Saving dataframe results as csv 
    df.to_csv('reports/figures/classifier_chain_results.csv')
    print("saved results dataframe in reports/figures")
    
    #Saving models as pickle

    with open(output_dir + 'baseline_theme.pkl', 'wb') as f:
        pickle.dump(model1, f)
    print("saved model in", output_dir)

    with open(output_dir + 'baseline_subtheme.pkl', 'wb') as f:
        pickle.dump(model2, f)

    
if __name__ == "__main__":
    main(opt["--input_dir"], opt["--output_dir"])
