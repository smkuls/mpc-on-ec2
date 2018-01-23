import json
from pprint import pprint

class AwsConfig:

    def __init__(self):
        self.__load()

    def __load(self):
        config = json.load(open('config.json'))
        self.ACCESS_KEY_ID = config["access_key_id"]
        self.SECRET_ACCESS_KEY = config["secret_access_key"]
        self.REGION = config["region"]
        self.VM_COUNT = config["vm_count"]
        self.IMAGE_ID = config["image_id"]
        self.SECURITY_GROUP_IDS = config["security_group_ids"]
        self.KEY_NAME = config["key_name"]
        self.INSTANCE_TYPE = config["instance_type"]
        self.VM_NAME = config["vm_name"]
        self.KEY_FILE_PATH = config["key_file_path"]
        self.SETUP_SCRIPT_PATH = config["setup_script_path"]
