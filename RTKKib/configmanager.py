import json

class ConfigManager:
    _instance = None
    _config_data = None

    def __new__(cls, config_file=None):
        if cls._instance is None:
            cls._instance = super(ConfigManager,cls).__new__(cls)
            cls._config_data = cls._load_config(config_file)

        return cls._instance
    
    @staticmethod
    def _load_config(config_file):
        with open(config_file,'r') as file:
            return json.load(file)
        
    def get_config(self):
        return self._config_data
    
    def get_value(self,key):
        return self._config_data[key]
    