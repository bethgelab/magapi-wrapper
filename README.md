
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
Once you have the key, you can use the key to retrieve the data.

### Usage

`mag-api` is a console script, it can be called with your key and other optional arguments.

`mag-api key [optional-args]` 



*  key                   Key from Microsoft Academic Knowledge API. Visit
                        https://msr-apis.portal.azure-api.net/ to get your key


*  --entity {paper,author,affiliation,study field}
                        Entity type to download
*  --save                Path to store the file. By default it will be in
                        Downloads
*  --format {csv,json}
*  --count count         Number documents to be downloaded
*  --AA.AfId affiliation_id
                        Author affiliation id
*  --AA.AfN affiliation_name
                        Author affiliation name, comma separated values for
                        more than one value
*  --AA.AuId AA.AUID     Author Id from Microsoft Academic, comma separated ids
                        for more than one. You can get the ID from
                        https://academic.microsoft.com
*  --AA.AuN author_name  Author name. Comma separated names for multiple
                        authors
*  --D publication_date  Date published in YYYY-MM-DD format. Which accepts <,
                        > and range
*  --F.FN study_field    Field of study. Comma separated values for more than
                        one field
*  --Id paper_id         Paper ID from Microsoft Academic Graph. You can get
                        the ID from https://academic.microsoft.com
*  --Ti title            Paper title. This will not accept only English
                        characters
*  --Y publication_year  Publication Year. It can also accepts >, < and <>
*  --citations           This field returns all the cited papers for given
                        titles or paper ids
*  --AuN author_name     Author name/s to download authors profile
*  --FN field_name       Field of study to download Study field statistics


### Examples

Using `64d4420ee3584a6d81feac210a7e5019` as a dummy key.  

1 **Retrieve 100 papers from one Author and save to file in csv format**

 ```
   mag-api 64d4420ee3584a6d81feac210a7e5019 --save --format=csv --AA.AuN="matthias bethge" --count=100

 ```
2 **Retrieve All papers from author from year between 2015 and 2020**

  ```
   mag-api 64d4420ee3584a6d81feac210a7e5019 --save --format=csv --count=1000 --AA.AuN="matthias bethge" -Y=2015,2020

  ```
3 **Retrieve papers from author with specific affiliation**
    
  ```
   mag-api 64d4420ee3584a6d81feac210a7e5019 --save --format=csv --count=1000 --AA.AuN="matthias bethge" --AA.AfN="university of tuebingen"

  ```
4 **Retrieve all papers from two authors**

  ```
   mag-api 64d4420ee3584a6d81feac210a7e5019 --save --format=csv --count=1000 --AA.AuN="matthias bethge,wieland brendel"

  ```
5 **Retrieve all the papers which are citing specific paper/s**

For example I want to get all the papers which are ciiting the paper `Image Style Transfer Using Convolutional Neural Networks`

  ```
   mag-api 64d4420ee3584a6d81feac210a7e5019 --save --format=csv --count=1000 --Ti="Image Style Transfer Using Convolutional Neural Networks" --citations

  ```

6 **Retrieve all the papers from University/Institute in specific domain**

    For Example retrieving all the papers in the area of Machine learning from University of Tuebingen


  ```
   mag-api 64d4420ee3584a6d81feac210a7e5019 --save --format=csv --count=1000 --AA.AfN="University of tuebingen" --F.FN="machine learning"

  ```
7 **Retrieve author profiles**

  ```
    mag-api 64d4420ee3584a6d81feac210a7e5019 --save --format=csv --entity=author --AuN="matthias bethge,wieland brendel"
  ```
   
8 **Retrieve study fields**

  ```
    mag-api 64d4420ee3584a6d81feac210a7e5019 --save --format=csv --entity="study field" --FN="deep learning,machine learning"
  ```

9 **Retrieve publications from different universities/institutions.**

```
mag-api 64d4420ee3584a6d81feac210a7e5019 --save --format=csv --count=10000 --AA.AfN="university of tuebingen,university of stuttgart"

```

## References
1. https://docs.microsoft.com/en-us/academic-services/graph/
2. https://docs.microsoft.com/en-us/academic-services/project-academic-knowledge/introduction


## Contact

This repo is currently maintained by Kantharaju Narayanappa ([@kantharajucn](http://github.com/kantharaju)).
If you find any bugs or incorrect data please report.