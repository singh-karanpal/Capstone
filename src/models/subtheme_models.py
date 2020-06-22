# author: Carlina Kim, Karanpal Singh, Sukriti Trehan, Victor Cuspinera
# date: 2020-06-21

'''This script will create a dictionary for the hyperparameters of
deep learning models for subthemes and train all subtheme models.
Trained models will be saved as pickel files.

Usage: subthemes_model_mappings.py --input_dir=<input_dirl> --output_dir=<output_dir>

Example:
    python src/models/subtheme_models.py --input_dir=data/interim/subthemes --output_dir=data/models/Subtheme_Models
'''

import requests
from docopt import docopt
import pandas as pd
import numpy as np
import pickle

import sys
sys.path.append('src/models/')
from subthemes_models_functions import bigru, bigru_2, cnn

opt = docopt(__doc__)

def main(input_dir, output_dir):
    """
    This method will download data from URL and save it to a project directory
    
    Arguments:
    ----------
    input_dir: String
    input directory as a string where all subthemes data
    is located including padded docs and embeddings.
    
    Return:
    ----------
    save all subtheme models as pickel files.
    """
    
    # main dict
    subthemes_mappings = dict()

    # label dicts
    cb_dict = dict()
    cpd_dict = dict()
    ewc_dict = dict()
    exec_dict = dict()
    fwe_dict = dict()
    oth_dict = dict()
    re_dict = dict()
    sp_dict = dict()
    sup_dict = dict()
    sw_dict = dict()
    tepe_dict = dict()
    vmg_dict = dict()



    # loading data files for subthemes to compute hyper-parameters
    print('\n--- Loading Paddings ---')
    # CB
    padded_docs_train_cb = np.load(input_dir + '/CB/X_train_padded.npy')
    embedding_matrix_ft_cb = np.load(input_dir + '/CB/embedding_matrix.npy')
    y_train_cb = np.load(input_dir + '/CB/y_train.npy')

    # CPD
    padded_docs_train_cpd = np.load(input_dir + '/CPD/X_train_padded.npy')
    embedding_matrix_ft_cpd = np.load(input_dir + '/CPD/embedding_matrix.npy')
    y_train_cpd = np.load(input_dir + '/CPD/y_train.npy')

    # EWC
    padded_docs_train_ewc = np.load(input_dir +'/EWC/X_train_padded.npy')
    embedding_matrix_ft_ewc = np.load(input_dir + '/EWC/embedding_matrix.npy')
    y_train_ewc = np.load(input_dir + '/EWC/y_train.npy')

    # Exec
    padded_docs_train_exec = np.load(input_dir +'/Exec/X_train_padded.npy')
    embedding_matrix_ft_exec = np.load(input_dir + '/Exec/embedding_matrix.npy')
    y_train_exec = np.load(input_dir + '/Exec/y_train.npy')

    # FWE
    padded_docs_train_fwe = np.load(input_dir +'/FWE/X_train_padded.npy')
    embedding_matrix_ft_fwe = np.load(input_dir + '/FWE/embedding_matrix.npy')
    y_train_fwe = np.load(input_dir + '/FWE/y_train.npy')

    # OTH
    padded_docs_train_oth = np.load(input_dir +'/OTH/X_train_padded.npy')
    embedding_matrix_ft_oth = np.load(input_dir + '/OTH/embedding_matrix.npy')
    y_train_oth = np.load(input_dir + '/OTH/y_train.npy')

    # RE
    padded_docs_train_re = np.load(input_dir +'/RE/X_train_padded.npy')
    embedding_matrix_ft_re = np.load(input_dir + '/RE/embedding_matrix.npy')
    y_train_re = np.load(input_dir + '/RE/y_train.npy')

    # SP
    padded_docs_train_sp = np.load(input_dir +'/SP/X_train_padded.npy')
    embedding_matrix_ft_sp = np.load(input_dir + '/SP/embedding_matrix.npy')
    y_train_sp = np.load(input_dir + '/SP/y_train.npy')

    # Sup
    padded_docs_train_sup = np.load(input_dir +'/Sup/X_train_padded.npy')
    embedding_matrix_ft_sup = np.load(input_dir + '/Sup/embedding_matrix.npy')
    y_train_sup = np.load(input_dir + '/Sup/y_train.npy')

    # SW
    padded_docs_train_sw = np.load(input_dir +'/SW/X_train_padded.npy')
    embedding_matrix_ft_sw = np.load(input_dir + '/SW/embedding_matrix.npy')
    y_train_sw = np.load(input_dir + '/SW/y_train.npy')

    # TEPE
    padded_docs_train_tepe = np.load(input_dir +'/TEPE/X_train_padded.npy')
    embedding_matrix_ft_tepe = np.load(input_dir + '/TEPE/embedding_matrix.npy')
    y_train_tepe = np.load(input_dir + '/TEPE/y_train.npy')

    # VMG
    padded_docs_train_vmg = np.load(input_dir +'/VMG/X_train_padded.npy')
    embedding_matrix_ft_vmg = np.load(input_dir + '/VMG/embedding_matrix.npy')
    y_train_vmg = np.load( input_dir + '/VMG/y_train.npy')

    print('--- Creating Dictionaries ---')


    cb_dict.update({
        'model':'cnn',
        'padded_docs_train':padded_docs_train_cb,
        'y_train':y_train_cb,
        'max_features':embedding_matrix_ft_cb.shape[0],
        'maxlen':padded_docs_train_cb.shape[1],
        'n_class':y_train_cb.shape[1],
        'weight_matrix':embedding_matrix_ft_cb,
        'batch_size': 128,
        'filters':250,
        'kernel_size':3,
        'hidden_dims':250,
        'epochs':7,
        'embed_size':300
    })

    subthemes_mappings.update({'CB':cb_dict})

    cpd_dict.update({
        'model':'bigru',
        'padded_docs_train':padded_docs_train_cpd,
        'y_train_':y_train_cpd,
        'max_features':embedding_matrix_ft_cpd.shape[0],
        'max_len':padded_docs_train_cpd.shape[1],
        'n_class':y_train_cpd.shape[1],
        'weight_matrix':embedding_matrix_ft_cpd, 
        'hidden_sequences':100,
        'epochs':6, 
        'batch_size':100, 
        'verbose':1
    })

    subthemes_mappings.update({'CPD': cpd_dict})

    ewc_dict.update({
        'model':'bigru',
        'padded_docs_train':padded_docs_train_ewc,
        'y_train':y_train_ewc,
        'max_features':embedding_matrix_ft_ewc.shape[0], 
        'max_len':padded_docs_train_ewc.shape[1], 
        'n_class':y_train_ewc.shape[1],
        'weight_matrix':embedding_matrix_ft_ewc, 
        'hidden_sequences': 100,
        'epochs':15, 
        'batch_size':200, 
        'verbose':1
    })

    subthemes_mappings.update({'EWC':ewc_dict})

    exec_dict.update({
        'model':'bigru',
        'padded_docs_train':padded_docs_train_exec,
        'y_train':y_train_exec,
        'max_features':embedding_matrix_ft_exec.shape[0], 
        'max_len':padded_docs_train_exec.shape[1], 
        'n_class':y_train_exec.shape[1],
        'weight_matrix':embedding_matrix_ft_exec, 
        'hidden_sequences': 100,
        'epochs':15, 
        'batch_size':256, 
        'verbose':1
    })

    subthemes_mappings.update({'Exec': exec_dict})

    fwe_dict.update({
        'model':'bigru_2',
        'padded_docs_train':padded_docs_train_fwe,
        'y_train':y_train_fwe,
        'max_features':embedding_matrix_ft_fwe.shape[0], 
        'max_len':padded_docs_train_fwe.shape[1], 
        'n_class':y_train_fwe.shape[1],
        'weight_matrix':embedding_matrix_ft_fwe, 
        'hidden_sequences':200, 
        'hidden_sequences_2':75,
        'epochs':10, 
        'batch_size':156, 
        'verbose':1
    })

    subthemes_mappings.update({'FWE': fwe_dict})

    oth_dict.update({
        'model':'bigru_2',
        'padded_docs_train':padded_docs_train_oth,
        'y_train':y_train_oth,
        'max_features':embedding_matrix_ft_oth.shape[0], 
        'max_len':padded_docs_train_oth.shape[1], 
        'n_class':y_train_oth.shape[1],
        'weight_matrix':embedding_matrix_ft_oth, 
        'hidden_sequences': 100, 
        'hidden_sequences_2': 75,
        'epochs':15, 
        'batch_size':200, 
        'verbose':1
    })

    subthemes_mappings.update({'OTH': oth_dict})

    re_dict.update({
        'model':'bigru_2',
        'padded_docs_train':padded_docs_train_re,
        'y_train':y_train_re,
        'max_features':embedding_matrix_ft_re.shape[0], 
        'max_len':padded_docs_train_re.shape[1], 
        'n_class':y_train_re.shape[1],
        'weight_matrix':embedding_matrix_ft_re, 
        'hidden_sequences':200, 
        'hidden_sequences_2':75,
        'epochs':12, 
        'batch_size':156, 
        'verbose':1
    })

    subthemes_mappings.update({'RE':re_dict})

    sp_dict.update({
        'model':'bigru',
        'padded_docs_train':padded_docs_train_sp,
        'y_train':y_train_sp,
        'max_features':embedding_matrix_ft_sp.shape[0], 
        'max_len':padded_docs_train_sp.shape[1], 
        'n_class':y_train_sp.shape[1],
        'weight_matrix':embedding_matrix_ft_sp, 
        'hidden_sequences':100,
        'epochs':15, 
        'batch_size':256, 
        'verbose':1
    })

    subthemes_mappings.update({'SP':sp_dict})

    sup_dict.update({
        'model':'bigru',
        'padded_docs_train':padded_docs_train_sup,
        'y_train':y_train_sup,
        'max_features':embedding_matrix_ft_sup.shape[0], 
        'max_len':padded_docs_train_sup.shape[1], 
        'n_class':y_train_sup.shape[1],
        'weight_matrix':embedding_matrix_ft_sup, 
        'hidden_sequences':100,
        'epochs':20, 
        'batch_size':256, 
        'verbose':1
    })

    subthemes_mappings.update({'Sup':sup_dict})

    sw_dict.update({
        'model':'bigru',
        'padded_docs_train':padded_docs_train_sw,
        'y_train':y_train_sw,
        'max_features':embedding_matrix_ft_sw.shape[0], 
        'max_len':padded_docs_train_sw.shape[1], 
        'n_class':y_train_sw.shape[1],
        'weight_matrix':embedding_matrix_ft_sw, 
        'hidden_sequences':100,
        'epochs':20, 
        'batch_size':256, 
        'verbose':1
    })

    subthemes_mappings.update({'SW':sw_dict})

    tepe_dict.update({
        'model':'bigru',
        'padded_docs_train':padded_docs_train_tepe,
        'y_train':y_train_tepe,
        'max_features':embedding_matrix_ft_tepe.shape[0], 
        'max_len':padded_docs_train_tepe.shape[1], 
        'n_class':y_train_tepe.shape[1],
        'weight_matrix':embedding_matrix_ft_tepe, 
        'hidden_sequences': 100,
        'epochs':6, 
        'batch_size':256, 
        'verbose':1
    })

    subthemes_mappings.update({'TEPE':tepe_dict})

    vmg_dict.update({
        'model':'bigru_2',
        'padded_docs_train':padded_docs_train_vmg,
        'y_train':y_train_vmg,
        'max_features':embedding_matrix_ft_vmg.shape[0], 
        'max_len':padded_docs_train_vmg.shape[1], 
        'n_class':y_train_vmg.shape[1],
        'weight_matrix':embedding_matrix_ft_vmg, 
        'hidden_sequences':100, 
        'hidden_sequences_2':75,
        'epochs':15, 
        'batch_size':256, 
        'verbose':1
        
    })

    subthemes_mappings.update({'VMG':vmg_dict})

    print('--- Training Subthemes ---')
    keynames = list(subthemes_mappings.keys())[1:2]

    for sub_theme in keynames:
        
        print('\n--- Training for '+sub_theme+' ---')

        model_type = subthemes_mappings.get(sub_theme).get('model')

        if model_type == 'bigru':

            print('**bigru training')

            # parameters to be passed
            # max_features, max_len, n_class, weight_matrix, hidden_sequences, embed_size = 300
            bigru_model = bigru(subthemes_mappings.get(sub_theme).get('max_features'), 
                                subthemes_mappings.get(sub_theme).get('maxlen'), 
                                subthemes_mappings.get(sub_theme).get('n_class'), 
                                subthemes_mappings.get(sub_theme).get('weight_matrix'), 
                                subthemes_mappings.get(sub_theme).get('hidden_sequences'), 
                                embed_size = 300)

            bigru_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy', 'categorical_accuracy'])

            bigru_model.fit(subthemes_mappings.get(sub_theme).get('padded_docs_train'), 
                                subthemes_mappings.get(sub_theme).get('y_train'), 
                                validation_split=0.15, 
                                epochs=subthemes_mappings.get(sub_theme).get('epochs'), 
                                batch_size=subthemes_mappings.get(sub_theme).get('batch_size'), 
                                verbose=subthemes_mappings.get(sub_theme).get('verbose'))

            bigru_model.save(output_dir + '/' + sub_theme +'_model')


        elif model_type == 'bigru_2':

            print('**bigru2 training')

            # parameters to be passed
            # max_features, max_len, n_class, weight_matrix, hidden_sequences, hidden_sequences_2, embed_size = 300
            bigru_2_model = bigru_2(subthemes_mappings.get(sub_theme).get('max_features'),
                                subthemes_mappings.get(sub_theme).get('maxlen'), 
                                subthemes_mappings.get(sub_theme).get('n_class'), 
                                subthemes_mappings.get(sub_theme).get('weight_matrix'), 
                                subthemes_mappings.get(sub_theme).get('hidden_sequences'), 
                                subthemes_mappings.get(sub_theme).get('hidden_sequences2'), 
                                embed_size = 300)

            bigru_2_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy', 'categorical_accuracy'])

            bigru_2_model.fit(subthemes_mappings.get(sub_theme).get('padded_docs_train'),
                                subthemes_mappings.get(sub_theme).get('y_train'),
                                validation_split=0.15, 
                                epochs=subthemes_mappings.get(sub_theme).get('epochs'), 
                                batch_size=subthemes_mappings.get(sub_theme).get('batch_size'), 
                                verbose=subthemes_mappings.get(sub_theme).get('verbose'))

            bigru_2_model.save(output_dir + '/' + sub_theme +'_model')

            

        elif model_type == 'cnn':

            print('**cnn training')

            # parameters to be passed
            # max_features, embed_size, weight_matrix, trainable, maxlen, filters,kernel_size, hidden_dims,n_class
            cnn_model = cnn(subthemes_mappings.get(sub_theme).get('max_features'),
                                subthemes_mappings.get(sub_theme).get('embed_size'),
                                subthemes_mappings.get(sub_theme).get('weight_matrix'),
                                True,
                                subthemes_mappings.get(sub_theme).get('maxlen'),
                                subthemes_mappings.get(sub_theme).get('filters'),
                                subthemes_mappings.get(sub_theme).get('kernel_size'),
                                subthemes_mappings.get(sub_theme).get('hidden_dims'),
                                subthemes_mappings.get(sub_theme).get('n_class')
                                )

            cnn_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
            
            cnn_model.fit(subthemes_mappings.get(sub_theme).get('padded_docs_train'), 
                            subthemes_mappings.get(sub_theme).get('y_train'), 
                            batch_size=subthemes_mappings.get(sub_theme).get('batch_size'), 
                            epochs=subthemes_mappings.get(sub_theme).get('epochs'), 
                            class_weight='auto', 
                            validation_split=0.15)

            cnn_model.save(output_dir + '/' + sub_theme +'_model')


if __name__ == "__main__":
    main(opt["--input_dir"], opt["--output_dir"])





