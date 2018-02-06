# mpc-on-ec2

Viff: This clones the asyncmix branch from the repo - https://github.com/amiller/viff/ on each of the VMs.
SPDZ-2: This clones the master branch from the repo - https://github.com/smkuls/SPDZ-2

## Dependencies:
* pip install boto3
* pip install paramiko

Note: Make sure that you install these packages for the correct python version.

## Steps to run:
1. Modify the 'config.json' as follows:
    * Specify the MPC framework you want to run against the 'mpc_framework' key. Must be either 'viff' or 'spdz'.
    * Specify the MPC application which you want to run against the key 'mpc_app_name'.
        Viff: This application must be present in viff/apps directory.
        SPDZ-2: Specify the relative path from the root directory of the repository.
    * Add 'access_key_id' and 'secret_access_key'.
    * Specify the path to the .pem file to access the VMs in 'key_file_path'. This .pem file should correspond to the 'key_name' which must exist in AWS.
    * Update the 'vm_count' and 'vm_name' (give a unique name so it is identifiable on the console easily, all VMs will have the same name) accordingly.
    * You will have to update the 'security_group_ids' appropriately to enable communication between the VMs. Testing was done with a fully open security group.
2. `python mpc_app_runner.py` - When running this for the first time, this will create new EC2 instances on AWS, save their instance ids in a file named 'current.vms', run the commands present in the setup script, and then invoke commands to run the MPC application. Subsequent runs will use the same instances from 'current.vms' file.
3. `python delete_vms.py` - This will delete all the vms whose ids are present in the 'current.vms' file and will also delete the file.
