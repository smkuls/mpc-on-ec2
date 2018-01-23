# ec2runner

## Dependencies:
* pip install boto3
* pip install paramiko

Note: Make sure that you install these packages for the correct python version.

## Steps to run:
1. Rename config.dummy.json to config.json
2. Add 'access_key_id' and 'secret_access_key'
3. Specify the path to the .pem file to access the VMs in 'key_file_path'. This .pem file should correspond to the 'key_name' which exists in AWS.