import json
import os


class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {
            'theme': 'dark',
            'auto_scan': True,
            'auto_connect': False,
            'scan_interval': 60,
            'notifications': True,
            'use_mock_data': False,
            'saved_networks': {}
        }
    
    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def set(self, key, value):
        self.config[key] = value
        self.save_config()
    
    def get_saved_password(self, ssid):
        return self.config.get('saved_networks', {}).get(ssid)
    
    def save_network(self, ssid, password):
        if 'saved_networks' not in self.config:
            self.config['saved_networks'] = {}
        self.config['saved_networks'][ssid] = password
        self.save_config()
    
    def forget_network(self, ssid):
        if 'saved_networks' in self.config and ssid in self.config['saved_networks']:
            del self.config['saved_networks'][ssid]
            self.save_config()
            return True
        return False
    
    def get_saved_networks(self):
        return list(self.config.get('saved_networks', {}).keys())