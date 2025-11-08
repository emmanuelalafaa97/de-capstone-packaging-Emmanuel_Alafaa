import os
import requests
import logging
from pathlib import Path
#from omnicart_pipeline.config import ConfigManager


try:
    from .config import ConfigManager  # Relative import
except ImportError:
    from omnicart_pipeline.config import ConfigManager

#ensure you put the .cfg or .ini file here and not config.py

current_dir = os.path.dirname(os.path.abspath(__file__))
class API:
    CONFIGMANAGER = ConfigManager()      #just call the ConfigManager() without any arguments

    # Configure basic logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


    def __init__(self) :   #no need to put def __init__(self, base_url, limit), because the API class is always supposed to read its URL from the configuration file, hence no need for another "base_url" argument unless you want it to read based on manual change from each files
         super().__init__()
         self.base_url = API.CONFIGMANAGER.get("API", "base_url")
         self.limit = int(API.CONFIGMANAGER.get("PAGINATION", "pagination_limit"))


    def pagination(self, data_input:list[dict], limit: int) :
        paginated_data = []
        page = 1

        for skip in range(0, len(data_input), limit):
            chunk = data_input[skip: skip + limit]  

            #add a logger here
            print(f"processing page{page} : {len(chunk)} items")
            paginated_data.extend(chunk)
            page += 1

        return paginated_data    #outside so that it returns the last data and not each pages with the page number
       
    #function to fetch all users data from the API
    def get_all_users(self) -> dict:
         """Fetches all users by their ID."""
         endpoint = f"/users"                 # note for your links use f"/users"  not f"/users/" so that it matches what you have in your tests
         url = self.base_url + endpoint 

         logging.info(f"Fetching user from {url}")
         try:
             response = requests.get(url)
             response.raise_for_status() # Check for HTTP errors
             all_users = response.json()    # return response.json   if you are not paginating
         
             # Apply pagination using the limit from config
             paginated_users = self.pagination(all_users, self.limit)
             logging.info(f"Successfully paginated {len(all_users)} users into chunks of {self.limit}")
             return paginated_users
         
         except requests.exceptions.RequestException as e:
             logging.error(f"API request failed: {e}")
             # Return an empty dict or raise a custom exception
             return {}
        
    def get_all_products(self):
        '''Fetches all products by their product IDs'''
        endpoint = f"/products/"
        url = self.base_url + endpoint 

        #try: 
            #r = requests.get(url)
            #r.raise_for_status()  #checking http errors
            #return r.json()  #not callit back as a .json() file because "r.text" would cause issues
        #except requests.exceptions.RequestException as e:
            #logging.error(f"API Request Failed: {e}")
            #return {}
        try: 
            r = requests.get(url)
            r.raise_for_status()  #checking http errors
            all_products = r.json()

            paginated_products = self.pagination(all_products, self.limit)
            logging.info(f"Successfully paginated {len(all_products)} users into chunks of {self.limit}")
            return paginated_products
         
        except requests.exceptions.RequestException as e:
             logging.error(f"API request failed: {e}")
             # Return an empty dict or raise a custom exception
             return {}
        
   


    

    