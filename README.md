
BC Stats Capstone project 2020
-----------------------------
*Text Analytics: Quantifying the Repsonses to Open-Ended Survey Questions*

[![License:
MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Authors**: Carlina Kim, Karanpal Singh, Sukriti Trehan, Victor Cuspinera
**Mentor**: Varada Kolhatkar
**Partner**: [BC Stats](https://www2.gov.bc.ca/gov/content/data/about-data-management/bc-stats)

## About
BC-Stats conducts the Work Environment Survey (WES) on BC Public Service’s ministries with the goal of identifying areas for improvement and understanding employee’s experiences in the working environment. Currently, the comments to the open-ended questions have been manually encoded. Given a large number of employees across their 26 ministries, hand-labelling comments is expensive and time-consuming. In this project we propose using natural language processing and machine learning classification techniques to automate the labelling of text responses with the goals of build an useful model to automate multi-label text classification and gather insight on trends by themes across ministries.

## Report
The final report is available [here]().

## Usage

### Recommended
To replicate the analysis, clone this GitHub repository, install the [dependencies](#dependencies) listed below, follow the next steps:

1. Add a copy of the sensitive data in the `data/raw` folder, and download the Fasttext pre-trained embeddings file `crawl-300d-2M.vec.zip` in `data/fasttext`

2. Run the following command at the command line/terminal from the root directory of this project to prepare data for the models
```
make ready
```

3. Upload the embedding matrix and padded datasets to [Google Drive](https://www.google.ca/drive/) with termination `.npy`. This files contain a vectorial representation of the words from the preprocesed comments, so they don't show any sensitive information.
 **Warning:** don't upload any other file because it may contain sensitive information.

4. Open and run the models in [Google Colab](https://colab.research.google.com/)

5. Run the following command at the command line/terminal from the root directory of this project to make predictions and the final report.
```
make results
```

This process could take couple hours.


### Running all from one command

An alternative would is to run the following command at the command line/terminal from the root directory of this project. However, this process would run the models in your computer instead of the cloud, it will only use **1 epoc** so won't return as good results, it will take several hours, and your computer may crash in the process:
```
make all
```

### Cleaning the repository

To reset the repository to a clean state, with no intermediate or results files, run the following command at the command line/terminal from the root directory of this project:
```
make clean
```

To delete all sensitive data and pre-trained embeddings, run the following command at the command line/terminal from the root directory of this project:
```
make clean_confidential
```

## Project Organization    

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── fasttext       <- Data from third party sources.
    │   ├── glove          <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   ├── figures        <- Generated graphics and figures to be used in reporting
    │   └── tables         <- General .csv files used for the report and presentation.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

