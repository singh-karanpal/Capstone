BC Stats Proposal
================
Carlina Kim, Karanpal Singh, Sukriti Trehan, Victor Cuspinera
2020-05-07

## R Markdown

This is an R Markdown document. Markdown is a simple formatting syntax
for authoring HTML, PDF, and MS Word documents. For more details on
using R Markdown see <http://rmarkdown.rstudio.com>.

``` r
library(vegawidget)
library(reticulate)
library(timevis)
use_python('/usr/local/bin/python')
```

## Introduction

![](%22figures/WES_report2018.png%22)

**Work Environment Survey (WES)**

  - Survey conducted by BC Stats for employees of BC Public Service.

  - Measures the health of the work environments.

  - 80 multiple choice questions (5 point scale) and 2 open-ended
    questions.

  - 2013, 2015, 2018, and 2020 across 26 Ministries.

## Introduction

<br>

### Open-ended Questions

<br>

**Question
1**

### <b> <span style="color:#005c99"> What one thing would you like your organization to focus on to improve your work environment? </span></b>

Example: *“Better health and social benefits should be provided.”*

<br>

rn

**Question
2**

### <b> <span style="color:red"> Have you seen any improvements in your work environment and if so, what are the improvements? </span> </b>

Example: *“Now we have more efficient vending machines.”*

<br> <br> <font size="3"> \*Note: these are fake comments as examples of
the data. </font>
