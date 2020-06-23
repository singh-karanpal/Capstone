.PHONY: clean data lint requirements sync_data_to_s3 sync_data_from_s3

# Make file for BC Stats Capstone project 2020
# author: Carlina Kim, Karanpal Singh, Sukriti Trehan, Victor Cuspinera
# date: 2020-06-05
# 
# This driver script split the data, create the embedding matrix and padded 
# files, run the models, and clean the repo. This script takes no arguments. 
#
# usage: make requirements
#						to install all Python and R pacakges for Analysis
# 
# usage: make all
#						to run all the analysis
#
# usage: make ready
#						to prepare data for the models
#
# usage: make dashboard
#						to run Dashboard using R as a server
#
# usage: make clean
#						to clean up all the intermediate files
#
# usage: make clean_confidential
#						to clean up all raw data and pre-trained embeddings


#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = 591_capstone_2020_bc_stats_mds
PYTHON_INTERPRETER = python3

ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python Dependencies
requirements: 
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt
	$ Rscript -e 'install.packages("shiny", repos="http://cran.us.r-project.org")'
	$ Rscript -e 'install.packages("shinydashboard", repos="http://cran.us.r-project.org")'
	$ Rscript -e 'install.packages("RColorBrewer", repos="http://cran.us.r-project.org")'
	$ Rscript -e 'install.packages("shinycssloaders", repos="http://cran.us.r-project.org")'
	$ Rscript -e 'install.packages("shinyBS", repos="http://cran.us.r-project.org")'
	$ Rscript -e 'install.packages("tidyverse", repos="http://cran.us.r-project.org")'
	$ Rscript -e 'install.packages("wordcloud", repos="http://cran.us.r-project.org")'
	$ Rscript -e 'install.packages("SnowballC", repos="http://cran.us.r-project.org")'
	$ Rscript -e 'install.packages("tm", repos="http://cran.us.r-project.org")'
	$ Rscript -e 'install.packages("readxl", repos="http://cran.us.r-project.org")'
	$ Rscript -e 'install.packages("tidytext", repos="http://cran.us.r-project.org")'
	$ Rscript -e 'install.packages("textdata", repos="http://cran.us.r-project.org")'
	$ Rscript -e 'install.packages("tidyr", repos="http://cran.us.r-project.org")'
	$ Rscript -e 'install.packages("tokenizers", repos="http://cran.us.r-project.org")'
	$ Rscript -e 'install.packages("igraph", repos="http://cran.us.r-project.org")'
	$ Rscript -e 'install.packages("ggraph", repos="http://cran.us.r-project.org")'
	$ Rscript -e 'install.packages("magrittr", repos="http://cran.us.r-project.org")'
	$ Rscript -e 'install.packages("stringr", repos="http://cran.us.r-project.org")'
	$ Rscript -e 'install.packages("data.table", repos="http://cran.us.r-project.org")'
	$ Rscript -e 'install.packages("Hmisc", repos="http://cran.us.r-project.org")'
	$ Rscript -e 'install.packages("sentimentr", repos="http://cran.us.r-project.org")'
	$ Rscript -e 'install.packages("rlang", repos="http://cran.us.r-project.org")'
	


## Make Dataset
data: requirements
	$(PYTHON_INTERPRETER) src/data/make_dataset.py data/raw data/processed

## Prepare data for the models
ready:
	python src/data/merge_split_data.py --input_dir=data/raw/ --output_dir=data/interim/
	python src/data/ministries_data.py --input_dir=data/ --output_dir=data/interim/
	python src/data/embeddings.py --model='fasttext' --level='theme' --label_name='' --include_test='True'
	python src/data/subthemes.py --input_dir='data/interim/question1_models/advance/' --model='fasttext' --include_test='True'

dashboard:
	R -e "shiny::runApp('src/visualization/', launch.browser=TRUE)"

## Delete all compiled Python files
clean:
	rm -r data/interim/question1_models/basic/*
	rm -r data/interim/question1_models/advance/*
	rm -r data/interim/question2_models/*
	find data/interim/subthemes/. -mindepth 1 ! -name *.pickle -delete

	# find . -type f -name "*.py[co]" -delete
	# find . -type d -name "__pycache__" -delete

## Delete all confidential files
clean_confidential:
	rm -r data/raw/*
	find data/fasttext/. -mindepth 1 ! -name *.md -delete
	find data/glove/. -mindepth 1 ! -name *.md -delete