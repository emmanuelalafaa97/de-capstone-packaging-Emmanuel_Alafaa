import pandas as pd
import logging 
import json
import os
from omnicart_pipeline.pipeline import Pipeline




if __name__ == "__main__":
    p = Pipeline()
    result = p.run()
    print("\nAnalysis result (head):")
    try:
        # If it's a DataFrame
        print(result.head())
    except Exception:
        print(result)