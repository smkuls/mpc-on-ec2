#!/usr/bin/env python3
from ec2Manager import EC2Manager
import time

def run_viff_millionaires(instance_ids, instance_ips):
    port_numbers = [9000+i for i in range(1, ec2Manager.config.VM_COUNT + 1)]

    # kill_previous_commands = "killall python"
    for player_number, instance_id in zip(range(1, ec2Manager.config.VM_COUNT + 1), instance_ids):
        viff_config_command = "python ~/viff/apps/generate-config-files.py -n "+str(ec2Manager.config.VM_COUNT)+" -t 1"
        for port_number, instance_ip in zip(port_numbers, instance_ips):
            viff_config_command += " " + instance_ip+":"+str(port_number)

        viff_app_command = "python ~/viff/apps/millionaires.py --no-ssl player-"+str(player_number)+".ini > output 2>&1 &"

        # print (viff_config_command)
        # print (viff_app_command)
        ec2Manager.execute_command_on_instance(instance_id, [viff_config_command, viff_app_command])

def display_output(instance_ids):
    for instance_id in instance_ids:
        ec2Manager.execute_command_on_instance(instance_id, ["cat ~/output"], True)

ec2Manager = EC2Manager()

instance_ids, instance_ips = ec2Manager.create_instances()

# instance_ids = ['i-0d84e2917acb29b3c', 'i-0f13caa0b8003ff4a', 'i-044430258e0d9c0fc']
# instance_ips = ['52.90.110.187', '54.158.52.208', '54.226.185.62']

# print(instance_ips)
# print(instance_ids)
run_viff_millionaires(instance_ids, instance_ips)
time.sleep(2)
display_output(instance_ids)
