Executive Summary
=================

<span style="color:darkred">A brief and high level summary of the
project proposal.</span>  
**We should write this section after we finish the proposal.**

<br>

Introduction
============

*“I believe a well performing government, one that meets  
the service expectations of British Columbians, can only  
be achieved through a strong, highly competent and  
committed public service.”*<br> <span style="color:gray">- Wayne
Strelioff, Auditor General of British Columbia<span>

### Work Environment Survey (WES)

<style>
.column-left{
  float: left;
  width: 40%;
  text-align: center;
}
.column-center{
  float: right;
  width: 60%;
  text-align: left;
}
</style>
<img src="figures/WES_report2018.png" data-fig.align="center" style="width:70.0%" />

Since 2006, the BC Public Service has conducted the Work Environment
Survey (WES) with the goal of understanding their employees’ experience,
celebrating their successes, and identifying areas for improvement. The
survey consists of ~80 multiple choice questions, in 5-point scale, and
two open ended questions:

<br>

**Question 1.** <span style="color:#005c99">**What one thing would you
like your organization to focus on to improve your work environment?**
</span>

<span style="color:gray">*Example[1]: “Better health and social benefits
should be provided.”*</span>

**Question 2.** <span style="color:#005c99">**Have you seen any
improvements in your work environment and if so, what are the
improvements?**</span>

<span style="color:gray">*Example[2]: “Now we have more efficient
vending machines.”*</gray>

The responses to the first question have been manually coded into 13
themes and 63 sub-themes, and for the second question it has been
manually coded into 6 themes and 16 sub-themes.

<br> <br> <br>

Objectives
==========

Our project aims to apply natural language processing and machine
learning classification on these open-ended questions to automate the
process.

The specific objectives for each question are:

**Question 1**

-   <span style="color:#005c99">Build a model</span> for predicting
    label(s) for main <span style="color:#005c99">themes</span>.

-   <span style="color:#005c99">Build a model</span> for predicting
    label(s) for <span style="color:#005c99">sub-themes</span>.

-   Scalability: Identify <span style="color:#005c99">trends across
    ministries</span> and over the four specified years.

**Question 2**

-   <span style="color:#005c99">Identify labels</span> for theme
    classification and compare with existing labels.

-   Create <span style="color:#005c99">visualizations for
    executives</span> to explore the results.

<br>

It is important to mention that the first question has been addressed by
previous Capstone projects of MDS Students. In specific, the BC Stat’s
Capstone of 2019 (Quinton, Pearson, Nie), built a model that predicts
the labels of the main themes, and reached the following results:

<img src="figures/results_capstone_2019.png" data-fig.align="center" style="width:80.0%" />

