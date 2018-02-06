#!/usr/bin/env python3
import boto3
from config import AwsConfig
import paramiko
import os.path
import time


class EC2Manager:
    current_vms_file_name = "current.vms"

    def __init__(self):
        self.config = AwsConfig()
        self.ec2 = boto3.resource(
            'ec2',
            aws_access_key_id=self.config.ACCESS_KEY_ID,
            aws_secret_access_key=self.config.SECRET_ACCESS_KEY,
            region_name=self.config.REGION
        )
        self.ec2_client = boto3.client(
            'ec2',
            aws_access_key_id=self.config.ACCESS_KEY_ID,
            aws_secret_access_key=self.config.SECRET_ACCESS_KEY,
            region_name=self.config.REGION
        )

    def __get_setup_commands(self):
        with open("setup.sh", "r") as starter_file:
            return starter_file.read()

    def get_current_vm_details(self):
        with open(EC2Manager.current_vms_file_name, "r") as file_handle:
            data = file_handle.readlines()
        instance_ids = data[0].strip().split(",")
        # print(instance_ids)
        return instance_ids

    def create_instances(self):
        if os.path.isfile(EC2Manager.current_vms_file_name):
            print(">>> Picking up VMs from current.vms file.")
            instance_ids = self.get_current_vm_details()
        else:
            instances = self.ec2.create_instances(
                ImageId=self.config.IMAGE_ID,
                MinCount=self.config.VM_COUNT,
                MaxCount=self.config.VM_COUNT,
                SecurityGroupIds=self.config.SECURITY_GROUP_IDS,
                KeyName=self.config.KEY_NAME,
                InstanceType=self.config.INSTANCE_TYPE,
                TagSpecifications=[
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': self.config.VM_NAME
                            },
                        ]
                    },
                ],
                UserData=self.__get_setup_commands()
            )

            for instance in instances:
                self.ec2.Instance(id=instance.id).wait_until_running()

            instance_ids = [instance.id for instance in instances]

            waiter = self.ec2_client.get_waiter('instance_status_ok')
            waiter.wait(InstanceIds=instance_ids)

            with open(EC2Manager.current_vms_file_name, "w") as file_handle:
                file_handle.write(",".join(instance_ids))

        instance_ips = [self.get_instance_public_ip(instance_id)
                        for instance_id in instance_ids]
        return instance_ids, instance_ips

    def list_all_instances(self):
        for instance in self.ec2.instances.all():
            print(
                instance.id,
                instance.state,
                instance.tags,
                instance.public_ip_address
                )

    def terminate_instances_by_name(self):
        self.ec2.instances.filter(
            Filters=[{'Name': 'tag:' + "Name",
                      'Values': [self.config.VM_NAME]}]).terminate()

    def terminate_instances_by_id(self):
        instance_ids = self.get_current_vm_details()
        self.ec2.instances.filter(InstanceIds=instance_ids).terminate()
        if os.path.isfile(EC2Manager.current_vms_file_name):
            os.remove(EC2Manager.current_vms_file_name)

    def get_instance_public_ip(self, instance_id):
        return self.ec2.Instance(id=instance_id).public_ip_address

    def execute_command_on_instance(
            self,
            instance_id,
            commands,
            display_output=False,
            write_output_to_file=False):

        key = paramiko.RSAKey.from_private_key_file(self.config.KEY_FILE_PATH)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        instance_ip = self.get_instance_public_ip(instance_id)

        try:
            ssh_client.connect(
                    hostname=instance_ip,
                    username=self.config.INSTANCE_USER_NAME,
                    pkey=key)
            for command in commands:
                stdin, stdout, stderr = ssh_client.exec_command(command)
                output = stdout.read()

                if display_output and len(output) != 0:
                    print()
                    print("########################### " + "OUTPUT FROM: " +
                          instance_id + " " + command + " ##################")
                    print(output.decode('utf-8'))
                    print("###############################################" +
                          "###########################")

                if write_output_to_file and len(output) != 0:
                    with open(("output-" + instance_id), 'w') as file:
                        file.write(output.decode('utf-8'))

                err = stderr.read()
                if display_output and len(err) != 0:
                    print()
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~ " + "ERROR WHILE" +
                          " EXECUTING COMMAND ON: " + instance_id + " " +
                          command + " ~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    print(err.decode('utf-8'))

                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" +
                          "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

                if write_output_to_file and len(err) != 0:
                    with open(("error-" + instance_id), 'w') as file:
                        file.write(output.decode('utf-8'))

            ssh_client.close()

        except Exception as ex:
            print(ex)
