# TikTok Analysis

The goal of this project is to gather insights from the social media platform TikTok and its political impact. In this case two prominent hashtags are compared: #trump2020 and #biden2020. 

## data/

Data is gathered with the usage of [TikTokApi](https://github.com/davidteather/TikTok-Api). 
In the data folder are three types of data
    - Graphs
    - Raw Data
    - Processed Data

## src/

### src/preprocessing.ipynb

The raw data from data/raw/... is transformed to a usable format and saved into data/processed/...

### src/create_graph.ipynb

First, an networkx MultiGraph is created with two node types: users and hashtags. Second, multiple edges are accumulated and merged to create edges with weight > 1.0.
The resulting graph is undirected and saved as .gexf (gephi file) into data/graphs/...

### src/data_visualizations.ipynb

This notebook is used to create plots to show the affiliation for each hashtag.

## gephi/

Contains graph projects created in gephi.

