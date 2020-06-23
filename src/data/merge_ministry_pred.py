# author: Carlina Kim, Karanpal Singh, Sukriti Trehan, Victor Cuspinera
# date: 2020-06-12

'''This script read ministries' comments data from interim directory and predicted
labels of question 1 from interim directory, joins both databases, and saves it in specified directory.
There are 2 parameters Input and Output Path where you want to write this data.

Usage: merge_ministry_pred.py --input_dir=<input_dir_path> --output_dir=<destination_dir_path>

Example:
    python src/data/merge_ministry_pred.py --input_dir=data/interim --output_dir=data/interim/

Options:
--input_dir=<input_dir_path> Location of data Directory
--output_dir=<destination_dir_path> Directory for saving ministries files
'''

import numpy as np
import pandas as pd

from docopt import docopt

opt = docopt(__doc__)

def main(input_dir, output_dir):

    print("\n--- START: merge_ministry_pred.py ---")
    
    ### Question 1 - Predictions on 2015 dataset ###

    # Ministries data
    print("Loading Q1 ministries' data and predictions into memory.")

    # QUAN 2015
    ministries_q1 = pd.read_excel(input_dir + "/question1_models/advance/ministries_Q1.xlsx")
    ministries_2015 = pd.read_excel(input_dir + "/question1_models/advance/ministries_2015.xlsx")
    pred_2015 = np.load(input_dir + "/question1_models/advance/theme_question1_2015.npy")

    
    columns_basic = ['Telkey', 'Comment', 'Year', 'Ministry', 'Ministry_id']
    columns_labels = ['CPD', 'CB', 'EWC', 'Exec', 'FEW', 'SP', 'RE', 'Sup', 
                     'SW', 'TEPE', 'VMG', 'OTH']
    columns_order = columns_basic + columns_labels

    pred_2015 = pd.DataFrame(pred_2015, columns=columns_labels)
    ministries_q1 = ministries_q1[columns_order]
    
    ministries_pred_2015 = pd.concat([ministries_2015, pred_2015], axis=1)
    ministries_q1_all = pd.concat([ministries_q1, ministries_pred_2015], axis=0)


    ### Question 2 - Predictions on all the data ###

    # Ministries data
    print("Loading Q2 ministries' data and predictions into memory.")

    # QUAN 2018
    ministries_q2 = pd.read_excel(input_dir + "/question2_models/ministries_Q2.xlsx")
    pred_ministries = np.load(input_dir + "/question2_models/pred_ministries.npy")

    pred_ministries = pd.DataFrame(pred_ministries, columns=['CPD', 'CB', 'EWC', 'Exec', 'FEW', 'SP', 'RE', 'Sup', 'SW', 'TEPE', 'VMG', 'OTH'])
    
    print("Merging the dataframes")
    ministries_pred_q2 = pd.concat([ministries_q2, pred_ministries], axis=1)
    
    ## Saving Excel files
    print("Saving merged datasets")
    ministries_q1_all.to_excel(output_dir + "/question1_models/advance/ministries_Q1_all.xlsx", index=False)
    ministries_pred_q2.to_excel(output_dir + "/question2_models/ministries_Q2_pred.xlsx", index=False)

    print("--- END: merge_ministry_pred.py ---\n")

if __name__ == "__main__":
    main(opt["--input_dir"], opt["--output_dir"])
