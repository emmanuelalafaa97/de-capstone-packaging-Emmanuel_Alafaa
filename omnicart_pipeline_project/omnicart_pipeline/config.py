import os      #ensure you import os first for the file to run well
from configparser import ConfigParser
import logging
from pathlib import Path


# Get the directory containing the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)

#parent_dir = os.path.dirname(current_dir)
#print("parent dir:", parent_dir)

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ConfigManager(ConfigParser):
    def __init__(self, config_path=None):
        # Call parent class's __init__
        super().__init__()

        if config_path is None:
            # Use default config.ini in the same directory as this script
            config_path = os.path.join(current_dir, 'pipeline.cfg')
            

        self.logger = logging.getLogger("ConfigManager")
        if not os.path.exists(config_path):
            self.logger.error(f"Configuration file '{config_path}' not found.")
            raise FileNotFoundError(f"Configuration file '{config_path}' not found.")
        
        #self.config = ConfigManager.ConfigParser()
        self.read(config_path)
        self.logger.info(f"Loaded configuration from {config_path}")

    @property
    def base_url(self):
        url = self.get('API', 'base_url')
        self.logger.debug(f"Base URL: {url}")
        return url

    @property
    def pagination_limit(self):
        limit = self.getint('PAGINATION', 'pagination_limit')    #getint because the limit is an integer
        self.logger.debug(f"Pagination Limit: {limit}")
        return limit
    

