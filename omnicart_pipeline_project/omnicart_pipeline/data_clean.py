import pandas as pd
import ast     # remember to import this library
from omnicart_pipeline.data_enricher import Enricher
import json

users_data = Enricher.users_data_enricher()
products_data = Enricher.prod_data_enricher()

#convert to a dataframe
#users_data_df = pd.read_csv(r"week4\data_and_other_info\data_exported\users_data.csv")
#prod_data_df = pd.read_csv(r"week4\data_and_other_info\data_exported\products_data.csv")

users_data_df = pd.DataFrame(users_data)
prod_data_df = pd.DataFrame(products_data)

class Cleaning:
    

    def __init__(self):
        pass
     
     
    def left_merged(self, df_1 : pd.DataFrame, df_2 : pd.DataFrame, on: str = "id", how: str = "left"): 
     try:
         # First verify the merge column exists in both dataframes
         if on not in df_1.columns:
                raise KeyError(f"Column '{on}' not found in first DataFrame. Available columns: {df_1.columns.tolist()}")
         if on not in df_2.columns:
                raise KeyError(f"Column '{on}' not found in second DataFrame. Available columns: {df_2.columns.tolist()}")
         left_merged_df = pd.merge(df_1, df_2, on=on, how=how)
         print("number of rows and columns in new dataframe:", left_merged_df.shape)
         #return left_merged_df.head()
     
     except ValueError:
          print("Failed to merge")
          return ValueError
     return left_merged_df
     
    #def handle_missing_mergers(file_one_df, file_two_df):
    #left_merged_df = pd.merge(file_one_df, file_two_df, on='id', how='left')
    #for col in left_merged_df.columns:
        #if left_merged_df[col].isnull().any():
            #print(f"Column '{col}' has missing values.")
    #if file_one_df.equals(file_two_df):
        #print("Both files have identical data.")
    #elif file_one_df.shape[0] > file_two_df.shape[0]:
        #print("File one has more rows than file two.")
    #elif file_one_df.shape[0] < file_two_df.shape[0]:
        #print("File two has more rows than file one.")
    #elif file_one_df.shape[0] == file_two_df.shape[0]:
        #print("Both files have the same number of rows but different data.")
    #elif file_one_df.shape[1] != file_two_df.shape[1]:
        #print("Files have different number of columns.")
    #return left_merged_df
    #left_merged()

    # this function cleans the data by expanding dictionary-like columns, it can be a stand file or program module to clean any json or csv data
    @staticmethod
    def clean_data(df: pd.DataFrame):     #note the use of static decorator for functions in class that will take in an argument
        """
         Automatically expands columns in a DataFrame that contain dictionary-like strings.

        For example:
        {'rate': 4.1, 'count': 259}
         becomes two columns: columnname_rate and columnname_count
        """
        #create a copy of the datafram
        out = df.copy()

        for col in out.columns:
          # Check if column values look like dictionaries
          if out[col].apply(lambda x: isinstance(x, (dict, str))).all():
            try:
                # Convert string dicts to actual dicts if needed
                out[col] = out[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
                
                # Check if the column contains dicts after conversion
                if out[col].apply(lambda x: isinstance(x, dict)).any():
                    expanded = out[col].apply(pd.Series)
                    expanded.columns = [f"{col}_{subcol}" for subcol in expanded.columns]
                    print(f"splitting column: {col} into {list(expanded.columns)}")
                    #print("new dataframe shape:", out.shape)
                    
                    # Join back to the main DataFrame
                    out = out.join(expanded)
                    out = out.drop(columns=[col])
                    print("new dataframe shape:", out.shape)
            except Exception:
                continue  # skip if not safely evaluable
        return out     #out not df for the new shape to show
 
     
    #function to create a new column 'revenue' by multiplying 'price' and 'rating_count'
    def handle_null_revenue(df):
      if 'price' in df.columns and 'rating_count' in df.columns:
            df['revenue'] = df['price'] * df['rating_count']     #creates a new column 'revenue' by multiplying 'price' and 'rating_count'
      else:
          raise KeyError("Required columns for revenue calculation are missing.")
      return df
    
    

    

    
if __name__ == "__main__":
        # to use get your data either in a csv or json format and 
      
      #users_data_df = pd.DataFrame(users_data)
      #prod_data_df = pd.DataFrame(products_data)

      cleaner= Cleaning()
      data = cleaner.left_merged(users_data_df, prod_data_df)  # frist convert it to a dataframe
      cleaned_df = cleaner.clean_data(data)      #Then use the clean_data function
      print(cleaned_df.shape)             #print out the first 5 rows to see the result

      transformed_data = Cleaning.handle_null_revenue(cleaned_df) #calling the function to create 'revenue' column
      #transformed_data.to_csv(r"week4\data_and_other_info\data_exported\transformed_data.csv", index=False) #saving the transformed data to a csv file    
      
      
      #save the dataframe to a csv file and check it out
      #cleaned_df.to_csv(r"week4\data_and_other_info\data_exported\cleaned_data.csv", index=False)

      #Second_cleaned_df = clean_data(cleaned_df)  # you can run the clean_data function again if needed
      #Second_cleaned_df.head()
