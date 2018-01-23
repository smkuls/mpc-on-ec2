#!/usr/bin/env python3
from ec2Manager import EC2Manager
import time

def viff_app_runner_helper(ec2Manager, instance_ids, instance_ips, viff_app):
    
    port_numbers = [9000+i for i in range(1, ec2Manager.config.VM_COUNT + 1)]
    n = ec2Manager.config.VM_COUNT
    # kill_previous_commands = "killall python"
    for player_number, instance_id in zip(range(1, n + 1), instance_ids):
        viff_config_command = "python ~/viff/apps/generate-config-files.py -n "+str(n)+" -t 1"
        for port_number, instance_ip in zip(port_numbers, instance_ips):
            viff_config_command += " " + instance_ip+":"+str(port_number)

        viff_app_command = "python ~/viff/apps/" + viff_app +" --no-ssl --statistics" \
            " --deferred-debug player-" + str(player_number)+".ini > output 2>&1 &"

        print (viff_config_command)
        print (viff_app_command)
        # ec2Manager.execute_command_on_instance(instance_id, [kill_previous_commands, viff_config_command, viff_app_command])
        ec2Manager.execute_command_on_instance(instance_id, [viff_config_command, viff_app_command])

def display_output(ec2Manager, instance_ids):
    for instance_id in instance_ids:
        ec2Manager.execute_command_on_instance(instance_id, ["cat ~/output"], True)

def run_viff_app():
    ec2Manager = EC2Manager()
    instance_ids, instance_ips = ec2Manager.create_instances()
    viff_app_runner_helper(ec2Manager, instance_ids, instance_ips, ec2Manager.config.VIFF_APP_NAME)
    time.sleep(ec2Manager.config.SLEEP_TIMEOUT_IN_SECONDS)
    display_output(ec2Manager, instance_ids)

run_viff_app()
