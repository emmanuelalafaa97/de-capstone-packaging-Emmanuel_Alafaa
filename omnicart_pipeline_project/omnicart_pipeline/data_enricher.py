import pandas as pd
#from omnicart_pipeline.api import API

try:
    from api import API  # Relative import
except ImportError:
    from omnicart_pipeline.api import API

class Enricher:
    def data_enricher():
             client = API()
             Users_data = client.get_all_users()
             if Users_data:
                    users_df = pd.DataFrame(Users_data)
                    print("All Users dataframe successfully created")
                    print(users_df.head())
                    return users_df         #ensure to return the dataframe if you do not want to save it
                    #users_df.to_csv(r"week4\data_and_other_info\data_exported\users_data.csv",index=False)
             else:
                     print(("Failed to fetch users data"))

             All_products_data = client.get_all_products()
             if All_products_data:
                     prod_df = pd.DataFrame(All_products_data)
                     print("Products dataframe successfully created")
                     print(prod_df.head())
                     #save the dataframe in a csv file
                     #prod_df.to_csv(r"week4\data_and_other_info\data_exported\products_data.csv", index=False)
                     return prod_df     #ensure to return the dataframe if you do not want to save it
             else:
                     print(("Failed to fetch Product data"))
    
     #or since we are not saving to csv then it is better to divide the users and products data into 2 separate functions

    def users_data_enricher():
             client = API()
             Users_data = client.get_all_users()
             if Users_data:
                    users_df = pd.DataFrame(Users_data)
                    print("All Users dataframe successfully created")
                    print(users_df.head())
                    print("datatype:,", type(users_df))
                    print(users_df.dtypes)
                    return users_df       #ensure to return the dataframe if you do not want to save it
             else:
                     print(("Failed to fetch users data"))

    def prod_data_enricher():
             client = API()
             All_products_data = client.get_all_products()
             if All_products_data:
                     prod_df = pd.DataFrame(All_products_data)
                     print("Products dataframe successfully created")
                     print(prod_df.head()) 
                     print(prod_df.dtypes) 
                     return prod_df          #ensure to return the dataframe if you do not want to save it so that you can continue the pipeline
             else:
                     print(("Failed to fetch Product data"))
           
    
    if __name__ == "__main__":
           #data_enricher()   #call for it to run
           users_data_enricher()
           prod_data_enricher()