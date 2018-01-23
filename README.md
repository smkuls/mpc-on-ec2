# viff-on-ec2

This clones the asyncmix branch from the repo - https://github.com/amiller/viff/ on each of the VMs.

## Dependencies:
* pip install boto3
* pip install paramiko

Note: Make sure that you install these packages for the correct python version.

## Steps to run:
1. Modify the 'config.json' as follows:
    * Specify the viff application which you want to run against the key 'viff_app_name', this application must be present in viff/apps directory.
    * Add 'access_key_id' and 'secret_access_key'.
    * Specify the path to the .pem file to access the VMs in 'key_file_path'. This .pem file should correspond to the 'key_name' which must exist in AWS.
    * Update the 'vm_count' and 'vm_name' (give a unique name so it is identifiable on the console easily, all VMs will have the same name) accordingly.
    * You will have to update the 'security_group_ids' appropriately to enable communication between the VMs. Testing was done with a fully open security group.
2. `python viff_app_runner.py` - When running this for the first time, this will create new EC2 instances on AWS, save their instance ids in a file named 'current.vms', run the commands present in 'setup.sh' and then invoke commands to run the viff application. Subsequent runs will use the same instances from 'current.vms' file.
3. `python delete_vms.py` - This will delete all the vms whose ids are present in the 'current.vms' file and will also delete the file.