*Source: [Final Report of BC Stats Capstone 2019, by Quinton,Pearson and
Nie.](https://github.com/aaronquinton/mds-capstone-bcstats/blob/master/reports/BCStats_Final_Report.pdf)*

In this case, our aim is to improve the accuracy for predicting labels
for main themes respective the results of the 2019 BC Stats Capstone
Project.

<br>

Getting Familiar with the Data
==============================

The Data consist of separated files for each question, and for each of
the years (2013, 2015, 2018, 2020), in Microsoft Excel format (.xlsx),
and contain sensitive information from employees of BC Public Services.

In specific, the information that we would use for this project for the
first question corresponds to the labeled data from 2013, 2018, 2020,
that added to around 32,000 respondents.

In the following we can see an example[3] of how this question is
presented in the database.

<table>
<thead>
<tr class="header">
<th style="text-align: left;">Comments<a href="#fn1" class="footnote-ref" id="fnref1"><sup>1</sup></a></th>
<th style="text-align: center;">CPD</th>
<th style="text-align: center;">CB</th>
<th style="text-align: center;">EWC</th>
<th style="text-align: center;">…</th>
<th style="text-align: center;">CB_Improve_benefits</th>
<th style="text-align: center;">CB_Increase_salary</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;">Better health and social benefits should be provided</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">1</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">…</td>
<td style="text-align: center;">1</td>
<td style="text-align: center;">0</td>
</tr>
</tbody>
</table>
<section class="footnotes">
<hr />
<ol>
<li id="fn1"><p>This is a fake comment as an example of the data<a href="#fnref1" class="footnote-back">↩</a></p></li>
</ol>
</section>

<br>

The classification of the previous comment is CB (Compensation and
Benefits) for theme, and CB\_Improve\_benefits (Improve benefits) as
sub-theme.

For the second question, we have labeled data from 2018, which add
around 6,000 respondents. Also, we have unlabeled data from 2015 and
2020, that represent 9,000 additional comments.

Exploratory Data Analysis
=========================

**Question 1.** <br> <span style="color:grey">**What one thing would you
like your organization to focus on to improve your work environment?**
</span>

Labels: <span style="color:#005c99">13 themes</span> and <span
style="color:#005c99">63 sub-themes</span>.

<center>
![](BCStats_Proposal_Report_files/figure-markdown_strict/unnamed-chunk-2-1.png)
</center>
Label cardinality for **themes**: **~1.4**

<center>
![](BCStats_Proposal_Report_files/figure-markdown_strict/unnamed-chunk-5-1.png)
</center>
Label cardinality for **sub-themes**: **~1.6**

<br>

**Question 2.** <br> <span style="color:grey">**Have you seen any
improvements in your work environment and if so, what are the
improvements?**</span>

Labels for 2018: <span style="color:#005c99">6 themes</span> and <span
style="color:#005c99">16 sub-themes</span>

<center>
![](BCStats_Proposal_Report_files/figure-markdown_strict/unnamed-chunk-7-1.png)
</center>
Label cardinality: **~1.6**

<br>

Challenges
==========

-   <span style="color:#005c99">Decide appropriate metric for evaluating
    accuracy</span> (considering partial correctness) for multi-label
    prediction problem.

-   Low label cardinality indicating <span
    style="color:#005c99">sparsity</span> in training data
    -   ~2 labels per comment from ~60 labels.
-   Build a model with increased performance -<span
    style="color:#005c99">higher label precision and recall</span>- than
    the MDS team last year so that it <span style="color:#005c99">can be
    deployed by BC Stats</span>.

-   <span style="color:#005c99">Class Imbalance</span> in the data
    -   skeweness in number of comments per label.

<br>

Data Science Techniques
=======================

<span style="color:darkred">**Expectatives of this section:** <br>
Describe how you will use data science techniques in the project. Be
sure to discuss the appropriateness of the data for the proposed data
science techniques, as well as difficulties the data might pose. It is
recommended to include a description of the data (variables/features and
observational units) and some examples/snippets of what the data looks
like (as a table or a visualization). Be sure to always always start
with simple data science techniques to obtain a simple version of your
data science product. There are two benefits to this approach. First,
the simple method gives you a baseline to which you can compare future
results. Second, the simple method may solve the problem, in which case
you don’t need something more complicated. For example, your first model
should not be an LSTM.</span>

<span style="color:green"> **What we had previously in Google Docs**
<br> Our first question includes labeled data from 2013, 2018, 2020,
while the second question has labeled data from 2015, 2018, 2020. Each
survey has around \_\_ respondents across \_\_ ministries. <br> Sparsity
of the data (cardinality) Multi-label problem Create fake comment and
labels (we can use real labels) (insert image of class imbalance figure)
<br> Initial observations we notice are patterns of class imbalance with
the themes and subthemes that may pose an issue with recall and
precision in the future. We also observe a low level of label
cardinality (average number of labels per comment) so we are dealing
with sparsity in our dataset. <br> For automated classification to
themes and subthemes tasks, our baseline approach will be to run TF-IDF
vectorizer and a Classifier Chains model. The past capstone group used
Binary Relevance for their multi-label classification model which treats
each label as a separate single class classification problem. In
Classifier Chains, the model forms chains in order to preserve label
correlation and believe this would be a better choice. <br> For theme
identification, our baseline is to use a standard LDA approach. For the
dashboard, we will be using Matplotlib, Altair and Plotly. The
visualizations are focused on: Identifying trends across the years
Identifying trends across ministries </span>

### Question 1

<span style="color:#005c99">Binary Relevance</span> - Base Model from
last year’s Captsone
<center>
<img src="figures/x.png" data-fig.align="center" style="width:18.0%" />
</center>
<center>
<img src="figures/br_train.png" data-fig.align="center" style="width:32.0%" />
</center>
<br> *Source: [Multi-Label Classification: Binary Relevance, by
Analytics
Vidhya](https://www.analyticsvidhya.com/blog/2017/08/introduction-to-multi-label-classification/)*

<span style="color:#005c99">Classifier Chains</span> - Proposed Base
Model
<center>
<img src="figures/cc_x.png" data-fig.align="center" style="width:25.0%" />
</center>
<center>
<img src="figures/cc_train.png" data-fig.align="center" style="width:80.0%" />
</center>
<br> *Source: [Multi-Label Classification: Classifier Chains, by
Analytics
Vidhya](https://www.analyticsvidhya.com/blog/2017/08/introduction-to-multi-label-classification/)*

-   Multi-Label Classification using TF-IDF Vectorizer with Classifier
    Chain.

### Question 2

**Theme Identifications**

-   Use clustering algorithms like <span
    style="color:#005c99">PCA</span> and <span
    style="color:#005c99">Topic Modelling</span>

**Scalability**

-   Descriptive Statistics using Matplotlib, Altair and Plotly
    -   Identify trends over the years
    -   Identify trends across Ministries

<br>

Deliverables
============

-   **<span style="color:#005c99">Data pipeline</span> with the
    documentation for our models**

<br>

-   **<span style="color:#005c99">Dash app</span> that displays the
    trends across ministries for both qualitative questions**

<center>
<img src="figures/Dash_app_sketch.png" data-fig.align="center" style="width:80.0%" />
</center>
*Source: Dash app’s sketch[4], based in [app developed by BC Stats for
the Workforce Profiles Report
2018](https://www.analyticsvidhya.com/blog/2017/08/introduction-to-multi-label-classification/).*

<br>

Timeline
========

![](figures/plan.png)

Week 1 (May 11-15) - Base Models: classification and topic modelling.  
Week 2 (May 18-22) - Begin working on advanced models & visualizations
for dashboard.  
Week 3 (May 25-29) - Continue working with advanced models & start
project reports.  
Week 4 (Jun 1-5) - Deliverables & Pipelines continuous integration.  
Week 5 (Jun 8-12) - Report Writing & Documentation.  
Week 6 (Jun 15-16) - Feedbacks & Submissions.

References
==========

-   BC Stats. (August 2018). 2018 Work Environment Survey Driver Guide.
    Site:
    <a href="https://www2.gov.bc.ca/assets/gov/data/statistics/government/wes/wes2018_driver_guide.pdf" class="uri">https://www2.gov.bc.ca/assets/gov/data/statistics/government/wes/wes2018_driver_guide.pdf</a>

-   BC Stats. (2018). Workforce Profile Report 2018. Online dashboard.
    Retrieved 2020-05-08, site
    <a href="https://securesurveys.gov.bc.ca/ERAP/workforce-profiles" class="uri">https://securesurveys.gov.bc.ca/ERAP/workforce-profiles</a>

-   Province of British Columbia. (2020). About the Work Environment
    Survey (WES). Retrieved 2020-05-09, site
    <a href="https://www2.gov.bc.ca/gov/content/data/statistics/government/employee-research/wes/" class="uri">https://www2.gov.bc.ca/gov/content/data/statistics/government/employee-research/wes/</a>

-   Quinton, A., Pearson, A., Nie, F. (2019). BC Stats Capstone Final
    Report, Quantifying the Responses to Open-Ended Survey Questions.
    GitHub account of Aaron Quinton. Site:
    <a href="https://github.com/aaronquinton/mds-capstone-bcstats/blob/master/reports/BCStats_Final_Report.pdf" class="uri">https://github.com/aaronquinton/mds-capstone-bcstats/blob/master/reports/BCStats_Final_Report.pdf</a>

-   Jain, S. (2017). Solving Multi-Label Classification problems (Case
    studies included). Analytics Vidhya. Retrieved 2020-05-05, site
    <a href="https://www.analyticsvidhya.com/blog/2017/08/introduction-to-multi-label-classification/" class="uri">https://www.analyticsvidhya.com/blog/2017/08/introduction-to-multi-label-classification/</a>

[1] This is a fake comment as examples of the data.

[2] Idem.

[3] This is a fake comment as an example of the data.

[4] This figure is just for illustrative purpose, the final version of
the app could differ from the sketch.
