
# Microsoft Academic Knowledge API wrapper

## Introduction

Microsoft Academic knowledge provides rich API'S to retrieve information from 
Microsoft Academic Graph. MAG knowledge base is web-based heterogeneous entity graph which consists of entities such as Papers, 
Field of study, Authors, Affiliations, Citation Contexts, References etc.

This tool provides a wrapper around the Knowledge API to retrieve Authors, Field of Study and Papers data.


## Installation

```
    pip install magapi-wrapper
```

or 

```
   git clone https://github.com/bethgelab/magapi_wrapper
   pip install . or python setup.py install
```



## Get Started

To access the data from Microsoft Academic Knowledge you need a key. Visit [here](https://msr-apis.portal.azure-api.net/) and subscribe.


1 **Retrieve 100 papers from one Author and save to file in csv format**

 ```
   mag-api llohgdu786786gsufzsazf --save --format=csv --AA.AuN="matthias bethge" --count=100

 ```
2 **Retrieve All papers from author from year between 2015 and 2020**

  ```
   mag-api llohgdu786786gsufzsazf --save --format=csv --count=1000 --AA.AuN="matthias bethge" -Y=2015,2020

  ```
3 **Retrieve papers from author with specific affiliation**
    
  ```
   mag-api llohgdu786786gsufzsazf --save --format=csv --count=1000 --AA.AuN="matthias bethge" --AA.AfN="university of tuebingen"

  ```
4 **Retrieve all papers from two authors**

  ```
   mag-api llohgdu786786gsufzsazf --save --format=csv --count=1000 --AA.AuN="matthias bethge,wieland brendel"

  ```
5 **Retrieve all the papers which are citing specific paper/s**

For example I want to get all the papers which are ciiting the paper `Image Style Transfer Using Convolutional Neural Networks`

  ```
   mag-api llohgdu786786gsufzsazf --save --format=csv --count=1000 --Ti="Image Style Transfer Using Convolutional Neural Networks" --citations

  ```

6 **Retrieve all the papers from University/Institute in specific domain**

    For Example retrieving all the papers in the area of Machine learning from University of Tuebingen


  ```
   mag-api llohgdu786786gsufzsazf --save --format=csv --count=1000 --AA.AfN="University of tuebingen" --F.FN="machine learning"

  ```
7 **Retrieve author profiles**

  ```
    mag-api llohgdu786786gsufzsazf --save --format=csv --entity=author --AuN="matthias bethge,wieland brendel"
  ```
   
8 **Retrieve study fields**

  ```
    mag-api llohgdu786786gsufzsazf --save --format=csv --entity="study field" --FN="physics,machine learning"
  ```

## References
1. https://docs.microsoft.com/en-us/academic-services/graph/
2. https://docs.microsoft.com/en-us/academic-services/project-academic-knowledge/introduction


## Contact

This repo is currently maintained by Kantharaju Narayanappa ([@kantharajucn](http://github.com/kantharaju)).
If you find any bugs or incorrect data please report.