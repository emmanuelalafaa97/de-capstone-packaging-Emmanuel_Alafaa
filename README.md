# Multi-Source Data Enrichment Pipeline

<p>This project implements a data pipeline that fetches data from multiple API endpoints, handles pagination, enriches product data with seller information, and generates performance insights. The pipeline is configurable, modular, and built using production-grade ETL patterns.</p>


## Overview

<p>Working as a data engineer at OmniCart Analytics, where clients need visibility into not only what products sell, but who is selling effectively. Product and seller information are stored in separate systems and exposed via different endpoints, so the goal is to:</p>

* Retrieve all product and seller records.

* Handle API pagination for large product datasets.

* Combine (enrich) product data with seller attributes.

* Analyze which sellers generate the most revenue and product sales.

* Externalize settings like API URLs and pagination limits into a config file.

<br>This project uses the Fake Store API:
  `` 
     https://fakestoreapi.com/

  ``

## Key Features

Component	Description
ConfigManager	Loads configuration values (e.g., base API URL, pagination limit) from pipeline.cfg
APIClient	Handles all API requests and pagination logic using a limit parameter
DataEnricher	Converts API data into DataFrames and performs a left join to attach seller info to products
DataAnalyzer	Aggregates final metrics such as revenue per seller and average product price
Pipeline	Coordinates the entire ETL process and outputs the final seller_performance_report.json


## Pagination Strategy

<p>The Fake Store API accepts a limit parameter, which controls how many records are returned in one call. </p>

 ```  paginated_data = []
        page = 1

        for skip in range(0, len(data_input), limit):
            chunk = data_input[skip: skip + limit]  

            #add a logger here
            print(f"processing page{page} : {len(chunk)} items")
            paginated_data. extend(chunk)
            page += 1
 ```

## Project Structure

`` omnicart_pipeline/
├── omnicart_pipeline/
│   ├── api_client.py
│   ├── config.py
|   ├── cli.py
│   ├── data_enricher.py
│   ├── data_analyzer.py
    ├── pipeline.cfg
│   └── pipeline.py
├── tests/
│   ├── test_api_client.py
│   ├── test_data_enricher.py
│   ├── test_data_analyzer.py
│   └── test_config.py
└── README.md
``
## Insights Generated

The DataAnalyzer computes for each seller (username):

Metric	Description
Total Revenue	Sum of revenue across all products sold
Number of Products Sold	Count of products listed by seller
Average Product Price	Mean price of seller’s product catalog

Results are stored in: 
   ```
     seller_performance_report.json
  
   ``` 

## Installing and Running the Package 
### Open a virtual environment

    ``` 
       python -m venv environment_name

       #activate the environment before you install the package
       (windows)
       environment_name\Scripts\activate

       (linux)
       source\bin\activate

    ```
    
### install the package
 pip install -i https://test.pypi.org/simple/  --no-deps omnicart-pipeline-project==0.1.0-

** Note : **  use the "--no-deps" before the program name to avoid dependencies errors.