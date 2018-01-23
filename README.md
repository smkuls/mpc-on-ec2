# ec2runner

## Dependencies:
* pip install boto3
* pip install paramiko

Note: Make sure that you install these packages for the correct python version.

## Steps to run:
1. Rename config.dummy.json to config.json
2. Add 'access_key_id' and 'secret_access_key'
3. Specify the path to the .pem file to access the VMs in 'key_file_path'. This .pem file should correspond to the 'key_name' which exists in AWS.
4. `python run_millionaires.py` - When running this for the first time, this will create new EC2 instances on AWS, save their instance ids in the 'current.vms' file and run the commands present in 'setup.sh'. Subsequent runs will use the same instance ids.
5. `python delete_vms.py` - This will delete all the vms whose ids are present in the 'current.vms' file and also delete the file.