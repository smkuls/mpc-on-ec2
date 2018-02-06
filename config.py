import json


class AwsConfig:

    def __init__(self):
        self.__load()

    def __load(self):
        config = json.load(open('config.dummy.json'))
        self.MPC_FRAMEWORK = config["mpc_framework"]
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
        self.INSTANCE_USER_NAME = config["instance_user_name"]
        self.MPC_APP_NAME = config["mpc_app_name"]
        self.SLEEP_TIMEOUT_IN_SECONDS = config["sleep_timeout_in_seconds"]
