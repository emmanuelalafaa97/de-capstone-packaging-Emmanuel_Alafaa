import pandas as pd
import logging 
import json
import os
from omnicart_pipeline.data_enricher import Enricher
from configparser import ConfigParser
from omnicart_pipeline.api import API
from omnicart_pipeline.data_analyzer import Analyzer
from omnicart_pipeline.data_clean import Cleaning

current_dir = os.getcwd()

class Pipeline:

    def __init__(self):
        # Call parent class's __init__
        super().__init__()


    def run(self):
        #Enricher.data_enricher()
        users_data_df = Enricher.users_data_enricher()
        prod_data_df = Enricher.prod_data_enricher()

        cleaner= Cleaning()
        data = cleaner.left_merged(users_data_df, prod_data_df)  # frist convert it to a dataframe
        cleaned_df = cleaner.clean_data(data)
        transformed_df = Cleaning.handle_null_revenue(cleaned_df)
        #analyzed_df = Analyzer.all_analysis(transformed_df)
        
            # Call Analyzer.all_analysis in a safe way (supports class/static or instance method)
        try:
            analyzed_df = Analyzer.all_analysis(transformed_df)  
            print("data_type:",type(analyzed_df))
            #save final report
            with open(r"sellers_performance_report.json", 'w') as json_file:
                json.dump(analyzed_df, json_file, indent=4)

            print("\nData has been saved to 'sellers_performance_report.json'") 
        except (AttributeError, TypeError):
            analyzer = Analyzer()
            analyzed_df = analyzer.all_analysis(transformed_df)

        return analyzed_df

    

    
    
if __name__ == "__main__":
    p = Pipeline()
    result = p.run()
    print("\nAnalysis result (head):")
    try:
        # If it's a DataFrame
        print(result.head())
    except Exception:
        print(result)

        